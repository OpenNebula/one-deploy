from ansible_collections.opennebula.deploy.plugins.module_utils.main import (
    ipv4_mac,
    to_one,
    to_actions,
)


class FilterModule(object):

    def filters(self):
        return dict(
            ipv4_mac=ipv4_mac,
            to_one=to_one,
            to_actions=to_actions,
        )
