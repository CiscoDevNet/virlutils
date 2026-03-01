import os
import types
import importlib
import errno

import pytest
from requests.exceptions import HTTPError

import virl.helpers as helpers


class _FakeNode:
    def __init__(self, label="n1", booted=True, exc=None):
        self.label = label
        self._booted = booted
        self._exc = exc
        self.extracted = False

    def is_booted(self):
        return self._booted

    def extract_configuration(self):
        if self._exc:
            raise self._exc
        self.extracted = True


class _FakeLab:
    def __init__(self, nodes):
        self._nodes = nodes

    def nodes(self):
        return self._nodes


class _FakeInterface:
    def __init__(self, ipv4=None, ipv6=None):
        self.discovered_ipv4 = ipv4 or []
        self.discovered_ipv6 = ipv6 or []


def test_find_virl_or_else_and_cache_paths(monkeypatch):
    monkeypatch.setattr(helpers, "find_virl", lambda: None)
    assert helpers.find_virl_or_else() == "."
    assert helpers.get_cache_root().endswith("/.virl/cached_cml_labs")
    assert helpers.get_current_lab_link().endswith("/.virl/current_cml_lab")
    assert helpers.get_default_plugin_dir().endswith("/.virl/plugins")


def test_safe_join_existing_lab_variants():
    client = types.SimpleNamespace(
        get_lab_list=lambda: ["lab-1"],
        join_existing_lab=lambda lab_id: {"id": lab_id},
        find_labs_by_title=lambda title: ["lab-1"] if title == "one" else ["a", "b"],
    )
    assert helpers.safe_join_existing_lab("lab-1", client) == {"id": "lab-1"}
    assert helpers.safe_join_existing_lab("missing", client) is None
    assert helpers.safe_join_existing_lab_by_title("one", client) == "lab-1"
    assert helpers.safe_join_existing_lab_by_title("dup", client) is None


def test_cache_lab_data_and_current_lab_link(monkeypatch, tmp_path):
    cache_root = tmp_path / ".virl" / "cached_cml_labs"
    current = tmp_path / ".virl" / "current_cml_lab"
    monkeypatch.setattr(helpers, "get_cache_root", lambda: str(cache_root))
    monkeypatch.setattr(helpers, "get_current_lab_link", lambda: str(current))

    helpers.cache_lab_data("lab-1", "topology-data")
    assert (cache_root / "lab-1").read_text() == "topology-data"

    helpers.set_current_lab("lab-1")
    assert helpers.get_current_lab() == "lab-1"

    helpers.clear_current_lab("other")
    assert os.path.exists(current)
    helpers.clear_current_lab("lab-1")
    assert not os.path.exists(current)


