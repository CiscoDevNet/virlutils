from . import BaseCMLTest
from virl.api.plugin import _test_enable_plugins
from click.testing import CliRunner
import requests_mock
import os


class CMLGoodPluginTest(BaseCMLTest):
    def setUp(self):
        _test_enable_plugins()
        super().setUp()
        os.environ["CML_PLUGIN_PATH"] = os.path.realpath("./tests/v2/plugins_good")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        os.environ.pop("CML_PLUGIN_PATH", None)
        _test_enable_plugins(enabled=False)

    def test_cmd_plugin_output(self):
        virl = self.get_virl()
        with requests_mock.Mocker() as m:
            runner = CliRunner()
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            result = runner.invoke(virl, ["--help"])
            self.assertEqual(0, result.exit_code)
            self.assertIn("test-cmd", result.output)

    def test_cmd_plugin(self):
        virl = self.get_virl()
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            runner = CliRunner()
            result = runner.invoke(virl, ["test-cmd"])
            self.assertEqual("TEST COMMAND\n", result.output)

    def test_gen_plugin_output(self):
        virl = self.get_virl()
        with requests_mock.Mocker() as m:
            runner = CliRunner()
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            result = runner.invoke(virl, ["generate", "--help"])
            self.assertEqual(0, result.exit_code)
            self.assertIn("test-gen", result.output)

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
