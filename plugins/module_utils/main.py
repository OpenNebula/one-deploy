# -*- coding: utf-8 -*-
# Copyright: OpenNebula Project, OpenNebula Systems
# Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)


# EXAMPLES:
# '10.11.12.13' -> '02:01:0a:0b:0c:0d'
def ipv4_mac(ipv4, fmt='02:01:%02x:%02x:%02x:%02x'):
    """Converts IPv4 (string) into MAC."""

    import ipaddress

    return fmt % tuple(ipaddress.IPv4Address(ipv4).packed)


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


def flatten(to_flatten, extract=False):
    """Flattens nested lists (with optional value extraction)."""

    def recurse(to_flatten):
        return sum(map(recurse, to_flatten), []) if isinstance(to_flatten, list) else [to_flatten]

    value = recurse(to_flatten)

    if extract and len(value) == 1:
        return value[0]

    return value


def to_one(to_render):
    """Converts dictionary to OpenNebula template."""

    def recurse(to_render):
        for key, value in sorted(to_render.items()):
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


def get_one(params):
    """Establishes a connection to OpenNebula."""

    if params.get("auth") is None:
        return

    if params["auth"].get("host") is None \
    or params["auth"].get("user") is None \
    or params["auth"].get("pswd") is None:
        return

    auth = params["auth"]

    from pyone import OneServer

    return OneServer(
        auth["host"],
        session="{user:s}:{pswd:s}".format(**auth),
    )


def get_vm(params, one=None):
    """Finds a VM by name."""

    if params.get("name") is None:
        return

    pool = (one or get_one(params)).vmpool.info(-1, -1, -1, -1)

    return next(
        ( vm
          for vm in pool.VM
          if vm.NAME == params["name"] ),
        None
    )


def get_template(params, one=None):
    """Finds a VM template by name."""

    if params.get("template") is None or params["template"].get("name") is None:
        return

    pool = (one or get_one(params)).templatepool.info(-1, -1, -1)

    return next(
        ( template
          for template in pool.VMTEMPLATE
          if template.NAME == params["template"]["name"] ),
        None
    )


def get_datablocks(params, one=None):
    """Finds datablocks by prefix."""

    if params.get("name") is None:
        return

    pool = (one or get_one(params)).imagepool.info(-1, -1, -1)

    return list(
        image
        for image in pool.IMAGE
        if image.TYPE == 2
        if image.NAME.startswith("{name:s}-".format(**params))
    )
