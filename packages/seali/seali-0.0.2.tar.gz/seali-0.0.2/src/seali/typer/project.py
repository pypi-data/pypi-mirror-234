# ruff: noqa: D415, UP007, D103
"""CLI interface for GDataSea. """
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import rich
import typer

from ..requests import project as project_req

__version__ = "0.0.1"

"""CLI interface for gdatasea.

Use `sea --help` for more info.
"""

project = typer.Typer()
download = typer.Typer()

project.add_typer(download, name="download")


@project.command("create", help="Create a new project on GDataSea")
def create(
    file: str = typer.Argument(
        help="EDA file to upload", rich_help_panel="Project Config", default=...
    ),
    lyp_file: Optional[str] = typer.Option(
        help="Layer properties file for project (.lyp)",
        default=None,
        rich_help_panel="Project Config",
    ),
    name: str = typer.Option(
        help="Project name", default=None, rich_help_panel="Project Config"
    ),
    description: Optional[str] = typer.Option(
        default=None, rich_help_panel="Project Config"
    ),
    base_url: str = typer.Option(
        envvar="GDATASEA_URL",
        rich_help_panel="GDataSea Config",
        default="http://localhost:3131",
        help="Base URL for GDataSea, e.g. https://gdatasea.example.com",
    ),
    top_cell: list[str] = typer.Option(
        help="Define one or more top cells to extract. Each top cell gets an "
        "associated list of wildcards (see --wildcards) for device extraction. "
        "If the number of wildcards lists is shorter than the list of top cells, "
        "the associated wildcards will be [], meaning no devices except the top "
        "cell device will be created",
        rich_help_panel="Device Extraction",
        default=[],
    ),
    wildcards: list[str] = typer.Option(
        help="Lists of (partial) cell names to extract as devices below the top"
        " cell. This is a string list separated by spaces or commas.",
        rich_help_panel="Device Extraction",
        default=[],
    ),
    browser: bool = typer.Option(
        False, "--open", help="Open project cell_view if successful"
    ),
) -> None:
    url = f"{base_url}/project"
    r = project_req.create(
        file=file,
        lyp_file=lyp_file,
        name=name,
        description=description,
        base_url=base_url,
        top_cell=top_cell,
        wildcards=wildcards,
    )
    # r = requests.post(url, params=params, files={"eda_file": f}, data=data)
    msg = f"Response from {url}: "
    try:
        msg += rich.pretty.pretty_repr(json.loads(r.text))
        msg = msg.replace("'success': 200", "[green]success: 200[/green]").replace(
            "422", "[red]422[/red]"
        )
    except json.JSONDecodeError:
        msg += rich.pretty.pretty_repr(f"[red]{r.text}[/red]")
    rich.print(msg)
    if r.status_code == 200 and browser:
        typer.launch(f"{base_url}/cell_view/{name}")


@project.command("delete", help="Delete a new project on GDataSea")
def delete(
    project_name: str = typer.Argument(default=...),
    confirm_deletion_of_project: bool = typer.Option(
        False,
        "--force",
        "-f",
        prompt=True,
        hidden=True,
        help="Delete the project truly?",
    ),
    base_url: str = typer.Option(
        envvar="GDATASEA_URL",
        rich_help_panel="GDataSea Config",
        default="http://localhost:3131",
        help="Base URL for GDataSea, e.g. https://gdatasea.example.com",
    ),
) -> None:
    if confirm_deletion_of_project:
        url = f"{base_url}/project/{project_name}"
        r = project_req.delete(project_name=project_name, base_url=base_url)
        msg = f"Response from {url}: "
        try:
            msg += rich.pretty.pretty_repr(json.loads(r.text))
            msg = msg.replace("'success': 200", "[green]success: 200[/green]").replace(
                "422", "[red]422[/red]"
            )
        except json.JSONDecodeError:
            msg += rich.pretty.pretty_repr(f"[red]{r.text}[/red]")
        rich.print(msg)
    else:
        rich.print(f"Aborting deletion of {project_name}")


@download.command("edafile", help="Download a project edafile")
def edafile(
    project_name: str = typer.Argument(default=...),
    base_url: str = typer.Option(
        envvar="GDATASEA_URL",
        rich_help_panel="GDataSea Config",
        default="http://localhost:3131",
        help="Base URL for GDataSea, e.g. https://gdatasea.example.com",
    ),
    output_file: str = typer.Option(
        None, "-o", "--output-file", help="Folder and filename to download the data to"
    ),
) -> None:
    r = project_req.download_edafile(project_name=project_name, base_url=base_url)
    filename = Path(
        output_file or r.headers["content-disposition"].split("; filename=")[1]
    )

    filename.resolve().parent.mkdir(parents=True, exist_ok=True)

    with filename.open("wb") as f:
        f.write(r.content)


@download.command("lypfile", help="Download a project edafile")
def lypfile(
    project_name: str = typer.Argument(default=...),
    base_url: str = typer.Option(
        envvar="GDATASEA_URL",
        rich_help_panel="GDataSea Config",
        default="http://localhost:3131",
        help="Base URL for GDataSea, e.g. https://gdatasea.example.com",
    ),
    output_file: str = typer.Option(
        None, "-o", "--output-file", help="Folder and filename to download the data to"
    ),
) -> None:
    r = project_req.download_lyp(project_name=project_name, base_url=base_url)
    filename = Path(
        output_file or r.headers["content-disposition"].split("; filename=")[1]
    )

    filename.resolve().parent.mkdir(parents=True, exist_ok=True)

    with filename.open("wb") as f:
        f.write(r.content)
