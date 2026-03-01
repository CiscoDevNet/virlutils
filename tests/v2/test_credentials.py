from virl.api import credentials


def test_get_from_file_ignores_malformed_lines(tmp_path):
    rcfile = tmp_path / ".virlrc"
    rcfile.write_text("VIRL_HOST\nVIRL_USERNAME = admin\n")

    assert credentials._get_from_file(str(rcfile), "VIRL_HOST") is None
    assert credentials._get_from_file(str(rcfile), "VIRL_USERNAME") == "admin"


def test_get_from_file_handles_double_quoted_values(tmp_path):
    rcfile = tmp_path / ".virlrc"
    rcfile.write_text('VIRL_PASSWORD="s3cr3t"\n')

    assert credentials._get_from_file(str(rcfile), "VIRL_PASSWORD") == "s3cr3t"


def test_get_prop_prefers_environment_when_no_virlrc(monkeypatch, tmp_path):
    monkeypatch.setenv("VIRL_HOST", "env-host")
    monkeypatch.setattr(credentials.os, "getcwd", lambda: str(tmp_path))
    monkeypatch.setattr(credentials, "find_virl", lambda: None)
    monkeypatch.setattr(credentials.os.path, "expanduser", lambda _: str(tmp_path / "missing-home"))

    assert credentials.get_prop("VIRL_HOST") == "env-host"


def test_get_prop_reads_home_virlrc_when_environment_missing(monkeypatch, tmp_path):
    monkeypatch.delenv("VIRL_USERNAME", raising=False)
    monkeypatch.setattr(credentials.os, "getcwd", lambda: str(tmp_path))
    monkeypatch.setattr(credentials, "find_virl", lambda: None)
    monkeypatch.setattr(credentials.os.path, "expanduser", lambda _: str(tmp_path))

    home_rc = tmp_path / ".virlrc"
    home_rc.write_text("VIRL_USERNAME=home-admin\n")

    assert credentials.get_prop("VIRL_USERNAME") == "home-admin"


def test_get_credentials_returns_tuple_with_optional_config(monkeypatch):
    values = {
        "VIRL_HOST": "localhost",
        "VIRL_USERNAME": "admin",
        "VIRL_PASSWORD": "admin",
        "CML_DEVICE_USERNAME": "devuser",
        "CML_PLUGIN_PATH": "/plugins",
    }

    monkeypatch.setattr(credentials, "get_prop", lambda name: values.get(name))
    host, username, password, config = credentials.get_credentials()

    assert (host, username, password) == ("localhost", "admin", "admin")
    assert config["CML_DEVICE_USERNAME"] == "devuser"
    assert config["CML_PLUGIN_PATH"] == "/plugins"
    assert "CML_DEVICE_PASSWORD" not in config
