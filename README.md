<div align="center">

# datacore-cli

**Vietnamese financial and alternative data, from your terminal.**

[![PyPI](https://img.shields.io/pypi/v/datacore-cli?color=blue&label=PyPI)](https://pypi.org/project/datacore-cli/)
[![Python](https://img.shields.io/pypi/pyversions/datacore-cli)](https://pypi.org/project/datacore-cli/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CI](https://github.com/DataCore-VietNam/datacore-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/DataCore-VietNam/datacore-cli/actions)
[![Downloads](https://img.shields.io/pypi/dm/datacore-cli)](https://pypi.org/project/datacore-cli/)

[Website](https://datacore.vn) · [Docs](https://docs.datacore.vn) · [API Reference](https://docs.datacore.vn/api) · [Changelog](CHANGELOG.md)

</div>

---

`datacore` is the official CLI for [DataCore](https://datacore.vn) — Vietnam's financial and alternative data platform. Search the catalog, preview datasets, and download production-grade data to CSV or Parquet, all without leaving your terminal.

```bash
pip install datacore-cli
export DATACORE_API_KEY=dc_...

datacore search "VN30 fundamentals"
datacore get equity.vn30.daily --start 2024-01-01 --output vn30.parquet
```

---

## Installation

```bash
pip install datacore-cli
```

Requires Python 3.10+. The CLI is a thin wrapper around the [DataCore Python SDK](https://github.com/DataCore-VietNam/DataCore); it is installed automatically.

### Shell completions (optional)

```bash
# Bash
datacore --install-completion bash

# Zsh
datacore --install-completion zsh

# Fish
datacore --install-completion fish
```

---

## Authentication

Get your API key at **[datacore.vn/dashboard](https://datacore.vn/dashboard)**.

```bash
# Option 1 — environment variable (recommended for CI/scripts)
export DATACORE_API_KEY=dc_...

# Option 2 — persistent config file
datacore config set api_key dc_...
```

The config file lives at `~/.config/datacore/config.json` on Linux/macOS and `%APPDATA%\datacore\config.json` on Windows.

---

## Commands

### Discovery

| Command | Description |
|---------|-------------|
| `datacore search QUERY` | Hybrid keyword + semantic search across the entire catalog |
| `datacore domains` | List all data domains (equity, macro, alternative, ...) |
| `datacore products DOMAIN` | List products within a domain |
| `datacore datasets` | List datasets — filter with `--product PRODUCT_ID` |

### Inspection

| Command | Description |
|---------|-------------|
| `datacore meta DATASET_ID` | Full dataset metadata as JSON |
| `datacore schema DATASET_ID` | Column-level schema: name, type, description |
| `datacore sample DATASET_ID` | Stream preview rows (default: 10, change with `-n N`) |

### Download

| Command | Description |
|---------|-------------|
| `datacore get DATASET_ID` | Download to CSV or Parquet — required: `--output FILE` |

Options for `get`:

```
--start DATE    Start date (ISO 8601, e.g. 2024-01-01)
--end   DATE    End date   (ISO 8601)
--output FILE   Destination file (.csv or .parquet)
--format FMT    Override output format
```

### Configuration

| Command | Description |
|---------|-------------|
| `datacore config show` | Dump the active config (file + env merged) |
| `datacore config set KEY VALUE` | Persist a setting (api_key, base_url, output_dir, default_format) |
| `datacore config get KEY` | Read a single setting |

### Integrations

| Command | Description |
|---------|-------------|
| `datacore mcp` | Write the DataCore entry into Claude Desktop's MCP config |
| `datacore version` | Print the installed CLI version |

---

## Output formats

Pass `--format` to any tabular command:

| Format | Flag | Notes |
|--------|------|-------|
| Table (default) | `--format table` | Rich-formatted, colour terminal output |
| JSON | `--format json` | One JSON object per line (NDJSON) |
| CSV | `--format csv` | Comma-separated, UTF-8 |
| Parquet | `--format parquet` | Columnar binary — best for large datasets |

---

## Examples

### Search and download VN30 OHLCV

```bash
# Discover available equity datasets
datacore search "VN30 OHLCV"
datacore schema equity.vn30.daily

# Download two years of daily data
datacore get equity.vn30.daily \
  --start 2022-01-01 \
  --end   2023-12-31 \
  --output vn30_2y.parquet
```

### Explore macroeconomic indicators

```bash
datacore domains
datacore products macro
datacore datasets --product macro-vn
datacore sample macro.vn.cpi -n 20
```

### Pipe JSON into jq

```bash
datacore meta equity.vn30.daily --format json | jq '.fields[].name'
```

### Use in a Python script

```python
import subprocess, json

result = subprocess.run(
    ["datacore", "meta", "equity.vn30.daily", "--format", "json"],
    capture_output=True, text=True
)
meta = json.loads(result.stdout)
```

---

## Python SDK

`datacore-cli` is built on the [DataCore Python SDK](https://github.com/DataCore-VietNam/DataCore), which you can use directly for programmatic access:

```python
from datacore import Datacore

client = Datacore(api_key="dc_...")
df = client.get_data("equity.vn30.daily", columns=["date", "close_price"])["data"]
```

See the [SDK docs](https://docs.datacore.vn/python) for the full API reference.

---

## Claude Desktop / MCP integration

`datacore-cli` ships a built-in MCP server that connects Claude Desktop to your DataCore account. Run:

```bash
export DATACORE_API_KEY=dc_...
datacore mcp
```

This writes the DataCore entry into `claude_desktop_config.json`. Restart Claude Desktop — you can then ask Claude to query DataCore datasets directly in conversation.

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

Quick start:

```bash
git clone https://github.com/DataCore-VietNam/datacore-cli
cd datacore-cli
pip install -e ".[dev]"
pre-commit install
pytest
```

---

## License

[MIT](LICENSE) © [DataCore Vietnam](https://datacore.vn)
