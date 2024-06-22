import os

from click.testing import CliRunner

from . import BaseCMLTest
from .mocks import MockCMLServer

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # noqa


class CMLTestWipe(BaseCMLTest):
    __m = None

    def setup_mocks(self, m):
        super().setup_mocks(m)
        self.__m = m

    def stop_lab(self, req=None, ctx=None):
        self.setup_func("get", self.__m, "labs/{}/state".format(self.get_test_id()), json="DEFINED_ON_CORE")
        return "STOPPED"

    def wipe_lab(self, req=None, ctx=None):
        self.setup_func("get", self.__m, "labs/{}/check_if_converged".format(self.get_test_id()), json=True)
        return "WIPED"

    def stop_node(self, req=None, ctx=None):
        self.setup_func(
            "get", self.__m, "labs/{}/lab_element_state".format(self.get_test_id()), json=MockCMLServer.get_lab_element_state_down
        )

    @patch("virl.cli.wipe.lab.commands.input", autospec=False, return_value="y")
    def test_cml_wipe_lab(self, input_mock):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            self.setup_func("get", m, "labs/{}/state".format(self.get_test_id()), json="DEFINED_ON_CORE")
            self.setup_func("put", m, "labs/{}/wipe".format(self.get_test_id()), json=self.wipe_lab)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "lab"])
            self.assertEqual(0, result.exit_code)
            self.assertNotIn("Not wiping lab", result.output)

    @patch("virl.cli.wipe.lab.commands.input", autospec=False, return_value="y")
    def test_cml_wipe_lab_force(self, input_mock):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            self.setup_func("put", m, "labs/{}/wipe".format(self.get_test_id()), json=self.wipe_lab)
            self.setup_func("put", m, "labs/{}/stop".format(self.get_test_id()), json=self.stop_lab)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "lab", "--force"])
            self.assertEqual(0, result.exit_code)

    @patch("virl.cli.wipe.lab.commands.input", autospec=False, return_value="y")
    def test_cml_wipe_lab_no_confirm(self, input_mock):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            self.setup_func("get", m, "labs/{}/state".format(self.get_test_id()), json="DEFINED_ON_CORE")
            self.setup_func("put", m, "labs/{}/wipe".format(self.get_test_id()), json=self.wipe_lab)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "lab", "--no-confirm"])
            self.assertEqual(0, result.exit_code)
            input_mock.assert_not_called()

    @patch("virl.cli.wipe.lab.commands.input", autospec=False, return_value="n")
    def test_cml_wipe_lab_denied(self, input_mock):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            self.setup_func("get", m, "labs/{}/state".format(self.get_test_id()), json="DEFINED_ON_CORE")
            self.setup_func("put", m, "labs/{}/wipe".format(self.get_test_id()), json=self.wipe_lab)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "lab"])
            self.assertEqual(0, result.exit_code)
            self.assertIn("Not wiping lab", result.output)

    def test_cml_wipe_lab_not_stopped(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            self.setup_func("put", m, "labs/{}/wipe".format(self.get_test_id()), json=self.wipe_lab)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "lab"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("is active", result.output)

    def test_cml_wipe_lab_no_lab(self):
        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "lab"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("Current lab is not set", result.output)

    def test_cml_wipe_lab_bogus_lab(self):
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
            result = runner.invoke(virl, ["wipe", "lab"])
            os.remove(".virl/cached_cml_labs/123456")
            os.remove(".virl/current_cml_lab")
            self.assertEqual(1, result.exit_code)
            self.assertIn("Unable to find lab 123456", result.output)

    @patch("virl.cli.wipe.node.commands.input", autospec=False, return_value="y")
    def test_cml_wipe_node(self, input_mock):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            self.setup_func("get", m, "labs/{}/nodes/n2/check_if_converged".format(self.get_test_id()), json=True)
            self.setup_func("put", m, "labs/{}/nodes/n2/wipe_disks".format(self.get_test_id()), json=True)
            self.setup_func("get", m, "labs/{}/nodes/n2/check_if_converged".format(self.get_test_id()), json=True)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "node", "rtr-2"])
            self.assertEqual(0, result.exit_code)
            self.assertNotIn("Not wiping node", result.output)

    @patch("virl.cli.wipe.node.commands.input", autospec=False, return_value="y")
    def test_cml_wipe_node_force(self, input_mock):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            self.setup_func("get", m, "labs/{}/nodes/n1/check_if_converged".format(self.get_test_id()), json=True)
            self.setup_func("put", m, "labs/{}/nodes/n1/state/stop".format(self.get_test_id()), json=self.stop_node)
            self.setup_func("put", m, "labs/{}/nodes/n1/wipe_disks".format(self.get_test_id()), json=True)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "node", "rtr-1", "--force"], catch_exceptions=False)
            self.assertEqual(0, result.exit_code)

    @patch("virl.cli.wipe.node.commands.input", autospec=False, return_value="y")
    def test_cml_wipe_node_no_confirm(self, input_mock):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            self.setup_func("get", m, "labs/{}/nodes/n2/check_if_converged".format(self.get_test_id()), json=True)
            self.setup_func("put", m, "labs/{}/nodes/n2/wipe_disks".format(self.get_test_id()), json=True)
            self.setup_func("get", m, "labs/{}/nodes/n2/check_if_converged".format(self.get_test_id()), json=True)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "node", "rtr-2", "--no-confirm"])
            self.assertEqual(0, result.exit_code)
            input_mock.assert_not_called()

    @patch("virl.cli.wipe.node.commands.input", autospec=False, return_value="n")
    def test_cml_wipe_node_denied(self, input_mock):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "node", "rtr-2"])
            self.assertEqual(0, result.exit_code)
            self.assertIn("Not wiping node", result.output)

    def test_cml_wipe_node_not_stopped(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "node", "rtr-1"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("is active", result.output)

    def test_cml_wipe_node_bogus_node(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "node", "rtr-3"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("Node rtr-3 was not found in lab {}".format(self.get_test_id()), result.output)

    def test_cml_wipe_node_bogus_lab(self):
        src_dir = os.path.realpath(".virl")
        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        with open(".virl/cached_cml_labs/123456", "w") as fd:
            fd.write("lab: bogus\n")

        os.symlink("{}/cached_cml_labs/123456".format(src_dir), "{}/current_cml_lab".format(src_dir))
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "node", "rtr-1"])
            os.remove(".virl/current_cml_lab")
            os.remove(".virl/cached_cml_labs/123456")
            self.assertEqual(1, result.exit_code)
            self.assertIn("Unable to find lab 123456", result.output)

    def test_cml_wipe_node_no_current_lab(self):
        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["wipe", "node", "rtr-1"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("No current lab set", result.output)
