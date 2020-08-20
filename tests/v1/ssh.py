from . import BaseTest
from .mocks.api import MockVIRLServer
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class Tests(BaseTest):

    @patch("virl.cli.ssh.commands.call", auto_spec=False)
    def test_virl_ssh(self, call_mock):

        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/roster/rest/',
                  json=MockVIRLServer.get_sim_roster())
            runner = CliRunner()
            runner.invoke(virl, ["ssh", "router1"])
            call_mock.assert_called_once_with(['ssh', 'cisco@1.1.1.1'])

    @patch("virl.cli.ssh.commands.call", auto_spec=False)
    def test_virl_ssh_proxy(self, call_mock):

        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/roster/rest/',
                  json=MockVIRLServer.get_sim_roster())
            runner = CliRunner()
            runner.invoke(virl, ["ssh", "via-lxc"])
            cmd = 'ssh -o "ProxyCommand ssh -W %h:%p' \
                  ' guest@FAKE_EXTERNAL_IP" cisco@10.5.5.5'
            call_mock.assert_called_once_with(cmd, shell=True)

    @patch("virl.cli.ssh.commands.call", auto_spec=False)
    def test_virl_ssh_env(self, call_mock):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/roster/rest/',
                  json=MockVIRLServer.get_sim_roster())
            runner = CliRunner()
            runner.invoke(virl, ["ssh", "TEST_ENV", "router1"])
