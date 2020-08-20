from . import BaseTest
from .mocks import MockVIRLServer
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class Tests(BaseTest):

    def test_virl_console_display(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/simengine/rest/serial_port/TEST_ENV',
                  json=MockVIRLServer.get_node_console())
            runner = CliRunner()
            result = runner.invoke(virl, ["console", "--display"])
            self.assertEqual(0, result.exit_code)

    @patch("virl.cli.console.commands.call", auto_spec=False)
    def test_virl_console_connect(self, call_mock):

        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/simengine/rest/serial_port/TEST_ENV',
                  json=MockVIRLServer.get_node_console())
            runner = CliRunner()
            runner.invoke(virl, ["console", "router1"])
            call_mock.assert_called_once_with(['telnet',
                                               u'10.94.241.194',
                                               u'17001'])

    @patch("virl.cli.console.commands.call", auto_spec=False)
    def test_virl_console_connect_env(self, call_mock):

        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/simengine/rest/serial_port/TEST_ENV',
                  json=MockVIRLServer.get_node_console())
            runner = CliRunner()
            runner.invoke(virl, ["console", "TEST_ENV", "router1"])
