from . import BaseTest
from .mocks.api import MockVIRLServer
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class TelnetTests(BaseTest):

    @patch("virl.cli.telnet.commands.call", auto_spec=False)
    def test_virl_telnet(self, call_mock):

        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/roster/rest/',
                  json=MockVIRLServer.get_sim_roster())
            runner = CliRunner()
            runner.invoke(virl, ["telnet", "router1"])
            call_mock.assert_called_once_with(['telnet',
                                               u'1.1.1.1'])

    @patch("virl.cli.telnet.commands.call", auto_spec=False)
    def test_virl_telnet_proxy(self, call_mock):

        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/roster/rest/',
                  json=MockVIRLServer.get_sim_roster())
            runner = CliRunner()
            runner.invoke(virl, ["telnet", "via-lxc"])
            cmd = 'ssh -t guest@FAKE_EXTERNAL_IP "telnet 10.5.5.5"'
            call_mock.assert_called_once_with(cmd, shell=True)

    @patch("virl.cli.telnet.commands.call", auto_spec=False)
    def test_virl_telnet_env(self, call_mock):

        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/roster/rest/',
                  json=MockVIRLServer.get_sim_roster())
            runner = CliRunner()
            runner.invoke(virl, ["telnet", "TEST_ENV", "router1"])

    @patch("virl.cli.telnet.commands.call",
           auto_spec=False,
           side_effect=KeyError)
    def test_virl_telnet_raises_KeyError(self, call_mock):

        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/roster/rest/',
                  json=MockVIRLServer.get_sim_roster())
            runner = CliRunner()
            runner.invoke(virl, ["telnet", "router1"])
            call_mock.assert_called_once_with(['telnet',
                                               u'1.1.1.1'])

    @patch("virl.cli.telnet.commands.call",
           auto_spec=False,
           side_effect=AttributeError)
    def test_virl_telnet_raises_AttributError(self, call_mock):

        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/roster/rest/',
                  json=MockVIRLServer.get_sim_roster())
            runner = CliRunner()
            runner.invoke(virl, ["telnet", "router1"])
            call_mock.assert_called_once_with(['telnet',
                                               u'1.1.1.1'])
