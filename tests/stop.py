from . import BaseTest
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl


class Tests(BaseTest):

    def test_virl_stop(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            down_url = 'http://localhost:19399/simengine/rest/stop/TEST_ENV'
            m.get(down_url, json=self.mock_down_response())
            runner = CliRunner()
            runner.invoke(virl, ["stop", "router1"])

    def mock_down_response(self):
        response = 'SUCCESS'
        return response
