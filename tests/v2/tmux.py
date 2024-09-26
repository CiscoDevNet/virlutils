from click.testing import CliRunner

from . import BaseCMLTest

try:
    from unittest.mock import call, patch
except ImportError:
    from mock import call, patch


class CMLTmuxTests(BaseCMLTest):
    @patch("virl.cli.tmux.commands.libtmux.server.Server")
    def test_cml_tmux_panes(self, mock_server):
        with self.get_context() as m:
            # Mocking libtmux server
            mock_session = mock_server.return_value.new_session.return_value
            mock_window = mock_session.windows[0]
            mock_pane = mock_window.panes[0]
            mock_window.split_window.return_value = mock_pane
            mock_window.panes = [mock_pane]
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            runner.invoke(virl, ["tmux"])
            mock_server.assert_called_once()
            mock_server.return_value.new_session.assert_called_once_with(session_name="Mock Test-5f0d", kill_session=True)
            expected_calls = [
                call("printf '\\033]2;%s\\033\\\\' 'rtr-1'", suppress_history=True),
                call("ssh -t admin@localhost open /5f0d96/n1/0", suppress_history=True),
            ]
            mock_pane.send_keys.assert_has_calls(expected_calls, any_order=True)

    @patch("virl.cli.tmux.commands.libtmux.server.Server")
    def test_cml_tmux_panes24(self, mock_server):
        with self.get_context() as m:
            # Mocking libtmux server
            mock_session = mock_server.return_value.new_session.return_value
            mock_window = mock_session.windows[0]
            mock_pane = mock_window.panes[0]
            mock_window.split_window.return_value = mock_pane
            mock_window.panes = [mock_pane]
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            lab_id = self.get_cml24_id()
            runner.invoke(virl, ["use", "--id", lab_id])
            runner.invoke(virl, ["tmux"])
            mock_server.assert_called_once()
            mock_server.return_value.new_session.assert_called_once_with(session_name="Mock Test 2_4-8811", kill_session=True)
            expected_calls = [
                call("printf '\\033]2;%s\\033\\\\' 'rtr-1'", suppress_history=True),
                call("ssh -t admin@localhost open /Mock Test 2.4/rtr-1/0", suppress_history=True),
            ]
            mock_pane.send_keys.assert_has_calls(expected_calls, any_order=True)

    @patch("virl.cli.tmux.commands.libtmux.server.Server")
    def test_cml_tmux_windows_24(self, mock_server):
        with self.get_context() as m:
            # Mocking libtmux server
            mock_session = mock_server.return_value.new_session.return_value
            mock_window = mock_session.windows[0]
            mock_session.windows = [mock_window]
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            lab_id = self.get_cml24_id()
            runner.invoke(virl, ["use", "--id", lab_id])
            runner.invoke(virl, ["tmux", "--group", "windows"])
            mock_server.assert_called_once()
            mock_server.return_value.new_session.assert_called_once_with(session_name="Mock Test 2_4-8811", kill_session=True)
            expected_calls = [
                call("rename-window", "rtr-1"),
            ]
            mock_window.cmd.assert_has_calls(expected_calls, any_order=True)
