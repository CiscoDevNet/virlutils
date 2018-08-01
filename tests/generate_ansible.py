from . import BaseTest
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl
from .mocks import MockVIRLServer
# import filecmp


class Tests(BaseTest):

    def test_virl_generate_ansible_yaml(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            roster_url = 'http://localhost:19399/roster/rest/'
            m.get(roster_url, json=MockVIRLServer.get_sim_roster())
            export_url = 'http://localhost:19399/simengine/rest/export/'
            export_url += 'TEST_ENV?running-configs=config&updated=true'
            m.get(export_url, text=MockVIRLServer.export())
            interface_url = 'http://localhost:19399/simengine/rest/interfaces/'
            interface_url += 'TEST_ENV'
            m.get(interface_url, json=MockVIRLServer.get_interfaces())
            runner = CliRunner()
            result = runner.invoke(virl, ["generate", "ansible"])
            # same = filecmp.cmp('default_inventory.yaml',
            #                    'tests/static/ansible_yaml_inventory')
            # self.assertTrue(same)
            self.assertEqual(0, result.exit_code)

    def test_virl_generate_ansible_ini(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            roster_url = 'http://localhost:19399/roster/rest/'
            m.get(roster_url, json=MockVIRLServer.get_sim_roster())
            export_url = 'http://localhost:19399/simengine/rest/export/'
            export_url += 'TEST_ENV?running-configs=config&updated=true'
            m.get(export_url, text=MockVIRLServer.export())
            interface_url = 'http://localhost:19399/simengine/rest/interfaces/'
            interface_url += 'TEST_ENV'
            m.get(interface_url, json=MockVIRLServer.get_interfaces())
            runner = CliRunner()
            result = runner.invoke(virl, ["generate", "ansible",
                                          "--style", "ini"])
            # same = filecmp.cmp('default_inventory.ini',
            #                    'tests/static/ansible_ini_inventory')
            # self.assertTrue(same)
            self.assertEqual(0, result.exit_code)
