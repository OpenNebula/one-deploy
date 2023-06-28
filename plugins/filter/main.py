#!/usr/bin/env python3

class FilterModule(object):
    def filters(self):
        return {
            'to_one': to_one,
        }

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
