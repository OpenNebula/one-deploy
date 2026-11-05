from ansible_collections.opennebula.deploy.plugins.module_utils.main import (
    explode_bitmask,
    explode_ranges,
    implode_bitmask,
    implode_ranges,
    ipv4_mac,
    to_actions,
    to_one,
)


class FilterModule(object):

    def filters(self):
        return dict(
            explode_bitmask=explode_bitmask,
            explode_ranges=explode_ranges,
            implode_bitmask=implode_bitmask,
            implode_ranges=implode_ranges,
            ipv4_mac=ipv4_mac,
            to_actions=to_actions,
            to_one=to_one,
        )
