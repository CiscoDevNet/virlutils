class MockGitHub(object):
    @staticmethod
    def get_topology(req, ctx=None):
        with open("tests/v2/static/fake_repo_topology.yaml", "r") as fh:
            response = fh.read()
        return response
