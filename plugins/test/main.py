from ansible_collections.opennebula.deploy.plugins.module_utils.main import match_address


class TestModule(object):
    def tests(self):
        return dict(match_address=match_address)
