# ruff: noqa: D415, UP007, D103
"""CLI interface for SeaLI.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal, TypeAlias

import pydantic
import requests

from seali.config import CONF

JSONDict: TypeAlias = "dict[str, int | float | str | JSONDict]"

__version__ = "0.0.1"

"""CLI interface for gdatasea.

Use `sea --help` for more info.
"""

base_url = CONF.url


class PlottingKwargs(pydantic.BaseModel):
    x_col: str
    y_col: list[str]
    x_name: str
    y_name: str
    scatter: bool = False
    x_units: str | None = None
    y_units: str | None = None
    x_log_axis: bool = False
    y_log_axis: bool = False
    x_limits: tuple[int, int] | None = None
    y_limit: tuple[int, int] | None = None
    sort_by: dict[str, bool] | None = None
    grouping: dict[str, int] | None = None


def upload(
    file: str | Path,
    project_name: str,
    device_name: str,
    base_url: str = base_url,
    data_type: Literal["simulation", "measurement"] = "measurement",
    meta: dict[str, str | int | float] | None = None,
    plotting_kwargs: PlottingKwargs | None = None,
    wafer_name: str | None = None,
    die_x: str | None = None,
    die_y: str | None = None,
) -> requests.Response:
    """Upload a new project to gdatasea.

    Args:
        file: Path to the file to upload.
        project_name: Name of the project to upload to.
        device_name: Name of the device to upload to.
        base_url: Base URL of the gdatasea server.
        data_type: Type of data to upload. Either "simulation" or "measurement".
        meta: Meta data to upload with the file.
        plotting_kwargs: Plotting kwargs to upload with the file.
        wafer_name: Name of the wafer to upload to.
        die_x: X coordinate of the die to upload to.
        die_y: Y coordinate of the die to upload to.

    """
    url = f"{base_url}/device_data/"
    # params = {"name": name}
    # data: dict[str, str] = {}
    # if description:
    #     params["description"] = description
    # if tc_wcs:
    #     data["cell_wildcards"] = ",".join([json.dumps(tc_wc) for tc_wc in tc_wcs])

    meta = meta or {}

    params = {
        "project_name": project_name,
        "device_name": device_name,
        "data_type": data_type,
    }
    data: JSONDict = {}

    if meta:
        data["meta"] = meta  # type: ignore
    if plotting_kwargs:
        data["plotting_kwargs"] = plotting_kwargs.model_dump()

    fp = Path(file).expanduser().resolve()
    assert (
        fp.exists() and fp.is_file()
    ), f"{fp.resolve()} doesn't exists or is not a file"
    with open(fp, "rb") as f:
        return requests.post(url, params=params, files={"data_file": f}, data=data)


# def delete(
#     project_name: str,
#     base_url: str = os.getenv("GDATASEA_URL") or "http://localhost:3131",
# ) -> requests.Response:
#     url = f"{base_url}/project/{project_name}"
#     r = requests.delete(url)
#     return r


def download(
    project_name: str,
    base_url: str = base_url,
    cell_name: str | None = None,
    device_name: str | None = None,
    wafer_name: str | None = None,
    die_x: str | None = None,
    die_y: str | None = None,
    data_type: Literal["simulation", "measurement"] = "measurement",
) -> requests.Response:
    """Download a project from gdatasea.

    Args:
        project_name: Name of the project to download.
        base_url: Base URL of the gdatasea server.
        cell_name: Name of the cell to download.
        device_name: Name of the device to download.
        wafer_name: Name of the wafer to download.
        die_x: X coordinate of the die to download.
        die_y: Y coordinate of the die to download.
        data_type: Type of data to download. Either "simulation" or "measurement".

    """
    url = f"{base_url}/device_data/{project_name}/data_files"

    params = {}
    if cell_name:
        params["cell_name"] = cell_name
    if device_name:
        params["device_name"] = device_name
    if wafer_name:
        params["wafer_name"] = wafer_name
    if die_x:
        params["die_x"] = die_x
    if die_y:
        params["die_y"] = die_y
    if data_type:
        params["data_type"] = data_type

    return requests.get(url=url, params=params)
