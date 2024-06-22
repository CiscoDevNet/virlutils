import requests_mock
from click.testing import CliRunner

from . import BaseCMLTest
from .mocks.nso import MockNSOServer


class Tests(BaseCMLTest):
    def test_virl_generate_nso(self):
        data = {
            "n0": {"name": "Lab Net", "interfaces": {}},
            "n1": {
                "name": "rtr-1",
                "interfaces": {
                    "52:54:00:1f:27:95": {"id": "i2", "ip4": ["10.1.1.1"], "ip6": ["fc00::1"], "label": "MgmtEth0/RP0/CPU0/0"},
                    "52:54:00:06:b7:7c": {"id": "i3", "ip4": [], "ip6": [], "label": "donotuse1"},
                    "52:54:00:16:ef:1a": {"id": "i4", "ip4": [], "ip6": [], "label": "donotuse2"},
                    "52:54:00:00:73:28": {"id": "i5", "ip4": [], "ip6": [], "label": "GigabitEthernet0/0/0/0"},
                },
            },
        }
        with self.get_context() as m, requests_mock.mock() as nso_mock:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            self.setup_func("get", m, "labs/{}/layer3_addresses".format(self.get_test_id()), json=data)
            self.setup_func("get", m, "labs/{}/nodes/n0/layer3_addresses".format(self.get_test_id()), json=data["n0"])
            self.setup_func("get", m, "labs/{}/nodes/n1/layer3_addresses".format(self.get_test_id()), json=data["n1"])

            # mock the responses we expect from NSO
            devices_url = "http://localhost:8080/api/config/devices/"
            nso_mock.patch(devices_url, json=MockNSOServer.update_devices())
            sync_url = "http://localhost:8080/api/running/devices/"
            sync_url += "_operations/sync-from"
            nso_mock.post(sync_url, json=MockNSOServer.perform_sync_from())
            ned_url = "http://localhost:8080/api/config/devices/ned-ids/ned-id"
            nso_mock.get(ned_url, json=MockNSOServer.get_ned_list())
            module_url = "http://localhost:8080/api/config/modules-state/module"
            nso_mock.get(module_url, json=MockNSOServer.get_module_list())

            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["generate", "nso", "--syncfrom"])
            self.assertEqual(0, result.exit_code)
