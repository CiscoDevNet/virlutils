from . import BaseTest
from .mocks.github import MockGitHub
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl


class Tests(BaseTest):

    def test_virl_pull(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.

            topo_url = 'https://raw.githubusercontent.com/'
            topo_url += 'foo/bar/master/topology.virl'
            m.get(topo_url, json=MockGitHub.get_topology())
            runner = CliRunner()
            result = runner.invoke(virl, ["pull", "foo/bar"])
            self.assertEqual(0, result.exit_code)
