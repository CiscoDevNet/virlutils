from . import BaseCMLTest
from .mocks.github import MockGitHub  # noqa
from click.testing import CliRunner
import requests_mock
import os

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # noqa


class TestCMLUp(BaseCMLTest):
    def get_up_id(self):
        return "7e5712"

    def setup_mocks(self, m):
        super().setup_mocks(m)
        m.post(self.get_api_path("import?title=Fake%20Lab"), json={"id": self.get_up_id()})
        m.get(self.get_api_path("labs/{}/topology?exclude_configurations=False".format(self.get_up_id())), json=TestCMLUp.get_fake_topology)
        m.get(self.get_api_path("labs/{}/state".format(self.get_up_id())), json="STOPPED")
        m.put(self.get_api_path("labs/{}/start".format(self.get_up_id())), json="STARTED")
        m.put(self.get_api_path("labs/{}/start".format(self.get_alt_id())), json="STARTED")
        m.get(self.get_api_path("labs/{}/download".format(self.get_up_id())), text=MockGitHub.get_topology)

    @staticmethod
    def get_fake_topology(req, ctx):
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
            "lab_notes": "",
            "lab_title": "Fake Lab",
            "lab_description": "",
            "state": "STOPPED",
            "created_timestamp": 1589294717.9075089,
            "cluster_id": "cluster_1",
            "version": "0.0.3",
        }
        return response

    def setUp(self):
        super().setUp()

        try:
            os.remove(".virl/current_cml_lab")
            os.system("cp tests/v2/static/fake_repo_topology.yaml topology.yaml")

        except OSError:
            pass

    def test_cml_up(self):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["up"])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(os.path.basename(os.readlink(".virl/current_cml_lab")) == self.get_up_id())
            self.assertTrue(os.path.isfile(os.readlink(".virl/current_cml_lab")))

    def test_cml_up_by_name(self):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["up", "--lab-name", self.get_alt_title()])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(os.path.basename(os.readlink(".virl/current_cml_lab")) == self.get_alt_id())
            self.assertTrue(os.path.isfile(os.readlink(".virl/current_cml_lab")))

    def test_cml_up_by_id(self):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["up", "--id", self.get_alt_id()])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(os.path.basename(os.readlink(".virl/current_cml_lab")) == self.get_alt_id())
            self.assertTrue(os.path.isfile(os.readlink(".virl/current_cml_lab")))

    @patch("virl.cli.up.commands.call", auto_spec=False)
    def test_cml_up_from_repo(self, call_mock):
        try:
            os.remove("topology.yaml")
        except OSError:
            pass

        with requests_mock.Mocker() as m:
            self.setup_mocks(m)
            topo_url = "https://raw.githubusercontent.com/"
            topo_url += "foo/bar/master/topology.yaml"
            m.get(topo_url, json=MockGitHub.get_topology)
            virl = self.get_virl()
            runner = CliRunner()
            runner.invoke(virl, ["up", "foo/bar"])
