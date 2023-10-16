"""
Plots of IR energies.

:func:`ir_energy_hist` plots a histogram of the IR energies for the different status categories.
"""

import logging
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from timewise.wise_data_base import WISEDataBase

from timewise_sup.plots import plots_dir
from timewise_sup.meta_analysis.ir_energy import get_ir_energy_status
from timewise_sup.mongo import Status


logger = logging.getLogger(__name__)


def ir_energy_hist(
        base_name: str,
        database_name: str,
        status: Status,
        wise_data: WISEDataBase | None = None,
):
    """
    Plots a histogram of the IR energies for the different status categories. The IR energies are calculated using
    :func:`timewise_sup.meta_analysis.ir_energy.get_ir_energy_status`.
    """
    logger.info("plotting bolometric luminosities histogram")

    if isinstance(status, str):
        status = [status]

    fig, ax = plt.subplots()

    lums = list()
    for s in status:
        df = pd.DataFrame.from_dict(get_ir_energy_status(base_name, database_name, s, wise_data), orient="index")
        df["status"] = s
        lums.append(df)

    lums_df = pd.concat(lums)
    pos_mask = lums_df["ir_energy_erg"] > 0

    sns.histplot(
        data=lums_df[pos_mask],
        x="ir_energy_erg",
        hue="status",
        log_scale=True,
        ax=ax,
        kde=True,
        stat="density",
        common_norm=False,
    )

    ax.set_xlabel("IR energy [erg]")
    ax.set_ylabel("density")
    ax.grid(ls=":", zorder=10, alpha=0.5)

    for loc in ["top", "right"]:
        ax.spines[loc].set_visible(False)

    fn = os.path.join(plots_dir("ir_energy", base_name), "ir_energy_hist.pdf")
    logger.debug(f"writing {fn}")
    fig.savefig(fn, bbox_inches="tight")
    plt.close()
