from . import BaseCMLTest
from .mocks.github import MockGitHub
from click.testing import CliRunner
import requests_mock


class Tests(BaseCMLTest):
    def test_virl_pull(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            topo_url = "https://raw.githubusercontent.com/"
            topo_url += "foo/bar/master/topology.yaml"
            m.get(topo_url, json=MockGitHub.get_topology)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["pull", "foo/bar"])
            self.assertEqual(0, result.exit_code)

    def test_virl_pull_invalid_repo(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            topo_url = "https://raw.githubusercontent.com/"
            topo_url += "doesnt/exist/master/topology.yaml"
            m.get(topo_url, status_code=400)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["pull", "doesnt/exist"])
            expected = "Pulling from doesnt/exist on branch master\nError pulling " "doesnt/exist - repo or file not found\n"
            self.assertEqual(result.output, expected)
