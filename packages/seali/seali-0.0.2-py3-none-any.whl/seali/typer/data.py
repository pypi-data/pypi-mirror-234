# ruff: noqa: D415, UP007, D103
"""CLI interface for GDataSea."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from seali.config import CONF

from ..requests import data as data_req

__version__ = "0.0.1"

"""CLI interface for gdatasea.

Use `sea --help` for more info.
"""
data = typer.Typer()


@data.command("download", help="Download a project device data and metadata")
def download(
    project_name: str = typer.Argument(default=...),
    base_url: str = typer.Option(
        envvar="GDATASEA_URL",
        rich_help_panel="GDataSea Config",
        default=CONF.url,
        help="Base URL for GDataSea, e.g. https://gdatasea.example.com",
    ),
    cell_name: Optional[str] = None,
    device_name: Optional[str] = None,
    wafer_name: Optional[str] = None,
    die_x: Optional[str] = None,
    die_y: Optional[str] = None,
    data_type: str = "measurement",
    output_file: str = typer.Option(
        ..., "-o", "--output-file", help="Folder and filename to download the data to"
    ),
) -> None:
    if data_type and data_type not in ["measurement", "simulation"]:
        raise ValueError("Only measurement or simulation are supported")
    r = data_req.download(
        project_name=project_name,
        base_url=base_url,
        cell_name=cell_name,
        device_name=device_name,
        wafer_name=wafer_name,
        die_x=die_x,
        die_y=die_y,
        data_type=data_type,  # type:ignore
    )
    # msg = f"Response from {url}: "
    # try:
    #     msg += rich.pretty.pretty_repr(json.loads(r.text))
    #     msg = msg.replace("'success': 200", "[green]success: 200[/green]").replace(
    #         "422", "[red]422[/red]"
    #     )
    # except json.JSONDecodeError:
    #     msg += rich.pretty.pretty_repr(f"[red]{r.text}[/red]")
    # rich.print(msg)
    r.raise_for_status()
    path = Path(output_file)
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as _f:
        _f.write(r.content)
    typer.launch(str(path))
