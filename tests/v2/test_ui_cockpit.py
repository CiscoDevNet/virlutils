from click.testing import CliRunner

from virl.cli.cockpit.commands import cockpit
from virl.cli.ui.commands import ui


class FakeServer:
    host = "cml.example.local"


def test_cockpit_opens_expected_url(monkeypatch):
    opened = []
    monkeypatch.setattr("virl.cli.cockpit.commands.VIRLServer", lambda: FakeServer())
    monkeypatch.setattr("virl.cli.cockpit.commands.webbrowser.open", lambda url: opened.append(url))

    result = CliRunner().invoke(cockpit, [])

    assert result.exit_code == 0
    assert opened == ["https://cml.example.local:9090"]


def test_ui_opens_current_lab_when_present(monkeypatch):
    opened = []
    monkeypatch.setattr("virl.cli.ui.commands.VIRLServer", lambda: FakeServer())
    monkeypatch.setattr("virl.cli.ui.commands.get_cml_client", lambda _server: object())
    monkeypatch.setattr("virl.cli.ui.commands.get_current_lab", lambda: "lab-123")
    monkeypatch.setattr("virl.cli.ui.commands.safe_join_existing_lab", lambda _lab_id, _client: object())
    monkeypatch.setattr("virl.cli.ui.commands.webbrowser.open", lambda url: opened.append(url))

    result = CliRunner().invoke(ui, [])

    assert result.exit_code == 0
    assert opened == ["https://cml.example.local/lab/lab-123"]


def test_ui_does_not_open_when_current_lab_missing(monkeypatch):
    opened = []
    monkeypatch.setattr("virl.cli.ui.commands.VIRLServer", lambda: FakeServer())
    monkeypatch.setattr("virl.cli.ui.commands.get_cml_client", lambda _server: object())
    monkeypatch.setattr("virl.cli.ui.commands.get_current_lab", lambda: None)
    monkeypatch.setattr("virl.cli.ui.commands.webbrowser.open", lambda url: opened.append(url))

    result = CliRunner().invoke(ui, [])

    assert result.exit_code == 0
    assert opened == []
