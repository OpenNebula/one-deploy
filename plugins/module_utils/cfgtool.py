# -*- coding: utf-8 -*-
# Copyright: OpenNebula Project, OpenNebula Systems
# Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

import copy
import fnmatch
import io
import re


class ParserEngine:
    class ParseFailure(Exception): pass

    def __init__(self, inp):
        self._inp = inp
        self._pos = 0

    def zero_or_more(self, parser):
        try:
            matches = []
            while True:
                matches.append(self.__backtrack(parser))
        except self.ParseFailure:
            return matches

    def one_of(self, *parsers):
        for parser in parsers:
            try:
                return self.__backtrack(parser)
            except self.ParseFailure:
                pass
        self.quit()

    def between(self, begin, end, inner):
        def block():
            begin(); t = inner(); end()
            return t
        return self.__backtrack(block)

    def peek(self, length=1):
        s = self._input()[0:length]
        return s if len(s) == length else self.quit()

    def take(self, length=1):
        t = self.peek(length); self.__consume(length)
        return t

    def take_exact(self, pattern):
        def block():
            s = self.take(len(pattern))
            return s if s == pattern else self.quit()
        return self.__backtrack(block)

    def take_while(self, pred):
        try:
            s = ''
            def block():
                c = self.take()
                return c if pred(c) else self.quit()
            while True:
                s += self.__backtrack(block)
            return s
        except self.ParseFailure:
            return s

    def quit(self):
        raise self.ParseFailure

    def _input(self):
        return self._inp[self._pos:]

    def __consume(self, length=1):
        self._pos += length

    def __backtrack(self, parser):
        try:
            before = self._pos
            return parser()
        except self.ParseFailure as e:
            self._pos = before
            raise e


class ParserBase(ParserEngine):
    class InvalidPath(Exception): pass
    class InvalidTree(Exception): pass
    class AmbiguousMatch(Exception): pass
    class EmptyMatch(Exception): pass

    class Meta:
        def setm(self, k, v): setattr(self, k, v); return self
        def getm(self, k): return getattr(self, k)

    class Lookup(Meta, dict):
        @classmethod
        def from_args(cls, *a): return cls(a)

    class Sequence(Meta, list):
        @classmethod
        def from_args(cls, *a): return cls(a)

    class Pair(Sequence):
        @classmethod
        def from_args(cls, *a): return cls(a)

    class Comment(Meta, str):
        @classmethod
        def from_str(cls, s): return cls(s) if ('#' in s) else str(s)

    def __init__(self, inp):
        super().__init__(inp)

    def parse(self):
        self.parsed = self.parser_proc()
        if len(self._input()) > 0:
            line = self._inp[0:self._pos].count('\n') + 1
            text = self._inp[self._pos:(self._pos + 16)].split('\n', 1)[0]
            raise self.ParseFailure(f"line {line}, at `{text}..'")
        return self.parsed

    def render(self, node=None):
        raise NotImplementedError

    def match(self, path, value=None):
        atrb, atrb_i, item, item_i = self._ypath(path, wildcards=True)
        def recurse(node, pfx, acc):
            if isinstance(node, self.Pair) and (value is None or node[3] == str(value)):
                i = node.getm('_index_')
                idx = '' if i is None else f'[{i}]'
                acc.append(pfx + idx)
            elif isinstance(node, self.Sequence):
                for v in node:
                    recurse(v, pfx, acc)
            elif isinstance(node, self.Lookup):
                if len(pfx) > 0:
                    i = node.getm('_index_')
                    idx = '' if i is None else f'[{i}]'
                    pfx += idx + '/'
                for k, v in node.items():
                    recurse(v, pfx + k, acc)
        found = []
        recurse(self._filtered(patterns=[atrb, item], indices=[atrb_i, item_i]), '', found)
        return found

    def get(self, path):
        atrb, atrb_i, item, item_i = self._ypath(path, wildcards=True)
        def recurse(node, acc):
            if isinstance(node, self.Pair):
                acc.append(node[3])
            elif isinstance(node, self.Sequence):
                for v in node:
                    recurse(v, acc)
            elif isinstance(node, self.Lookup):
                for v in node.values():
                    recurse(v, acc)
        found = []
        recurse(self._filtered(patterns=[atrb, item], indices=[atrb_i, item_i]), found)
        return found

    def put(self, path, value):
        raise NotImplementedError

    def drop(self, path, value=None):
        raise NotImplementedError

    def _ypath(self, path, wildcards=True):
        raise NotImplementedError

    def _searchable(self, node=None):
        raise NotImplementedError

    def _filtered(self, node=None, patterns=None, indices=None):
        def recurse(node, patterns, indices):
            if isinstance(node, self.Pair) and len(patterns) == 0:
                return node
            elif isinstance(node, self.Lookup):
                try:
                    pat = patterns.pop(0)
                except IndexError:
                    pat = None
                if pat is not None:
                    acc = {}
                    for k, vv in node.items():
                        if fnmatch.fnmatch(k, pat):
                            v = recurse(vv, copy.copy(patterns), copy.copy(indices))
                            if v is not None:
                                acc[k] = v
                    if acc:
                        return self.Lookup(acc).setm('_index_', node.getm('_index_'))
            elif isinstance(node, self.Sequence):
                try:
                    idx = indices.pop(0)
                except IndexError:
                    idx = None
                if idx is None or (idx == 0 and len(node) > 1):
                    acc = []
                    for vv in node:
                        v = recurse(vv, copy.copy(patterns), copy.copy(indices))
                        if v is not None:
                            acc.append(v)
                    acc = [x for x in acc if x is not None]
                    if acc:
                        return self.Sequence(acc)
                elif idx is not None and idx != 0 and len(node) > 1 and node[idx - 1] is not None:
                    v = recurse(node[idx - 1], copy.copy(patterns), copy.copy(indices))
                    if v is not None:
                        return self.Sequence([v])
        return recurse(
            self._searchable(node or self.parsed),
            [x for x in copy.copy(patterns or []) if x is not None],
            copy.copy(indices or [])
        )


