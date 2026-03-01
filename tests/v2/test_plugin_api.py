import types

from virl.api import plugin


def test_load_plugins_only_adds_real_directories(monkeypatch):
    monkeypatch.setattr(plugin, "iter_modules", lambda path: [])
    monkeypatch.setattr(plugin.os.path, "isdir", lambda p: p == "/tmp/real-plugin-dir")
    fake_syspath = []
    monkeypatch.setattr(plugin.sys, "path", fake_syspath)

    plugin.load_plugins("/tmp/real-plugin-dir:/tmp/missing-plugin-dir")

    assert fake_syspath == ["/tmp/real-plugin-dir"]


def test_load_plugins_reports_invalid_plugin_import(monkeypatch):
    monkeypatch.setattr(plugin.os.path, "isdir", lambda _p: False)
    monkeypatch.setattr(
        plugin,
        "iter_modules",
        lambda path: [types.SimpleNamespace(name="broken_plugin")],
    )

    def _raise_import_error(name):
        raise ImportError("boom")

    monkeypatch.setattr(plugin, "import_module", _raise_import_error)

    reported = []
    monkeypatch.setattr(plugin.click, "secho", lambda msg, fg: reported.append((msg, fg)))

    plugin.load_plugins(["/not/used"])

    assert reported == [("boom", "red")]
