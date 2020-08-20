from . import BaseTest
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl


class NodesTest(BaseTest):

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
                "Status": "BUILDING",
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
            },
            "guest|TEST_ENV|virl|router3": {
                "Status": "",
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
            },
            "guest|TEST_ENV|virl|mgmt-lxc": {
                "Status": "",
                "simLaunch": "2018-04-04T14:25:12.916689",
                "PortConsole": 17003,
                "NodeName": "router2",
                "simExpires": None,
                "managementIP": "2.2.2.2",
                "SerialPorts": 2,
                "SimulationHost": "5.5.5.5",
                "NodeSubtype": "LXC FLAT",
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

    def test_virl_nodes(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/roster/rest/',
                  json=self.mock_response())
            runner = CliRunner()
            result = runner.invoke(virl, ["nodes"])
            self.assertEqual(0, result.exit_code)

    def test_virl_nodes_in_env(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/roster/rest/',
                  json=self.mock_response())
            runner = CliRunner()
            result = runner.invoke(virl, ["nodes", "foo"])
            self.assertEqual(0, result.exit_code)