class OneParser(ParserBase):
    class Vector(ParserBase.Sequence): pass

    def parser_proc(self):
        def quoted():
            escaped = [False]
            def pred(c):
                if c == '\\' or (c == '"' and escaped[0]):
                    escaped[0] = not escaped[0]
                    return True
                else:
                    return c != '"'
            return self.between(lambda: self.take_exact('"'),
                                lambda: self.take_exact('"'),
                                lambda: '"' + self.take_while(pred) + '"')

        def unquoted():
            def pred(c):
                return not (c in [']', '[', '"', ',', '#'] or c.isspace())
            return self.take_while(pred) if pred(self.peek()) else self.quit()

        def attribute():
            return self.take_while(lambda c: c == '_' or c.isalnum())

        def blank():
            return self.take_while(lambda c: c in [' ', '\t'])

        def eol():
            return self.take_exact('\n')

        def blank_eol():
            return blank() + eol()

        def comment():
            return self.Comment.from_str(
                blank() + self.take_exact('#')
                        + self.take_while(lambda c: c != '\n')
                        + eol()
            )

        def pair():
            return self.Pair.from_args(
                blank(),
                attribute(),
                blank() + self.take_exact('=') + blank(),
                self.one_of(quoted,
                            unquoted),
                self.one_of(comment,
                            blank_eol,
                            blank)
            )

        def blank_comma():
            t = blank(); self.take_exact(',')
            return t

        def item():
            return self.Pair.from_args(
                blank(),
                attribute(),
                blank() + self.take_exact('=') + blank(),
                self.one_of(quoted,
                            unquoted),
                self.one_of(lambda: self.Comment.from_str(blank_comma() + comment()),
                            lambda: blank_comma() + blank_eol(),
                            blank_comma,
                            comment,
                            blank_eol,
                            blank)
            )

        def vector():
            return self.Vector.from_args(
                blank(),
                attribute(),
                blank() + self.take_exact('=') + blank(),
                self.between(lambda: self.take_exact('['),
                             lambda: self.take_exact(']'),
                             lambda: self.Sequence.from_args(
                            *(self.zero_or_more(lambda: self.one_of(item,
                                                                    comment,
                                                                    blank_eol)))
                        )
                ),
                self.one_of(comment,
                            blank_eol,
                            blank)
            )

        return self.Sequence.from_args(
            *(self.zero_or_more(lambda: self.one_of(pair,
                                                    vector,
                                                    comment,
                                                    blank_eol)))
        )

    def __init__(self, inp):
        super().__init__(inp)

    def render(self, node=None):
        acc = ''
        for vv in (node or self.parsed):
            if isinstance(vv, str):
                acc += vv
            elif isinstance(vv, self.Pair):
                acc += ''.join(vv)
            elif isinstance(vv, self.Vector):
                acc += ''.join(vv[0:3])
                acc += '['
                count = 0
                for v in vv[3]:
                    if isinstance(v, self.Pair):
                        count += 1
                for v in vv[3]:
                    if isinstance(v, str):
                        acc += v
                    elif isinstance(v, self.Pair):
                        acc += ''.join(v[0:4])
                        count = count - 1
                        if count > 0:
                            acc += ','
                        acc += v[4]
                    else:
                        raise self.InvalidTree
                acc += ']'
                acc += vv[4]
            else:
                raise self.InvalidTree
        return acc

    def put(self, path, value):
        atrb, atrb_i, item, item_i = self._ypath(path, wildcards=False)
        s = self._searchable()

        # add a new pair directly at the root level
        if (s.get(atrb) is None or (atrb_i is not None and atrb_i == 0)) and item is None:
            self.parsed.append(self.Pair.from_args(
                '', atrb, ' = ', str(value), '\n'
            ))
            return

        # add a new vector with a single pair directly at the root level
        if (s.get(atrb) is None or (atrb_i is not None and atrb_i == 0)) and item is not None:
            self.parsed.append(self.Vector.from_args(
                '', atrb, ' = ', self.Sequence.from_args(
                    '\n', self.Pair.from_args(
                        ' ', item, ' = ', str(value), ' '
                    )
                ), '\n'
            ))
            return

        # require paths to be unequivocal
        if atrb_i is None and len(s[atrb]) > 1:
            raise self.AmbiguousMatch

        # fail when nothing found
        try:
            s = s[atrb][0 if atrb_i is None else (atrb_i - 1)]
        except (KeyError, IndexError):
            raise self.EmptyMatch

        # when second pattern is provided then first one must not resolve into a pair
        # when second pattern is not provided then first one must resolve into a pair
        if (item is None) ^ isinstance(s, self.Pair):
            raise self.InvalidPath

        # update the value (root level)
        if item is None:
            s[3] = str(value)
            return

        # add a new pair to an existing vector
        if s.get(item) is None or (item_i is not None and item_i == 0):
            parent = s[list(s.keys())[0]][0].getm('_parent_') # get parent from a neighbor pair
            indent = self.__infer_vector_indent(parent)
            # apply suffix correction to the former last pair
            indent['prev_pair'][4] = indent['prev_suffix']
            # append new correctly indented pair
            parent.append(self.Pair.from_args(
                indent['next_prefix'], item, ' = ', str(value), indent['next_suffix']
            ))
            return

        # require paths to be unequivocal
        if item_i is None and len(s[item]) > 1:
            raise self.AmbiguousMatch

        # fail when nothing found
        try:
            s = s[item][0 if item_i is None else (item_i - 1)]
        except (KeyError, IndexError):
            raise self.EmptyMatch

        # second pattern must resolve into a pair
        if not isinstance(s, self.Pair):
            raise self.InvalidPath

        # update the value (vector level)
        s[3] = str(value)
        return

    def drop(self, path, value=None):
        atrb, atrb_i, item, item_i = self._ypath(path, wildcards=True)
        def recurse(node):
            if isinstance(node, self.Pair) and (value is None or node[3] == str(value)):
                parent = node.getm('_parent_')
                for i, x in enumerate(parent):
                    if id(x) == id(node):
                        parent.pop(i)
                        break
            elif isinstance(node, self.Sequence):
                for v in node:
                    recurse(v)
            elif isinstance(node, self.Lookup):
                for v in node.values():
                    recurse(v)
        recurse(self._filtered(patterns=[atrb, item], indices=[atrb_i, item_i]))
        # remove empty vectors
        for node in self.parsed:
            if isinstance(node, self.Vector) and not [v for v in node[3] if isinstance(v, self.Pair)]:
                for i, x in enumerate(self.parsed):
                    if id(x) == id(node):
                        self.parsed.pop(i)
                        break

    def _ypath(self, path, wildcards=True):
        if isinstance(path, list):
            path = '/'.join(path)
        wild = '*' if wildcards else ''
        regx = rf'''(?x)
            ^
            ( [A-Za-z0-9_{wild}]+ )
            (?:
                \[ ( [0-9]* ) \]
            )?
            (?:
                /
                ( [A-Za-z0-9_{wild}]+ )
                (?:
                    \[ ( [0-9]* ) \]
                )?
            )?
            $
        '''
        m = re.match(regx, path)
        if m is None:
            raise self.InvalidPath

        atrb   = m[1]
        atrb_i = None if len(m[2] or '') == 0 else int(m[2])
        item   = m[3]
        item_i = None if len(m[4] or '') == 0 else int(m[4])
        if atrb is None or (item is None and item_i is not None) \
                        or (atrb_i is not None and int(atrb_i) < 0) \
                        or (item_i is not None and int(item_i) < 0):
            raise self.InvalidPath

        return atrb, atrb_i, item, item_i

    def _searchable(self, node=None):
        def recurse1(node):
            acc = self.Lookup()
            for v in node:
                if isinstance(v, self.Pair):
                    acc[v[1]] = acc.get(v[1], self.Sequence())
                    acc[v[1]].append(v)
                    v.setm('_parent_', node)
                elif isinstance(v, self.Vector):
                    acc[v[1]] = acc.get(v[1], self.Sequence())
                    acc[v[1]].append(recurse1(v[3]))
            return acc
        def recurse2(node, index):
            if isinstance(node, self.Pair):
                node.setm('_index_', index)
            elif isinstance(node, self.Sequence):
                for i, v in enumerate(node):
                    recurse2(v, (i + 1) if (len(node) > 1) else None)
            elif isinstance(node, self.Lookup):
                node.setm('_index_', index)
                for v in node.values():
                    recurse2(v, None)
            return node
        return recurse2(recurse1(node or self.parsed), None)

    def __infer_vector_indent(self, parent):
        acc = { 'has_eol': False,
                'prev_pair': None,
                'next_prefix': '',
                'prev_suffix': '',
                'next_suffix': '' }
        for node in parent:
            if isinstance(node, str):
                if '\n' in node:
                    acc['has_eol'] = True
            elif isinstance(node, self.Pair):
                if '\n' in node[4]:
                    acc['has_eol'] = True
                acc['prev_pair'] = node
        acc['next_prefix'] = copy.copy(acc['prev_pair'][0])
        s = acc['prev_pair'][4]
        if isinstance(s, self.Comment):
            acc['prev_suffix'] = copy.copy(s)
            acc['next_suffix'] = ' '
        else:
            acc['prev_suffix'] = '\n' if acc['has_eol'] else ''
            acc['next_suffix'] = copy.copy(s)
        return acc


