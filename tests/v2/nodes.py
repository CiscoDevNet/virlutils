import os

from click.testing import CliRunner

from . import BaseCMLTest


class CMLNodesTest(BaseCMLTest):
    def test_cml_nodes(self):
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
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            self.setup_func("get", m, "labs/{}/layer3_addresses".format(self.get_test_id()), json=data)
            self.setup_func("get", m, "labs/{}/nodes/n0/layer3_addresses".format(self.get_test_id()), json=data["n0"])
            self.setup_func("get", m, "labs/{}/nodes/n1/layer3_addresses".format(self.get_test_id()), json=data["n1"])
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["nodes"])
            self.assertEqual(0, result.exit_code)

    def test_cml_nodes_no_lab(self):
        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["nodes"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("No current lab selected", result.output)

    def test_cml_nodes_bogus_lab(self):
        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        src_dir = os.path.realpath(".virl")
        with open(".virl/cached_cml_labs/123456", "w") as fd:
            fd.write("lab: bogus\n")

        os.symlink("{}/cached_cml_labs/123456".format(src_dir), "{}/current_cml_lab".format(src_dir))

        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["nodes"])
            os.remove(".virl/cached_cml_labs/123456")
            self.assertEqual(1, result.exit_code)
            self.assertIn("Lab 123456 is not running", result.output)
