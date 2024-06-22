import os

from click.testing import CliRunner

from . import BaseCMLTest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # noqa


class CMLUseTest(BaseCMLTest):
    @patch("virl.cli.use.commands.call", autospec=False, return_value=0)
    def test_cml_use(self, call_mock):
        with self.get_context() as m:
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            runner.invoke(virl, ["use"])
            call_mock.assert_called_once_with(["virl", "use", "--help"])

    def test_cml_use_with_lab(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["use", self.get_test_title()])
            self.assertEqual(0, result.exit_code)

    def test_cml_use_with_id(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["use", "--id", self.get_test_id()])
            self.assertEqual(0, result.exit_code)

    def test_cml_use_with_lab_name(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["use", "--lab-name", self.get_test_title()])
            self.assertEqual(0, result.exit_code)

    def test_cml_use_with_cache(self):
        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        try:
            os.remove(".virl/cached_cml_labs/{}".format(self.get_test_id()))
        except OSError:
            pass

        with self.get_context() as m:
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["use", "--id", self.get_test_id()])
            self.assertEqual(0, result.exit_code)

    def test_cml_use_with_bogus_id(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["use", "--id", "123456"])
            self.assertEqual(1, result.exit_code)
            self.assertIn("Unable to find unique lab in the cache or on the server", result.output)
