from . import BaseTest
from .mocks import MockVIRLServer
from .mocks.nso import MockNSOServer
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl


class Tests(BaseTest):
    def test_virl_generate_nso(self):
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

            # mock the responses we expect from NSO
            devices_url = "http://localhost:8080/api/config/devices/"
            m.patch(devices_url, json=MockNSOServer.update_devices())
            sync_url = "http://localhost:8080/api/running/devices/"
            sync_url += "_operations/sync-from"
            m.post(sync_url, json=MockNSOServer.perform_sync_from())
            ned_url = "http://localhost:8080/api/config/devices/ned-ids/ned-id"
            m.get(ned_url, json=MockNSOServer.get_ned_list())
            module_url = "http://localhost:8080/api/config/modules-state/module"
            m.get(module_url, json=MockNSOServer.get_module_list())
            runner = CliRunner()
            result = runner.invoke(virl, ["generate", "nso", "--syncfrom"])
            self.assertEqual(0, result.exit_code)
