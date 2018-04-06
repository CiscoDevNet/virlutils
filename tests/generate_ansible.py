from . import BaseTest
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl
# import filecmp


class Tests(BaseTest):

    def test_virl_generate_ansible_yaml(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            roster_url = 'http://localhost:19399/roster/rest'
            m.get(roster_url, json=self.mock_roster_response())
            export_url = 'http://localhost:19399/simengine/rest/export/'
            export_url += 'TEST_ENV?running-configs=config&updated=true'
            m.get(export_url, text=self.mock_export_response())
            interface_url = 'http://localhost:19399/simengine/rest/interfaces/'
            interface_url += 'TEST_ENV'
            m.get(interface_url, json=self.mock_interface_response())
            runner = CliRunner()
            result = runner.invoke(virl, ["generate", "ansible"])
            # same = filecmp.cmp('default_inventory.yaml',
            #                    'tests/static/ansible_yaml_inventory')
            # self.assertTrue(same)
            self.assertEqual(0, result.exit_code)

    def test_virl_generate_ansible_ini(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            roster_url = 'http://localhost:19399/roster/rest'
            m.get(roster_url, json=self.mock_roster_response())
            export_url = 'http://localhost:19399/simengine/rest/export/'
            export_url += 'TEST_ENV?running-configs=config&updated=true'
            m.get(export_url, text=self.mock_export_response())
            interface_url = 'http://localhost:19399/simengine/rest/interfaces/'
            interface_url += 'TEST_ENV'
            m.get(interface_url, json=self.mock_interface_response())
            runner = CliRunner()
            result = runner.invoke(virl, ["generate", "ansible",
                                          "--style", "ini"])
            # same = filecmp.cmp('default_inventory.ini',
            #                    'tests/static/ansible_ini_inventory')
            # self.assertTrue(same)
            self.assertEqual(0, result.exit_code)

    def mock_up_response(self):
        response = u'TEST_ENV'
        return response

    def mock_roster_response(self):
        response = {
            u'guest|TEST_ENV|virl|router1': {
                u'Status': u'ACTIVE',
                u'simLaunch': u'2018-04-06T02:57:15.217442',
                u'simID': u'virlutils_default_XzmcAm',
                u'NodeName': u'router1',
                u'simStatus': u'ACTIVE',
                u'simExpires': None,
                u'managementIP': u'172.16.30.121',
                u'managementProtocol': u'telnet',
                u'SimulationHost': u'10.10.10.170',
                u'NodeSubtype': u'IOSv',
                u'PortMonitor': 17029,
                u'Reachable': True,
                u'SerialPorts': 2,
                u'managementProxy': u'jumphost',
                u'VncConsole': False,
                u'PortConsole': 17028,
                u'Annotation': u'REACHABLE'
            },
            u'guest|TEST_ENV|virl|router2': {
                u'Status': u'ACTIVE',
                u'simLaunch': u'2018-04-06T02:57:15.217442',
                u'simID': u'virlutils_default_XzmcAm',
                u'NodeName': u'router2',
                u'simStatus': u'ACTIVE',
                u'simExpires': None,
                u'managementIP': u'172.16.30.122',
                u'managementProtocol': u'telnet',
                u'SimulationHost': u'10.10.10.170',
                u'NodeSubtype': u'IOSv',
                u'PortMonitor': 17030,
                u'Reachable': True,
                u'SerialPorts': 2,
                u'managementProxy': u'jumphost',
                u'VncConsole': False,
                u'PortConsole': 17027,
                u'Annotation': u'REACHABLE'
            }
        }
        return response

    def mock_interface_response(self):

        response = {
            "2nodes_default_ngTj03": {
                "router2": {
                    "0": {
                        "status": "UP",
                        "link-state": True,
                        "name": "GigabitEthernet0/1",
                        "hw-addr": "fa:16:3e:48:8e:c2",
                        "port-state": True,
                        "external-ip-address": None,
                        "ip-address": "10.255.0.6/30",
                        "external-port": None,
                        "network": "router1-to-router2"
                    },
                    "management": {
                        "status": "UP",
                        "link-state": True,
                        "name": "GigabitEthernet0/0",
                        "hw-addr": "5e:00:c0:01:00:00",
                        "port-state": True,
                        "external-ip-address": True,
                        "ip-address": "172.16.30.126/24",
                        "external-port": True,
                        "network": "flat"
                    }
                },
                "router1": {
                    "0": {
                        "status": "UP",
                        "link-state": True,
                        "name": "GigabitEthernet0/1",
                        "hw-addr": "fa:16:3e:95:f1:c5",
                        "port-state": True,
                        "external-ip-address": None,
                        "ip-address": "10.255.0.5/30",
                        "external-port": None,
                        "network": "router1-to-router2"
                    },
                    "management": {
                        "status": "UP",
                        "link-state": True,
                        "name": "GigabitEthernet0/0",
                        "hw-addr": "5e:00:c0:00:00:00",
                        "port-state": True,
                        "external-ip-address": None,
                        "ip-address": "172.16.30.125/24",
                        "external-port": None,
                        "network": "flat"
                    }
                }
            }
        }
        return response

    def mock_export_response(self):

        with open('tests/static/test_virl_data', 'r') as fh:
            virl_data = fh.read()
        return virl_data
