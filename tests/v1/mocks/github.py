
class MockGitHub:

    @classmethod
    def get_topology(cls):
        with open('tests/v1/static/fake_repo_topology.virl', 'r') as fh:
            response = fh.read()
        return response
