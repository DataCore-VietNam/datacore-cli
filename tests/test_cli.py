"""Tests for the DataCore CLI."""

import pytest
from typer.testing import CliRunner

from datacore_cli.main import app


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def tmp_config(tmp_path, monkeypatch):
    monkeypatch.setenv("DATACORE_CONFIG_DIR", str(tmp_path))
    import datacore_cli.config as cfg
    cfg.CONFIG_DIR = tmp_path
    cfg.CONFIG_FILE = tmp_path / "config.json"
    return tmp_path


def test_version(runner):
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "datacore-cli" in result.output


def test_config_show_defaults(runner, tmp_config):
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert "https://api.datacore.vn/v1" in result.output


def test_config_set_then_get(runner, tmp_config):
    r1 = runner.invoke(app, ["config", "set", "base_url", "https://staging.datacore.vn"])
    assert r1.exit_code == 0
    r2 = runner.invoke(app, ["config", "get", "base_url"])
    assert r2.exit_code == 0
    assert "https://staging.datacore.vn" in r2.output


def test_config_get_unset_key_exits_nonzero(runner, tmp_config):
    result = runner.invoke(app, ["config", "get", "totally_not_set"])
    assert result.exit_code == 1


def test_mcp_requires_api_key(runner, monkeypatch):
    monkeypatch.delenv("DATACORE_API_KEY", raising=False)
    result = runner.invoke(app, ["mcp"])
    assert result.exit_code == 1
    assert "not set" in result.output.lower()
