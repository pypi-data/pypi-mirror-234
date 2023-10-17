# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: base
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Simulation data
#
# You can easily upload and download measurement or simulation data.
#
#
# ## Sparameters

# %%
import seali as sea

from seali.typer.data import download
from pathlib import Path
import json
import gzip
import matplotlib.pyplot as plt

# %%

output_file = sea.PATH.repo / "extra" / "CHIPLET1_mzi_test_DL10_711500_60500.tar.gz"
dirpath = output_file.parent
dirpath.mkdir(parents=True, exist_ok=True)

download(
    project_name="MZI_CHIP",
    device_name="CHIPLET1_mzi_test_DL10_711500_60500",
    base_url=sea.CONF.url,
    output_file=output_file,
    data_type="simulation",
)

# %%
import tarfile

with tarfile.open(output_file, "r:gz") as tar:
    tar.extractall(path=sea.PATH.repo / "extra")

# %%
import pandas as pd
import numpy as np

# %%
dirpath = output_file.parent
xkey = "wavelengths"

for filepath in dirpath.glob("*.json.gz"):
    plt.figure()
    plt.title(filepath.stem)
    data = gzip.open(filepath).read()
    df = pd.DataFrame(**json.loads(data))
    for key in df.keys():
        if key.endswith("m"):
            plt.plot(df[xkey], 10 * np.log10(df[key]), label=key)
    plt.legend()


# %%
df.head()

# %%
