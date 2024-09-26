from click.testing import CliRunner

from . import BaseCMLTest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class CMLConsoleTests(BaseCMLTest):
    def test_cml_console_display(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["console", "rtr-1", "--display"])
            self.assertEqual(0, result.exit_code)

    @patch("virl.cli.console.commands.call", autospec=False)
    def test_cml_console_connect(self, call_mock):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            runner.invoke(virl, ["console", "rtr-1"])
            call_mock.assert_called_once_with(["ssh", "-t", "admin@localhost", "open", "/5f0d96/n1/0"])

    @patch("virl.cli.console.commands.call", autospec=False)
    def test_cml_console_connect_24(self, call_mock):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            runner.invoke(virl, ["use", "--id", self.get_cml24_id()])
            runner.invoke(virl, ["console", "rtr-1"])
            call_mock.assert_called_once_with(["ssh", "-t", "admin@localhost", "open", "/Mock", "Test", "2.4/rtr-1/0"])
