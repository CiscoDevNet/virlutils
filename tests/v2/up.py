import os

from click.testing import CliRunner

from . import BaseCMLTest
from .mocks.github import MockGitHub  # noqa

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # noqa


class TestCMLUp(BaseCMLTest):
    def get_up_id(self):
        return "7e5712"

    def setup_mocks(self, m):
        super().setup_mocks(m)
        self.setup_func("post", m, "import?title=Fake%20Lab", json={"id": self.get_up_id()})
        self.setup_func(
            "get", m, "labs/{}/topology?exclude_configurations=False".format(self.get_up_id()), json=TestCMLUp.get_fake_topology
        )
        self.setup_func("get", m, "labs/{}/state".format(self.get_up_id()), json="STOPPED")
        self.setup_func("put", m, "labs/{}/start".format(self.get_up_id()), json="STARTED")
        self.setup_func("put", m, "labs/{}/start".format(self.get_alt_id()), json="STARTED")
        self.setup_func("get", m, "labs/{}/download".format(self.get_up_id()), text=MockGitHub.get_topology)
        self.setup_func("get", m, "labs/{}/lab_element_state".format(self.get_up_id()), json=TestCMLUp.get_fake_element_state)

    @staticmethod
    def get_fake_element_state(req, ctx=None):
        response = {
            "nodes": {"n0": "BOOTED", "n1": "BOOTED"},
            "links": {"l0": "STARTED"},
            "interfaces": {"i0": "STARTED", "i1": "STARTED", "i2": "STARTED", "i3": "STARTED", "i4": "STARTED", "i5": "STARTED"},
        }
        return response

    @staticmethod
    def get_fake_topology(req, ctx=None):
        response = {
            "nodes": [
                {
                    "id": "n0",
                    "data": {
                        "node_definition": "nxosv",
                        "image_definition": "nxosv-7-3-0",
                        "label": "bt-test-sw",
                        "configuration": "hostname inserthostname_here",
                        "x": -350,
                        "y": 0,
                        "state": "STOPPED",
                        "ram": None,
                        "cpus": None,
                        "cpu_limit": None,
                        "data_volume": None,
                        "boot_disk_size": None,
                        "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                        "tags": [],
                    },
                },
                {
                    "id": "n1",
                    "data": {
                        "node_definition": "external_connector",
                        "image_definition": None,
                        "label": "ext-conn-0",
                        "configuration": "bridge0",
                        "x": 0,
                        "y": 0,
                        "state": "STOPPED",
                        "ram": None,
                        "cpus": None,
                        "cpu_limit": None,
                        "data_volume": None,
                        "boot_disk_size": None,
                        "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                        "tags": [],
                    },
                },
            ],
            "links": [{"id": "l0", "interface_a": "i1", "interface_b": "i5", "data": {"state": "DEFINED_ON_CORE"}}],
            "interfaces": [
                {"id": "i0", "node": "n0", "data": {"label": "Loopback0", "slot": None, "state": "STOPPED", "type": "loopback"}},
                {"id": "i1", "node": "n0", "data": {"label": "mgmt0", "slot": 0, "state": "STOPPED", "type": "physical"}},
                {"id": "i2", "node": "n0", "data": {"label": "Ethernet2/1", "slot": 1, "state": "STOPPED", "type": "physical"}},
                {"id": "i3", "node": "n0", "data": {"label": "Ethernet2/2", "slot": 2, "state": "STOPPED", "type": "physical"}},
                {"id": "i4", "node": "n0", "data": {"label": "Ethernet2/3", "slot": 3, "state": "STOPPED", "type": "physical"}},
                {"id": "i5", "node": "n1", "data": {"label": "port", "slot": 0, "state": "STOPPED", "type": "physical"}},
            ],
            "lab": {
                "notes": "",
                "title": "Fake Lab",
                "description": "",
                "version": "0.1.0",
            }
        }
        return response

    def setUp(self):
        super().setUp()

        try:
            os.remove(".virl/current_cml_lab")
            os.system("cp -f tests/v2/static/fake_repo_topology.yaml topology.yaml")

        except OSError:
            pass

    def test_cml_up(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["up"])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(os.path.basename(os.readlink(".virl/current_cml_lab")) == self.get_up_id())
            self.assertTrue(os.path.isfile(os.readlink(".virl/current_cml_lab")))
            self.assertIn("Starting lab", result.output)

    def test_cml_up_by_name(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["up", "--lab-name", self.get_alt_title()])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(os.path.basename(os.readlink(".virl/current_cml_lab")) == self.get_alt_id())
            self.assertTrue(os.path.isfile(os.readlink(".virl/current_cml_lab")))

    def test_cml_up_by_id(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["up", "--id", self.get_alt_id()])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(os.path.basename(os.readlink(".virl/current_cml_lab")) == self.get_alt_id())
            self.assertTrue(os.path.isfile(os.readlink(".virl/current_cml_lab")))

    def test_cml_up_bad_yaml(self):
        try:
            os.system("cp tests/v2/static/fake_repo_bad_topology.yaml topology.yaml")
        except OSError:
            pass

        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["up"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("does not appear to be a YAML-formatted CML topology file", result.output)

    def test_cml_up_provision(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["up", "--provision"])
            self.assertEqual(0, result.exit_code)
            self.assertIn("Waiting for all nodes to be online", result.output)

    def test_cml_up_no_start(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["up", "--no-start"])
            self.assertEqual(0, result.exit_code)
            self.assertNotIn("Starting lab", result.output)

    def test_cml_up_after_use(self):
        super().setUp()
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["up"])
            self.assertEqual(0, result.exit_code)
            self.assertIn(
                "Lab {} (ID: {}) is already set as the current lab".format(self.get_test_title(), self.get_test_id()), result.output
            )

    def test_cml_up_running_lab(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["up", "--id", self.get_test_id()])
            self.assertEqual(0, result.exit_code)
            self.assertIn("Lab is already running (ID: {}, Title: {})".format(self.get_test_id(), self.get_test_title()), result.output)

    @patch("virl.cli.up.commands.call", autospec=False)
    def test_cml_up_no_lab(self, call_mock):
        try:
            os.remove("topology.yaml")
        except OSError:
            pass

        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["up"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("Could not find a lab to start", result.output)

    def test_cml_up_bogus_current_lab(self):
        src_dir = os.path.realpath(".virl")
        with open(".virl/cached_cml_labs/123456", "w") as fd:
            fd.write("lab: bogus\n")

        os.symlink("{}/cached_cml_labs/123456".format(src_dir), "{}/current_cml_lab".format(src_dir))
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["up"])
            os.remove(".virl/cached_cml_labs/123456")
            self.assertIn("Current lab is already set to {}, but that lab is not on server".format("123456"), result.output)

    @patch("virl.cli.up.commands.call", autospec=False, return_value=0)
    def test_cml_up_from_repo(self, call_mock):
        try:
            os.remove("topology.yaml")
        except OSError:
            pass

        try:
            os.remove("topology.virl")
        except OSError:
            pass

        with self.get_context() as m:
            self.setup_mocks(m)
            topo_url = "https://raw.githubusercontent.com/foo/bar/main/topology.yaml"
            self.setup_func("get", m, topo_url, json=MockGitHub.get_topology)
            virl = self.get_virl()
            runner = CliRunner()
            runner.invoke(virl, ["up", "foo/bar"])
            # The "call" function was called twice
            self.assertEqual(2, len(call_mock.mock_calls))
