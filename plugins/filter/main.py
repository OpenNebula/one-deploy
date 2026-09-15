from ansible_collections.opennebula.deploy.plugins.module_utils.main import to_one, to_actions


class FilterModule(object):

    def filters(self):
        return dict(to_one=to_one, to_actions=to_actions)
