# -*- coding: utf-8 -*-
# Copyright: OpenNebula Project, OpenNebula Systems
# Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)


# EXAMPLES:
# '0-2,3,5-7' -> '0,1,2,3,5,6,7'
def explode_ranges(ranges, split=False):
    """Converts ranges to indices."""

    import re

    if not ranges:
        return [] if split else ''

    def g():
        for z in re.split('[, ]', ranges):
            y = z.split('-')

            if len(y) > 0:
                if len(y) == 1:
                    yield str(y[0])
                else:
                    for x in range(int(y[0]), int(y[1]) + 1):
                        yield str(x)

    return list(g()) if split else ','.join(g())


# EXAMPLES:
# '0,1,2,3,5,6,7' -> '0-3,5-7'
def implode_ranges(indices, split=False):
    """Converts indices to ranges."""

    import re

    if not indices:
        return [] if split else ''

    if isinstance(indices, list):
        indices = ','.join(indices)

    def index_or_range(y):
        return str(y[0]) if len(y) == 1 else str(y[0]) + '-' + str(y[-1])

    def g():
        y = []

        for x in re.split('[, ]', indices):
            if len(y) > 0:
                if y[-1] + 1 != int(x):
                    yield index_or_range(y)
                    y.clear()

            y.append(int(x))

        yield index_or_range(y)

    return list(g()) if split else ','.join(g())


# EXAMPLES:
# '0xc06' -> '1,2,10,11'
# '0b1100_0000_0110' -> '1,2,10,11'
def explode_bitmask(mask, split=False):
    """Converts a non-negative bitmask to set-bit indices."""

    bits = reversed('{:b}'.format(int(mask, 0)))

    indices = [
        str(i)
        for i, b in enumerate(bits)
        if b == '1'
    ]

    return indices if split else ','.join(indices)


# EXAMPLES:
# '11,1,2,10' -> '0xc06'
# '11,1-2,10' -> '0xc06'
def implode_bitmask(indices, base=16):
    """Converts bit indices to a bitmask string."""

    if isinstance(indices, str):
        indices = explode_ranges(indices, split=True) if indices else []

    mask = sum(
        1 << i
        for i in {int(i) for i in indices}
    )

    base = {2: 'b', 8: 'o', 10: 'd', 16: 'x'}[base]

    return format(mask, '#' + base)


# EXAMPLES:
# '10.11.12.13' -> '02:01:0a:0b:0c:0d'
def ipv4_mac(ipv4, fmt='02:01:%02x:%02x:%02x:%02x'):
    """Converts IPv4 (string) into MAC."""

    import ipaddress

    return fmt % tuple(ipaddress.IPv4Address(ipv4).packed)


# NOTE: It does not validate character classes or character count!
# EXAMPLES:
# pci -> match_address('0000:0*:00.*', sep='[:.]')
# mac -> match_address('52:54:*:*:*:0*', sep='[:]')
def match_address(address, pattern, sep=None):
    """Tests if a split string matches a set of simple glob patterns."""

    import fnmatch
    import re

    # In case no separator is provided simply match the whole string.
    if sep is None:
        return fnmatch.fnmatch(address, pattern)

    # Make sure both address and pattern contain identical separators.
    if re.findall(sep, address) != re.findall(sep, pattern):
        return False

    # Try matching (glob) each segment separately.
    for x, y in zip(re.split(sep, address), re.split(sep, pattern)):
        if not fnmatch.fnmatch(x, y):
            return False

    return True


def to_actions(config):
    """Converts {'A/B': value} dictionary to cfgtool actions (None value = drop)."""

    actions = []

    for key, value in dict(config).items():
        path = str(key).split('/')

        if value is None:
            actions.append({'drop': {'path': path}})
            # NOTE: The parser drops attributes only, a whole vector is removed
            #       once emptied (KEY/*), both are no-ops when nothing matches.
            if len(path) == 1:
                actions.append({'drop': {'path': path + ['*']}})
        else:
            actions.append({'put': {'path': path, 'value': value}})

    return actions


def to_one(to_render):
    """Converts dictionary to OpenNebula template (None value = drop)."""

    def recurse(to_render):
        for key, value in sorted(to_render.items()):
            if value is None:
                continue

            if isinstance(value, dict):
                yield '{0:}=[{1:}]'.format(key, ','.join(recurse(value)))
                continue

            if isinstance(value, list):
                for item in value:
                    yield '{0:}=[{1:}]'.format(key, ','.join(recurse(item)))
                continue

            if isinstance(value, str):
                yield '{0:}="{1:}"'.format(key, value.replace('"', '\\"'))
            else:
                yield '{0:}="{1:}"'.format(key, value)

    return '\n'.join(recurse(to_render))