def test_check_lab_cache_handles_errors(monkeypatch, tmp_path):
    monkeypatch.setattr(helpers, "get_cache_root", lambda: str(tmp_path))
    cached = tmp_path / "lab-1"
    cached.write_text("x")
    assert helpers.check_lab_cache("lab-1").endswith("lab-1")

    monkeypatch.setattr(helpers, "get_cache_root", lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    assert helpers.check_lab_cache("lab-1") is None


def test_extract_configurations_handles_http_and_generic_errors(monkeypatch):
    good = _FakeNode(label="good")
    bad_http = _FakeNode(label="bad-http")
    bad_generic = _FakeNode(label="bad-generic")

    http_error = HTTPError("bad")
    http_error.response = types.SimpleNamespace(status_code=500)
    bad_http._exc = http_error
    bad_generic._exc = RuntimeError("oops")

    warnings = []
    monkeypatch.setattr(helpers.click, "secho", lambda msg, fg="yellow": warnings.append((msg, fg)))

    helpers.extract_configurations(_FakeLab([good, bad_http, bad_generic]))

    assert good.extracted is True
    assert any("bad-http" in msg for msg, _ in warnings)
    assert any("bad-generic" in msg for msg, _ in warnings)


def test_extract_configurations_ignores_http_400(monkeypatch):
    bad_http_400 = _FakeNode(label="bad-http-400")
    err = HTTPError("bad-400")
    err.response = types.SimpleNamespace(status_code=400)
    bad_http_400._exc = err

    warnings = []
    monkeypatch.setattr(helpers.click, "secho", lambda msg, fg="yellow": warnings.append((msg, fg)))
    helpers.extract_configurations(_FakeLab([bad_http_400]))
    assert warnings == []


def test_get_node_mgmt_ip_prefers_ipv4_then_non_link_local_ipv6():
    node_v4 = types.SimpleNamespace(interfaces=lambda: [_FakeInterface(ipv4=["10.10.10.10"])])
    assert helpers.get_node_mgmt_ip(node_v4) == "10.10.10.10"

    node_v6 = types.SimpleNamespace(interfaces=lambda: [_FakeInterface(ipv6=["fe80::1", "2001:db8::1"])])
    assert helpers.get_node_mgmt_ip(node_v6) == "2001:db8::1"


def test_get_node_mgmt_ip_skips_link_local_only_ipv6():
    node_v6 = types.SimpleNamespace(interfaces=lambda: [_FakeInterface(ipv6=["fe80::1"])])
    assert helpers.get_node_mgmt_ip(node_v6) is None


def test_get_cml_client_uses_verify_flag_and_clears_env(monkeypatch):
    captured = {}

    def fake_client(host, user, password, raise_for_auth_failure, ssl_verify):
        captured.update(
            {
                "host": host,
                "user": user,
                "password": password,
                "raise_for_auth_failure": raise_for_auth_failure,
                "ssl_verify": ssl_verify,
            }
        )
        return "client"

    monkeypatch.setattr(helpers, "ClientLibrary", fake_client)
    os.environ["VIRL2_USER"] = "u"
    os.environ["VIRL2_PASS"] = "p"
    os.environ["VIRL2_URL"] = "url"

    server = types.SimpleNamespace(host="h", user="u", passwd="p", config={"CML_VERIFY_CERT": "false"})
    assert helpers.get_cml_client(server) == "client"
    assert captured["ssl_verify"] is False
    assert "VIRL2_USER" not in os.environ

    server.config["CML_VERIFY_CERT"] = "/tmp/cert.pem"
    helpers.get_cml_client(server)
    assert captured["ssl_verify"] == "/tmp/cert.pem"
    helpers.get_cml_client(server, ignore=True)
    assert captured["ssl_verify"] is False


def test_group_permission_helpers_and_command_detection(monkeypatch):
    assert helpers.convert_permissions("read_write") == ["lab_view", "lab_edit", "lab_exec", "lab_admin"]
    assert helpers.convert_permissions("read_only") == ["lab_view"]

    users = [{"id": "1", "username": "a"}, {"id": "2", "username": "b"}]
    assert helpers.get_group_member_ids(users, ["b"], False) == ["2"]
    assert helpers.get_group_member_ids(users, ["b"], True) == ["1", "2"]

    client = types.SimpleNamespace(get_lab_list=lambda: ["lab-1", "lab-2"])
    assert helpers.get_group_associations(client, None, "read_only") == [
        {"id": "lab-1", "permissions": ["lab_view"]},
        {"id": "lab-2", "permissions": ["lab_view"]},
    ]
    assert helpers.get_group_associations(client, [("lab-9", "read_write")], None) == [
        {"id": "lab-9", "permissions": ["lab_view", "lab_edit", "lab_exec", "lab_admin"]}
    ]
    assert helpers.get_group_associations(client, None, None) == []

    monkeypatch.setattr(helpers.sys, "argv", ["cml"])
    assert helpers.get_command() == "cml"
    monkeypatch.setattr(helpers.sys, "argv", ["virl"])
    assert helpers.get_command() == "virl"


def test_set_current_lab_raises_when_cache_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(helpers, "get_cache_root", lambda: str(tmp_path / "cache"))
    monkeypatch.setattr(helpers, "get_current_lab_link", lambda: str(tmp_path / "link"))
    with pytest.raises(FileNotFoundError):
        helpers.set_current_lab("missing")


def test_mkdir_p_raises_non_eexist(monkeypatch):
    def _boom(_path):
        raise OSError(errno.EPERM, "denied")

    monkeypatch.setattr(helpers.os, "makedirs", _boom)
    with pytest.raises(OSError):
        helpers.mkdir_p("/tmp/denied")


def test_find_virl_windows_and_edge_cases(monkeypatch):
    # Force while loop to exit immediately (covers while false branch).
    class _RootLike(str):
        def split(self, _sep):
            return "\\"

    monkeypatch.setattr(helpers.os, "getcwd", lambda: _RootLike("\\"))
    monkeypatch.setattr(helpers.os.path, "abspath", lambda _p: "\\")
    monkeypatch.setattr(helpers.platform, "system", lambda: "Windows")
    assert helpers.find_virl() is None

    # Trigger Windows path building and IndexError path in pop().
    monkeypatch.setattr(helpers.os, "getcwd", lambda: "")
    monkeypatch.setattr(helpers.os.path, "abspath", lambda _p: "\\")
    monkeypatch.setattr(helpers.os, "listdir", lambda _p: [])
    assert helpers.find_virl() is None

    # Cover non-empty Windows lookin path branch.
    monkeypatch.setattr(helpers.os, "getcwd", lambda: "foo/bar")
    monkeypatch.setattr(helpers.os.path, "abspath", lambda _p: "\\")
    monkeypatch.setattr(helpers.os, "listdir", lambda _p: [".virl"])
    assert helpers.find_virl() == "foo\\bar"


def test_windows_redirection_context_manager(monkeypatch):
    # Reload helpers as if running on Windows so class attributes are created.
    import platform
    import ctypes
    import virl.helpers as helpers_mod

    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(ctypes, "windll", types.SimpleNamespace(kernel32=types.SimpleNamespace()), raising=False)
    monkeypatch.setattr(
        ctypes.windll.kernel32,
        "Wow64DisableWow64FsRedirection",
        lambda *_args: 1,
        raising=False,
    )
    monkeypatch.setattr(
        ctypes.windll.kernel32,
        "Wow64RevertWow64FsRedirection",
        lambda *_args: 1,
        raising=False,
    )

    win_helpers = importlib.reload(helpers_mod)
    ctx = win_helpers.disable_file_system_redirection()
    ctx.__enter__()
    ctx.__exit__(None, None, None)

    # Cover __exit__ no-op branch when disabling redirection fails.
    monkeypatch.setattr(ctypes.windll.kernel32, "Wow64DisableWow64FsRedirection", lambda *_args: 0, raising=False)
    win_helpers = importlib.reload(helpers_mod)
    ctx = win_helpers.disable_file_system_redirection()
    ctx.__enter__()
    ctx.__exit__(None, None, None)


def test_get_cml_client_without_verify_cert_key(monkeypatch):
    captured = {}

    def fake_client(host, user, password, raise_for_auth_failure, ssl_verify):
        captured["ssl_verify"] = ssl_verify
        return "client"

    monkeypatch.setattr(helpers, "ClientLibrary", fake_client)
    server = types.SimpleNamespace(host="h", user="u", passwd="p", config={})
    assert helpers.get_cml_client(server) == "client"
    assert captured["ssl_verify"] is True