class RcParser(ParserBase):
    def parser_proc(self):
        def single_quoted():
            return self.between(lambda: self.take_exact("'"),
                                lambda: self.take_exact("'"),
                                lambda: "'" + self.take_while(lambda c: c != "'") + "'")

        def double_quoted():
            escaped = [False]
            def pred(c):
                if c == '\\' or (c == '"' and escaped[0]):
                    escaped[0] = not escaped[0]
                    return True
                else:
                    return c != '"'
            return self.between(lambda: self.take_exact('"'),
                                lambda: self.take_exact('"'),
                                lambda: '"' + self.take_while(pred) + '"')

        def unquoted():
            def pred(c):
                return not (c == '#' or c.isspace())
            return self.take_while(pred) if pred(self.peek()) else self.quit()

        def attribute():
            return self.take_while(lambda c: c == '_' or c.isalnum())

        def blank():
            return self.take_while(lambda c: c in [' ', '\t'])

        def eol():
            return self.take_exact('\n')

        def blank_eol():
            return blank() + eol()

        def comment():
            return self.Comment.from_str(
                blank() + self.take_exact('#')
                        + self.take_while(lambda c: c != '\n')
                        + eol()
            )

        def pair():
            return self.Pair.from_args(
                self.one_of(lambda: blank() + self.take_exact('export') + blank(),
                            blank),
                attribute(),
                self.take_exact('='),
                self.one_of(single_quoted,
                            double_quoted,
                            unquoted,
                            blank),
                self.one_of(comment,
                            blank_eol,
                            blank)
            )

        return self.Sequence.from_args(
            *(self.zero_or_more(lambda: self.one_of(pair,
                                                    comment,
                                                    blank_eol)))
        )

    def __init__(self, inp):
        super().__init__(inp)

    def render(self, node=None):
        acc = ''
        for v in (node or self.parsed):
            if isinstance(v, str):
                acc += v
            elif isinstance(v, self.Pair):
                acc += ''.join(v)
            else:
                raise self.InvalidTree
        return acc

    def put(self, path, value):
        atrb, atrb_i, _, _ = self._ypath(path, wildcards=False)
        s = self._searchable()

        # add a new pair directly at the root level
        if s.get(atrb) is None or (atrb_i is not None and atrb_i == 0):
            self.parsed.append(self.Pair.from_args(
                '', atrb, '=', str(value), '\n'
            ))
            return

        # require paths to be unequivocal
        if atrb_i is None and len(s[atrb]) > 1:
            raise self.AmbiguousMatch

        # fail when nothing found
        try:
            s = s[atrb][0 if atrb_i is None else (atrb_i - 1)]
        except (KeyError, IndexError):
            raise self.EmptyMatch

        # the pattern must resolve into a pair
        if not isinstance(s, self.Pair):
            raise self.InvalidPath

        # update the value (root level)
        s[3] = str(value)
        return

    def drop(self, path, value=None):
        atrb, atrb_i, _, _ = self._ypath(path, wildcards=True)
        def recurse(node):
            if isinstance(node, self.Pair) and (value is None or node[3] == str(value)):
                for i, x in enumerate(self.parsed):
                    if id(x) == id(node):
                        self.parsed.pop(i)
                        break
            elif isinstance(node, self.Sequence):
                for v in node:
                    recurse(v)
            elif isinstance(node, self.Lookup):
                for v in node.values():
                    recurse(v)
        recurse(self._filtered(patterns=[atrb, None], indices=[atrb_i, None]))

    def _ypath(self, path, wildcards=True):
        if isinstance(path, list):
            path = '/'.join(path)
        wild = '*' if wildcards else ''
        regx = rf'''(?x)
            ^
            ( [A-Za-z0-9_{wild}]+ )
            (?:
                \[ ( [0-9]* ) \]
            )?
            $
        '''
        m = re.match(regx, path)
        if m is None:
            raise self.InvalidPath

        atrb   = m[1]
        atrb_i = None if len(m[2] or '') == 0 else int(m[2])
        if atrb is None or (atrb_i is not None and int(atrb_i) < 0):
            raise self.InvalidPath

        return atrb, atrb_i, None, None

    def _searchable(self, node=None):
        def recurse(node, index):
            if isinstance(node, self.Pair):
                node.setm('_index_', index)
            elif isinstance(node, self.Sequence):
                for i, v in enumerate(node):
                    recurse(v, (i + 1) if (len(node) > 1) else None)
            elif isinstance(node, self.Lookup):
                node.setm('_index_', index)
                for v in node.values():
                    recurse(v, None)
        acc = self.Lookup()
        for v in (node or self.parsed):
            if isinstance(v, self.Pair):
                acc[v[1]] = acc.get(v[1], self.Sequence())
                acc[v[1]].append(v)
        recurse(acc, None)
        return acc


