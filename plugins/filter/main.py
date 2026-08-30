from ansible_collections.opennebula.deploy.plugins.module_utils.main import (
    ipv4_mac,
    explode_ranges,
    implode_ranges,
    to_one,
)


class FilterModule(object):

    def filters(self):
        return dict(
            ipv4_mac=ipv4_mac,
            explode_ranges=explode_ranges,
            implode_ranges=implode_ranges,
            to_one=to_one,
        )
