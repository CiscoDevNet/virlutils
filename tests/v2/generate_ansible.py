from click.testing import CliRunner

from . import BaseCMLTest


class Tests(BaseCMLTest):
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

    def test_virl_generate_ansible_yaml(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            self.setup_func("get", m, "labs/{}/layer3_addresses".format(self.get_test_id()), json=self.data)
            self.setup_func("get", m, "labs/{}/nodes/n0/layer3_addresses".format(self.get_test_id()), json=self.data["n0"])
            self.setup_func("get", m, "labs/{}/nodes/n1/layer3_addresses".format(self.get_test_id()), json=self.data["n1"])
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["generate", "ansible"])
            self.assertEqual(0, result.exit_code)

    def test_virl_generate_ansible_topology_yaml(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            self.setup_func("get", m, "labs/{}/layer3_addresses".format(self.get_test_id()), json=self.data)
            self.setup_func("get", m, "labs/{}/nodes/n0/layer3_addresses".format(self.get_test_id()), json=self.data["n0"])
            self.setup_func("get", m, "labs/{}/nodes/n1/layer3_addresses".format(self.get_test_id()), json=self.data["n1"])
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["generate", "ansible", "-o", "topology.yaml"])
            self.assertEqual(0, result.exit_code)

    def test_virl_generate_ansible_ini(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            self.setup_func("get", m, "labs/{}/layer3_addresses".format(self.get_test_id()), json=self.data)
            self.setup_func("get", m, "labs/{}/nodes/n0/layer3_addresses".format(self.get_test_id()), json=self.data["n0"])
            self.setup_func("get", m, "labs/{}/nodes/n1/layer3_addresses".format(self.get_test_id()), json=self.data["n1"])
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["generate", "ansible", "--style", "ini"])
            self.assertEqual(0, result.exit_code)
