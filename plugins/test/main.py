#!/usr/bin/env python

import fnmatch
import re

class TestModule(object):
    def tests(self):
        return {
            'match_address': self.match_address,
        }

    # NOTE: It does not validate character classes or character count!
    # EXAMPLES:
    # pci -> match_address('0000:0*:00.*', sep='[:.]')
    # mac -> match_address('52:54:*:*:*:0*', sep='[:]')
    def match_address(self, address, pattern, sep=None):
        """Tests if a split string matches a set of simple glob patterns."""

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
