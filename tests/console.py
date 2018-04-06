from . import BaseTest
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class Tests(BaseTest):

    def mock_response(self):
        sim_response = {
            u'router2': u'10.94.241.194:17002',
            u'router1': u'10.94.241.194:17001'
        }
        return sim_response

    def test_virl_console_display(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/simengine/rest/serial_port/TEST_ENV',
                  json=self.mock_response())
            runner = CliRunner()
            result = runner.invoke(virl, ["console", "--display"])
            self.assertEqual(0, result.exit_code)

    @patch("virl.cli.console.commands.call", auto_spec=False)
    def test_virl_console_connect(self, call_mock):

        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/simengine/rest/serial_port/TEST_ENV',
                  json=self.mock_response())
            runner = CliRunner()
            runner.invoke(virl, ["console", "router1"])
            call_mock.assert_called_once_with(['telnet',
                                               u'10.94.241.194',
                                               u'17001'])
    # self.assertEqual(0, result.exit_code)
