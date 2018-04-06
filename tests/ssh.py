from . import BaseTest
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
            m.get('http://localhost:19399/roster/rest',
                  json=self.mock_response())
            runner = CliRunner()
            runner.invoke(virl, ["ssh", "router1"])
            call_mock.assert_called_once_with(['ssh', 'cisco@1.1.1.1'])

    @patch("virl.cli.ssh.commands.call", auto_spec=False)
    def test_virl_ssh_env(self, call_mock):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/roster/rest',
                  json=self.mock_response())
            runner = CliRunner()
            result = runner.invoke(virl, ["ssh", "TEST_ENV", "router1"])
            
    # self.assertEqual(0, result.exit_code)
    def mock_response(self):
        sim_response = {
            "guest|TEST_ENV|virl|router1": {
                "Status": "ACTIVE",
                "simLaunch": "2018-04-04T14:25:12.916689",
                "PortConsole": 17000,
                "NodeName": "router1",
                "simExpires": None,
                "managementIP": "1.1.1.1",
                "SerialPorts": 2,
                "SimulationHost": "5.5.5.5",
                "NodeSubtype": "IOSv",
                "simStatus": "ACTIVE",
                "Reachable": True,
                "PortMonitor": 17001,
                "managementProtocol": "telnet",
                "managementProxy": "jumphost",
                "VncConsole": False,
                "simID": "TEST_ENV",
                "Annotation": "REACHABLE"
            },
            "guest|TEST_ENV|virl|router2": {
                "Status": "ACTIVE",
                "simLaunch": "2018-04-04T14:25:12.916689",
                "PortConsole": 17003,
                "NodeName": "router2",
                "simExpires": None,
                "managementIP": "2.2.2.2",
                "SerialPorts": 2,
                "SimulationHost": "5.5.5.5",
                "NodeSubtype": "IOSv",
                "simStatus": "ACTIVE",
                "Reachable": True,
                "PortMonitor": 17004,
                "managementProtocol": "telnet",
                "managementProxy": "jumphost",
                "VncConsole": False,
                "simID": "TEST_ENV",
                "Annotation": "REACHABLE"
            }
        }
        return sim_response
