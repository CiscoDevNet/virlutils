import os

from click.testing import CliRunner

from . import BaseCMLTest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # type: ignore


class CMLStopTests(BaseCMLTest):
    def test_cml_stop(self):
        with self.get_context() as m:
            self.setup_func("get", m, "labs/{}/nodes/n1/check_if_converged".format(self.get_test_id()), json=True)
            self.setup_func("put", m, "labs/{}/nodes/n1/state/stop".format(self.get_test_id()), json=None)
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["stop", "rtr-1"])
            self.assertEqual(0, result.exit_code)
            self.assertNotIn("Node rtr-1 is already stopped", result.output)

    def test_cml_stop_by_id(self):
        with self.get_context() as m:
            self.setup_func("get", m, "labs/{}/nodes/{}/check_if_converged".format(self.get_cml24_id(), self.get_cml24_rtr_1()), json=True)
            self.setup_func("put", m, "labs/{}/nodes/{}/state/stop".format(self.get_cml24_id(), self.get_cml24_rtr_1()), json=None)
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["use", "--id", self.get_cml24_id()])
            result = runner.invoke(virl, ["stop", "--id", self.get_cml24_rtr_1()])
            self.assertEqual(0, result.exit_code)
            self.assertNotIn("Node rtr-1 is already stopped", result.output)

    def test_cml_stop_already_stopped(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["stop", "rtr-2"])
            self.assertEqual(0, result.exit_code)
            self.assertIn("Node rtr-2 is already stopped", result.output)

    def test_cml_stop_already_stopped_by_id(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["use", "--id", self.get_cml24_id()])
            result = runner.invoke(virl, ["stop", "--id", self.get_cml24_rtr_2()])
            self.assertEqual(0, result.exit_code)
            self.assertIn("Node rtr-2 is already stopped", result.output)

    @patch("virl.cli.stop.commands.call", autospec=False, return_value=0)
    def test_cml_stop_missing_args(self, call_mock):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["stop"])
            self.assertEqual(0, result.exit_code)
            # The "call" function was called once
            self.assertEqual(1, len(call_mock.mock_calls))

    def test_cml_stop_bogus_node(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["stop", "rtr-3"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("Node rtr-3 was not found in lab {}".format(self.get_test_id()), result.output)

    def test_cml_stop_bogus_lab(self):
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
            result = runner.invoke(virl, ["stop", "rtr-1"])
            os.remove(".virl/current_cml_lab")
            os.remove(".virl/cached_cml_labs/123456")
            self.assertEqual(1, result.exit_code)
            self.assertIn("Unable to find lab 123456", result.output)

    def test_cml_stop_no_current_lab(self):
        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["stop", "rtr-1"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("No current lab set", result.output)
