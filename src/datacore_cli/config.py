"""Persistent config for the DataCore CLI."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

CONFIG_DIR = Path(os.environ.get("DATACORE_CONFIG_DIR", Path.home() / ".datacore"))
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULTS: dict[str, Any] = {
    "base_url": "https://api.datacore.vn/v1",
    "output_dir": str(Path.home() / "datacore-data"),
    "default_format": "table",
}


def load() -> dict[str, Any]:
    """Load config, merging file values over defaults."""
    cfg = dict(DEFAULTS)
    if CONFIG_FILE.exists():
        cfg.update(json.loads(CONFIG_FILE.read_text()))
    return cfg


def save(cfg: dict[str, Any]) -> Path:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
    return CONFIG_FILE


def set_value(key: str, value: str) -> dict[str, Any]:
    cfg = load()
    cfg[key] = value
    save(cfg)
    return cfg


def get_value(key: str) -> Any:
    return load().get(key)
