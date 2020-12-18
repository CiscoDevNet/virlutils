from . import BaseCMLTest
from virl.api.plugin import _test_enable_plugins
from click.testing import CliRunner
import requests_mock
import os

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # noqa


class CMLBadPluginTest(BaseCMLTest):
    def localSetUp(self, pdir):
        os.environ["CML_PLUGIN_PATH"] = os.path.realpath("./tests/v2/{}".format(pdir))
        _test_enable_plugins()

    def tearDown(self):
        super().tearDown()
        os.environ.pop("CML_PLUGIN_PATH", None)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        os.environ.pop("CML_PLUGIN_PATH", None)
        _test_enable_plugins(enabled=False)

    @patch("virl.cli.main.click.secho", auto_spec=False)
    def test_cmd_plugin_bad(self, secho_mock):
        self.localSetUp("plugins_bad_cmd")
        virl = self.get_virl()
        with requests_mock.Mocker() as m:
            runner = CliRunner()
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            result = runner.invoke(virl, ["--help"])
            self.assertEqual(0, result.exit_code)
            self.assertNotIn("test-bad-cmd", result.output)
            secho_mock.assert_called_once_with(
                "ERROR: Malformed plugin for command test-bad-cmd.  The `run` method must be static and a click.command", fg="red"
            )

    @patch("virl.cli.generate.click.secho", auto_spec=False)
    def test_gen_plugin_bad(self, secho_mock):
        self.localSetUp("plugins_bad_gen")
        virl = self.get_virl()
        with requests_mock.Mocker() as m:
            runner = CliRunner()
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            result = runner.invoke(virl, ["generate", "--help"], catch_exceptions=False)
            self.assertEqual(0, result.exit_code)
            self.assertNotIn("test-bad-gen", result.output)
            secho_mock.assert_called_once_with(
                "ERROR: Malformed plugin for generator test-bad-gen.  The `generate` method must be static and a click.command", fg="red"
            )

    @patch("virl.api.plugin.click.secho", auto_spec=False)
    def test_view_plugin_bad(self, secho_mock):
        self.localSetUp("plugins_bad_viewer")
        virl = self.get_virl()
        with requests_mock.Mocker() as m:
            runner = CliRunner()
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            result = runner.invoke(virl, ["ls"])
            self.assertEqual(0, result.exit_code)
            self.assertNotIn("VIEWER PLUGIN", result.output)
            secho_mock.assert_any_call("invalid plugin BadLabViewer", fg="red")


"""

    def test_gen_plugin(self):
        virl = self.get_virl()
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            runner = CliRunner()
            result = runner.invoke(virl, ["generate", "test-gen"])
            self.assertEqual("TEST GENERATOR\n", result.output)

    def test_view_plugin(self):
        virl = self.get_virl()
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            runner = CliRunner()
            result = runner.invoke(virl, ["ls"])
            self.assertEqual("TEST VIEWER\n", result.output)
"""