class YamlParser(ParserBase):
    def parser_proc(self):
        raise NotImplementedError

    def __init__(self, inp):
        super().__init__(inp)
        from ruamel.yaml import YAML
        self.yaml = YAML(typ='rt', pure=True)
        self.yaml.preserve_quotes = True

    def parse(self):
        self.parsed = self.yaml.load(self._inp)
        return self.parsed

    def render(self, node=None):
        b = io.BytesIO()
        self.yaml.dump(self.parsed, b)
        return b.getvalue().decode('utf-8')

    def match(self, path, value=None):
        raise NotImplementedError

    def get(self, path):
        rest = self._ypath(path, wildcards=None)
        v = self.parsed
        for k in rest:
            if isinstance(k, str):
                if not isinstance(v, dict):
                    return []
                try:
                    v = v[k]
                except KeyError:
                    return []
            elif isinstance(k, int):
                if not isinstance(v, list):
                    return []
                if k >= 1:
                    try:
                        v = v[k - 1]
                    except IndexError:
                        return []
                else:
                    raise self.InvalidPath
            else:
                raise self.InvalidPath
        return [v]

    def put(self, path, value):
        rest = self._ypath(path, wildcards=None)
        last = rest[-1]
        # a s d f g _    a s d f g     v      v      v      v      v
        #             =>           => (a, s) (s, d) (d, f) (f, g) (g, h)
        # _ s d f g h    s d f g h        ^      ^      ^      ^      ^
        v = self.parsed
        for (p, n) in zip(rest[:-1], rest[+1:]):
            if isinstance(p, str):
                if not isinstance(v, dict):
                    raise self.EmptyMatch
                try:
                    v = v[p]
                except KeyError:
                    if isinstance(n, str):
                        v[p] = dict()
                        v = v[p]
                    elif isinstance(n, int):
                        v[p] = list()
                        v = v[p]
                    else:
                        raise self.InvalidPath
            elif isinstance(p, int):
                if not isinstance(v, list):
                    raise self.EmptyMatch
                if p >= 1:
                    try:
                        v = v[p - 1]
                    except IndexError:
                        raise self.EmptyMatch
                elif p == 0:
                    if isinstance(n, str):
                        t = dict()
                        v.append(t)
                        v = t
                    elif isinstance(n, int):
                        t = list()
                        v.append(t)
                        v = t
                    else:
                        raise self.InvalidPath
                else:
                    raise self.InvalidPath
            else:
                raise self.InvalidPath
        # set the final value
        if isinstance(last, str):
            if not isinstance(v, dict):
                raise self.EmptyMatch
            v[last] = value
        elif isinstance(last, int):
            if not isinstance(v, list):
                raise self.EmptyMatch
            if last >= 1:
                try:
                    v[last - 1] = value
                except IndexError:
                    raise self.EmptyMatch
            elif last == 0:
                v.append(value)
            else:
                raise self.InvalidPath
        else:
            raise self.InvalidPath

    def drop(self, path, value=None):
        if value is not None:
            raise NotImplementedError
        rest = self._ypath(path, wildcards=None)
        last = rest.pop()
        v = self.parsed
        for k in rest:
            if isinstance(k, str):
                if not isinstance(v, dict):
                    return []
                try:
                    v = v[k]
                except KeyError:
                    raise self.EmptyMatch
            elif isinstance(k, int):
                if not isinstance(v, list):
                    return []
                if k >= 1:
                    try:
                        v = v[k - 1]
                    except IndexError:
                        raise self.EmptyMatch
                else:
                    raise self.InvalidPath
            else:
                raise self.InvalidPath
        # remove the final key/index
        if isinstance(last, str):
            if not isinstance(v, dict):
                raise self.EmptyMatch
            try:
                del v[last]
            except KeyError:
                raise self.EmptyMatch
        elif isinstance(last, int):
            if not isinstance(v, list):
                raise self.EmptyMatch
            if last >= 1:
                try:
                    del v[last - 1]
                except IndexError:
                    raise self.EmptyMatch
            else:
                raise self.InvalidPath
        else:
            raise self.InvalidPath

    def _ypath(self, path, wildcards=True):
        if wildcards is not None:
            raise NotImplementedError
        if not isinstance(path, list) or not path:
            raise self.InvalidPath
        return path

    def _searchable(self, node=None):
        raise NotImplementedError

    def _filtered(self, node=None, patterns=None, indices=None):
        raise NotImplementedError
