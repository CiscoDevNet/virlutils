from . import BaseTest
from .mocks import MockVIRLServer
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl

# import filecmp


class Tests(BaseTest):
    def test_virl_generate_pyats(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            roster_url = "http://localhost:19399/roster/rest/"
            m.get(roster_url, json=MockVIRLServer.get_sim_roster())
            export_url = "http://localhost:19399/simengine/rest/export/"
            export_url += "TEST_ENV?running-configs=config&updated=true"
            m.get(export_url, text=MockVIRLServer.export())
            interface_url = "http://localhost:19399/simengine/rest/interfaces/"
            interface_url += "TEST_ENV"
            m.get(interface_url, json=MockVIRLServer.get_interfaces())
            runner = CliRunner()
            result = runner.invoke(virl, ["generate", "pyats"])
            # same = filecmp.cmp('default_testbed.yaml',
            #                    'tests/static/pyats_testbed')
            # self.assertTrue(same)
            self.assertEqual(0, result.exit_code)
