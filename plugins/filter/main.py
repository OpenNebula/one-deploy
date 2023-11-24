from ansible_collections.opennebula.deploy.plugins.module_utils.main import to_one


class FilterModule(object):

    def filters(self):
        return dict(to_one=to_one)
