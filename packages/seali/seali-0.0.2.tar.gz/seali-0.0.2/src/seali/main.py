# ruff: noqa: D415, UP007, D103
"""CLI interface for kfactory.

Use `sea --help` for more info.
"""
from __future__ import annotations

import typer

from .typer.data import data
from .typer.project import project

__version__ = "0.0.1"

app = typer.Typer(
    help="CLI to interact with a GDataSea instance (default at https://localhost:3131)"
)


@app.callback(invoke_without_command=True)
def version_callback(
    version: bool = typer.Option(False, "--version", help="Show version of the CLI")
) -> None:
    """Show the version of the cli."""
    if version:
        print(f"GDataSea CLI Version: {__version__}")
        raise typer.Exit()


app.add_typer(
    project, name="project", help="Commands to interact with a gdatasea project"
)
app.add_typer(
    data, name="data", help="Commands to interact with a gdatasea device data"
)
