# ruff: noqa: D415, UP007, D103
"""CLI interface for GDataSea."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import klayout.db as kdb
import requests
import rich

from seali.config import CONF

__version__ = "0.0.1"

"""CLI interface for gdatasea.

Use `sea --help` for more info.
"""

base_url = CONF.url


def create(
    file: str | Path,
    lyp_file: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    base_url: str = base_url,
    top_cell: list[str] | None = None,
    wildcards: list[str] | None = None,
) -> requests.Response:
    """Upload a new project to gdatasea.

    Args:
        file: Path to the eda file (.gds or .oas) to upload.
        lyp_file: Path to the Klayout layer properties lyp file to upload.
        name: Name of the project. If not given, the name of the top-cell.
        description: Description of the project.
        base_url: Base url of the gdatasea server.
        top_cell: Tuple of top-cells to upload. If not given, all top-cells.
        wildcards: Tuple of wildcards to use for each top-cell. If not given, no

    """
    top_cell = top_cell or []
    wildcards = wildcards or []
    lw = len(wildcards)
    ltc = len(top_cell)
    if lw > ltc:
        raise ValueError("Cannot define wildcards without an associated top-cell")

    tc_wcs: list[dict[str, list[str] | str]] = []

    for i, tc in enumerate(top_cell):
        if i < lw:
            wcs = wildcards[i]
            if "," in wcs:
                tc_wcs.append(
                    {
                        "parent_cell_name": tc,
                        "wildcards": [wc.strip() for wc in wcs.split(",")],
                    }
                )
            else:
                tc_wcs.append(
                    {
                        "parent_cell_name": tc,
                        "wildcards": [wc.strip() for wc in wcs.split()],
                    }
                )
        else:
            tc_wcs.append(
                {
                    "parent_cell_name": tc,
                    "wildcards": [],
                }
            )

    if name is None:
        ly = kdb.Layout()
        ly.read(str(file))
        assert len(ly.top_cells()) > 0, (
            "Cannot automatically determine name of gdatasea edafile if"
            " there is no name given and the gds is empty"
        )
        name = ly.top_cells()[0].name

    url = f"{base_url}/project"
    params = {"name": name}
    data: dict[str, str] = {}
    if description:
        params["description"] = description
    if tc_wcs:
        data["cell_wildcards"] = ",".join([json.dumps(tc_wc) for tc_wc in tc_wcs])

    fp = Path(file).expanduser().resolve()
    assert (
        fp.exists() and fp.is_file()
    ), f"{fp.resolve()} doesn't exists or is not a file"
    with open(fp, "rb") as f:
        if lyp_file:
            lp = Path(lyp_file)
            if lp.is_file():
                with open(lp, "rb") as lf:
                    return requests.post(
                        url,
                        params=params,
                        files={"eda_file": f, "lyp_file": lf},
                        data=data,
                    )
            else:
                rich.print(
                    f"[yellow]Warning:[/yellow] lyp file {str(lp.resolve())}"
                    " is non-existent or not a file. Skipping lyp"
                )
        return requests.post(url, params=params, files={"eda_file": f}, data=data)


def delete(
    project_name: str,
    base_url: str = base_url,
) -> requests.Response:
    url = f"{base_url}/project/{project_name}"
    return requests.delete(url)


def download_edafile(
    project_name: str,
    base_url: str = base_url,
) -> requests.Response:
    url = f"{base_url}/project/{project_name}"
    return requests.get(url)


def download_lyp(
    project_name: str,
    base_url: str = base_url,
) -> requests.Response:
    url = f"{base_url}/project/{project_name}/lyp_file"
    return requests.get(url)
