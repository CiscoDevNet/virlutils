from . import BaseTest
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class Tests(BaseTest):

    def test_virl_start(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            down_url = 'http://localhost:19399/simengine/rest/start/TEST_ENV'
            m.get(down_url, json=self.mock_down_response())
            runner = CliRunner()
            runner.invoke(virl, ["start", "router1"])

    def test_virl_start_env(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            down_url = 'http://localhost:19399/simengine/rest/start/foo_env'
            m.get(down_url, json=self.mock_down_response())
            runner = CliRunner()
            runner.invoke(virl, ["start", "foo_env", "router1"])

    @patch("virl.cli.start.commands.call", auto_spec=False)
    def test_virl_start_no_node_given(self, call_mock):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            down_url = 'http://localhost:19399/simengine/rest/stop/TEST_ENV'
            m.get(down_url, json=self.mock_down_response())
            runner = CliRunner()
            runner.invoke(virl, ["start"])
            call_mock.assert_called_with(['virl', 'start', '--help'])

    def mock_down_response(self):
        response = 'SUCCESS'
        return response
