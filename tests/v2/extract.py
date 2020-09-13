from . import BaseCMLTest
from click.testing import CliRunner
import requests_mock
import os


class CMLExtractTests(BaseCMLTest):
    def test_cml_extract(self):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["extract"])
            self.assertEqual(0, result.exit_code)

    def test_cml_extract_no_lab(self):
        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["extract"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("Current lab is not set", result.output)

    def test_cml_extract_bogus_lab(self):
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
            result = runner.invoke(virl, ["extract"])
            os.remove(".virl/cached_cml_labs/123456")
            os.remove(".virl/current_cml_lab")
            self.assertEqual(1, result.exit_code)
            self.assertIn("Failed to find running lab 123456", result.output)
