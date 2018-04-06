
class MockGitHub:

    @classmethod
    def get_topology(cls):
        with open('tests/static/fake_repo_topology.virl', 'r') as fh:
            response = fh.read()
        return response
