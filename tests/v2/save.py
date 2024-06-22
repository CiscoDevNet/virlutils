import os

from click.testing import CliRunner

from . import BaseCMLTest


class CMLSaveTests(BaseCMLTest):
    def test_cml_save(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["save"])
            self.assertEqual(0, result.exit_code)
            self.assertIn("Extracting configurations", result.output)
            self.assertIn("Writing topology.yaml", result.output)

    def test_cml_save_no_extract(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["save", "--no-extract"])
            self.assertEqual(0, result.exit_code)
            self.assertNotIn("Extracting configurations", result.output)
            self.assertIn("Writing topology.yaml", result.output)

    def test_cml_save_filename(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["save", "-f", "{}.yaml".format(self.get_test_id())])
            self.assertEqual(0, result.exit_code)
            self.assertIn("Extracting configurations", result.output)
            self.assertIn("Writing {}.yaml".format(self.get_test_id()), result.output)

    def test_cml_save_no_lab(self):
        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["save"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("Current lab is not set", result.output)

    def test_cml_save_bogus_lab(self):
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
            result = runner.invoke(virl, ["save"])
            os.remove(".virl/cached_cml_labs/123456")
            os.remove(".virl/current_cml_lab")
            self.assertEqual(1, result.exit_code)
            self.assertIn("Failed to find running lab 123456", result.output)
