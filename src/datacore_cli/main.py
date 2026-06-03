"""DataCore CLI — main entrypoint."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="datacore",
    help="DataCore — Vietnamese financial and alternative data, from your terminal.",
    no_args_is_help=True,
)
console = Console()


def _client():
    from datacore import Datacore
    return Datacore()


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(10, "--limit", "-n", help="Max results"),
):
    """Hybrid keyword + semantic search across the catalog."""
    results = _client().search(query, limit=limit)
    table = Table(title=f"Search: {query!r}")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Domain", style="magenta")
    for r in results:
        table.add_row(r.get("id", ""), r.get("name", ""), r.get("domain", ""))
    console.print(table)


@app.command()
def domains():
    """List all data domains."""
    items = _client().list_domains()
    table = Table(title="Domains")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Description")
    for d in items:
        table.add_row(d.get("id", ""), d.get("name", ""), d.get("description", ""))
    console.print(table)


@app.command()
def products(domain: str = typer.Argument(..., help="Domain ID")):
    """List products within a domain."""
    items = _client().list_products(domain)
    table = Table(title=f"Products in {domain}")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    for p in items:
        table.add_row(p.get("id", ""), p.get("name", ""))
    console.print(table)


@app.command()
def datasets(product: Optional[str] = typer.Option(None, "--product", "-p")):
    """List datasets, optionally filtered by product."""
    items = _client().list_datasets(product=product)
    table = Table(title="Datasets")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    for d in items:
        table.add_row(d.get("id", ""), d.get("name", ""))
    console.print(table)


@app.command()
def meta(dataset_id: str = typer.Argument(...)):
    """Show full metadata for a dataset."""
    md = _client().dataset(dataset_id).metadata()
    console.print_json(data=md)


@app.command()
def schema(dataset_id: str = typer.Argument(...)):
    """Show column-level schema."""
    cols = _client().dataset(dataset_id).schema()
    table = Table(title=f"{dataset_id} — schema")
    table.add_column("Column", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Description")
    for c in cols:
        table.add_row(c.get("name", ""), c.get("type", ""), c.get("description", ""))
    console.print(table)


@app.command()
def sample(
    dataset_id: str = typer.Argument(...),
    n: int = typer.Option(10, "--n", "-n"),
):
    """Stream preview rows from a dataset."""
    for row in _client().dataset(dataset_id).sample(n=n):
        console.print_json(data=row)


@app.command()
def get(
    dataset_id: str = typer.Argument(...),
    start: Optional[str] = typer.Option(None, "--start"),
    end: Optional[str] = typer.Option(None, "--end"),
    output: Path = typer.Option(..., "--output", "-o", help="Output file (.csv or .parquet)"),
):
    """Download a dataset to local disk."""
    df = _client().dataset(dataset_id).to_pandas(start=start, end=end)
    if output.suffix == ".parquet":
        df.to_parquet(output, index=False)
    elif output.suffix == ".csv":
        df.to_csv(output, index=False)
    else:
        raise typer.BadParameter("Output must end in .csv or .parquet")
    console.print(f"[green]Wrote {len(df)} rows to {output}[/green]")


config_app = typer.Typer(help="Manage CLI configuration.", no_args_is_help=True)
app.add_typer(config_app, name="config")


@config_app.command("show")
def config_show():
    """Show current config (file + defaults merged)."""
    from datacore_cli import config as cfg_mod
    cfg = cfg_mod.load()
    cfg["config_file"] = str(cfg_mod.CONFIG_FILE)
    console.print_json(data=cfg)


@config_app.command("set")
def config_set(key: str = typer.Argument(...), value: str = typer.Argument(...)):
    """Set a config key."""
    from datacore_cli import config as cfg_mod
    cfg = cfg_mod.set_value(key, value)
    console.print(f"[green]Set {key}={value}[/green] → {cfg_mod.CONFIG_FILE}")


@config_app.command("get")
def config_get(key: str = typer.Argument(...)):
    """Get a single config value."""
    from datacore_cli import config as cfg_mod
    val = cfg_mod.get_value(key)
    if val is None:
        console.print(f"[yellow]{key} is not set[/yellow]")
        raise typer.Exit(1)
    console.print(val)


@app.command()
def mcp(
    output: Path = typer.Option(None, "--output", "-o"),
):
    """Write the DataCore entry into Claude Desktop's MCP config."""
    from datacore import write_claude_desktop_config
    api_key = os.environ.get("DATACORE_API_KEY")
    if not api_key:
        console.print("[red]DATACORE_API_KEY not set[/red]")
        raise typer.Exit(1)
    written = write_claude_desktop_config(api_key, path=output)
    console.print(f"[green]Wrote config to {written}[/green]")
    console.print("Restart Claude Desktop to pick it up.")


@app.command()
def version():
    """Show the installed CLI version."""
    from datacore_cli import __version__
    console.print(f"datacore-cli {__version__}")


if __name__ == "__main__":
    app()
