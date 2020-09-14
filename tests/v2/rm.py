from . import BaseCMLTest
from click.testing import CliRunner
import requests_mock
import os

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # noqa


class CMLTestRm(BaseCMLTest):
    __m = None

    def setup_mocks(self, m):
        super().setup_mocks(m)
        self.__m = m
        m.delete(self.get_api_path("labs/{}".format(self.get_alt_id())), json="DELETED")

    def wipe_lab(self, req, ctx):
        self.__m.get(self.get_api_path("labs/{}/state".format(self.get_alt_id())), json="DEFINED_ON_CORE")
        self.__m.get(self.get_api_path("labs/{}/check_if_converged".format(self.get_alt_id())), json=True)
        return "WIPED"

    @patch("virl.cli.rm.commands.input", auto_spec=False, return_value="y")
    def test_cml_rm(self, input_mock):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            m.get(self.get_api_path("labs/{}/state".format(self.get_alt_id())), json="DEFINED_ON_CORE")
            virl = self.get_virl()
            runner = CliRunner()
            runner.invoke(virl, ["use", "--id", self.get_alt_id()])
            result = runner.invoke(virl, ["rm"])
            self.assertEqual(0, result.exit_code)
            self.assertNotIn("Not removing lab", result.output)

    @patch("virl.cli.rm.commands.input", auto_spec=False, return_value="y")
    def test_cml_rm_force(self, input_mock):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            m.put(self.get_api_path("labs/{}/wipe".format(self.get_alt_id())), json=self.wipe_lab)
            virl = self.get_virl()
            runner = CliRunner()
            runner.invoke(virl, ["use", "--id", self.get_alt_id()])
            result = runner.invoke(virl, ["rm", "--force"])
            self.assertEqual(0, result.exit_code)

    @patch("virl.cli.rm.commands.input", auto_spec=False, return_value="y")
    def test_cml_rm_no_confirm(self, input_mock):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            m.get(self.get_api_path("labs/{}/state".format(self.get_alt_id())), json="DEFINED_ON_CORE")
            virl = self.get_virl()
            runner = CliRunner()
            runner.invoke(virl, ["use", "--id", self.get_alt_id()])
            result = runner.invoke(virl, ["rm", "--no-confirm"])
            self.assertEqual(0, result.exit_code)
            input_mock.assert_not_called()

    @patch("virl.cli.rm.commands.input", auto_spec=False, return_value="y")
    def test_cml_rm_from_cache(self, input_mock):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            m.get(self.get_api_path("labs/{}/state".format(self.get_alt_id())), json="DEFINED_ON_CORE")
            virl = self.get_virl()
            runner = CliRunner()
            runner.invoke(virl, ["use", "--id", self.get_alt_id()])
            result = runner.invoke(virl, ["rm", "--from-cache"])
            self.assertEqual(0, result.exit_code)
            self.assertIn("Removed lab {} from cache".format(self.get_alt_id()), result.output)

    @patch("virl.cli.rm.commands.input", auto_spec=False, return_value="n")
    def test_cml_rm_denied(self, input_mock):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            m.get(self.get_api_path("labs/{}/state".format(self.get_alt_id())), json="DEFINED_ON_CORE")
            virl = self.get_virl()
            runner = CliRunner()
            runner.invoke(virl, ["use", "--id", self.get_alt_id()])
            result = runner.invoke(virl, ["rm"])
            self.assertEqual(0, result.exit_code)
            self.assertIn("Not removing lab", result.output)

    def test_cml_rm_not_wiped(self):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            runner.invoke(virl, ["use", "--id", self.get_alt_id()])
            result = runner.invoke(virl, ["rm"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("either active or not wiped", result.output)

    def test_cml_rm_no_lab(self):
        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["rm"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("Current lab is not set", result.output)

    def test_cml_rm_bogus_lab(self):
        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        src_dir = os.path.realpath(".virl")
        with open(".virl/cached_cml_labs/123456", "w") as fd:
            fd.write("lab: bogus\n")

        os.symlink("{}/cached_cml_labs/123456".format(src_dir), "{}/current_cml_lab".format(src_dir))

        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["rm"])
            os.remove(".virl/cached_cml_labs/123456")
            os.remove(".virl/current_cml_lab")
            self.assertEqual(1, result.exit_code)
            self.assertIn("Unable to find lab 123456", result.output)
