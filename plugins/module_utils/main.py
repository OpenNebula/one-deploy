# -*- coding: utf-8 -*-
# Copyright: OpenNebula Project, OpenNebula Systems
# Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)


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
