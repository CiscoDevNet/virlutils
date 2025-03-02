import os

from click.testing import CliRunner

from . import BaseCMLTest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # type: ignore


class CMLStartTests(BaseCMLTest):
    def test_cml_start(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_func("get", m, "labs/{}/nodes/n2/check_if_converged".format(self.get_test_id()), json=True)
            self.setup_func("put", m, "labs/{}/nodes/n2/state/start".format(self.get_test_id()), json=None)
            self.setup_func("get", m, "labs/{}/nodes/n2/check_if_converged".format(self.get_test_id()), json=True)
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["start", "rtr-2"])
            self.assertEqual(0, result.exit_code)
            self.assertNotIn("Node rtr-2 is already active", result.output)

    def test_cml_start_by_id(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_func("get", m, "labs/{}/nodes/{}/check_if_converged".format(self.get_cml24_id(), self.get_cml24_rtr_2()), json=True)
            self.setup_func("put", m, "labs/{}/nodes/{}/state/start".format(self.get_cml24_id(), self.get_cml24_rtr_2()), json=None)
            self.setup_func("get", m, "labs/{}/nodes/{}/check_if_converged".format(self.get_cml24_id(), self.get_cml24_rtr_2()), json=True)
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["use", "--id", self.get_cml24_id()])
            result = runner.invoke(virl, ["start", "--id", self.get_cml24_rtr_2()])
            self.assertEqual(0, result.exit_code)
            self.assertNotIn("Node rtr-2 is already active", result.output)

    def test_cml_start_already_active(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["start", "rtr-1"])
            self.assertEqual(0, result.exit_code)
            self.assertIn("Node rtr-1 is already active", result.output)

    def test_cml_start_already_active_by_id(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["use", "--id", self.get_cml24_id()])
            result = runner.invoke(virl, ["start", "--id", self.get_cml24_rtr_1()])
            print(result.output)
            self.assertEqual(0, result.exit_code)
            self.assertIn("Node rtr-1 is already active", result.output)

    @patch("virl.cli.start.commands.call", autospec=False, return_value=0)
    def test_cml_start_missing_args(self, call_mock):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["start"])
            self.assertEqual(0, result.exit_code)
            # The "call" function was called once
            self.assertEqual(1, len(call_mock.mock_calls))

    def test_cml_start_bogus_node(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["start", "rtr-3"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("Node rtr-3 was not found in lab {}".format(self.get_test_id()), result.output)

    def test_cml_start_bogus_lab(self):
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
            result = runner.invoke(virl, ["start", "rtr-1"])
            os.remove(".virl/current_cml_lab")
            os.remove(".virl/cached_cml_labs/123456")
            self.assertEqual(1, result.exit_code)
            self.assertIn("Unable to find lab 123456", result.output)

    def test_cml_start_no_current_lab(self):
        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["start", "rtr-1"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("No current lab set", result.output)
