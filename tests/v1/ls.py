from . import BaseTest
from .mocks.api import MockVIRLServer
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl


class LsTest(BaseTest):

    def test_virl_ls_alL(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/simengine/rest/list',
                  json=MockVIRLServer.list_simulations())
            runner = CliRunner()
            result = runner.invoke(virl, ["ls", "--all"])
            self.assertEqual(0, result.exit_code)

    def test_virl_ls(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/simengine/rest/list',
                  json=MockVIRLServer.list_simulations())
            runner = CliRunner()
            result = runner.invoke(virl, ["ls"])
            self.assertEqual(0, result.exit_code)
