from . import BaseCMLTest
from click.testing import CliRunner
import requests_mock
import os


class CMLStartTests(BaseCMLTest):
    def test_cml_start(self):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            m.put(self.get_api_path("labs/{}/nodes/n2/state/start".format(self.get_test_id())), json=None)
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["start", "rtr-2"])
            self.assertEqual(0, result.exit_code)
            self.assertNotIn("Node rtr-2 is already active", result.output)

    def test_cml_start_already_active(self):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["start", "rtr-1"])
            self.assertEqual(0, result.exit_code)
            self.assertIn("Node rtr-1 is already active", result.output)

    def test_cml_start_bogus_node(self):
        with requests_mock.Mocker() as m:
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
        with requests_mock.Mocker() as m:
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

        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["start", "rtr-1"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("No current lab set", result.output)
