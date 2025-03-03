import requests_mock
from click.testing import CliRunner

from . import BaseCMLTest
from .mocks.github import MockGitHub


class Tests(BaseCMLTest):
    def test_virl_pull(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            topo_url = "https://raw.githubusercontent.com/"
            topo_url += "foo/bar/main/topology.yaml"
            m.get(topo_url, json=MockGitHub.get_topology)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["pull", "foo/bar"])
            self.assertEqual(0, result.exit_code)

    def test_virl_pull_invalid_repo(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            topo_url = "https://raw.githubusercontent.com/"
            topo_url += "doesnt/exist/main/topology.yaml"
            m.get(topo_url, status_code=400)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["pull", "doesnt/exist"])
            expected = (
                "Pulling topology.yaml from doesnt/exist on branch main\nError pulling topology.yaml from doesnt/exist on branch "
                "main - repo, file, or branch not found\n"
            )
            self.assertEqual(result.output, expected)
