"""
Make a plot of the rise and fade times for all flares in the sample.

* :func:`make_rise_fade_time_plot` makes the plot
"""

import logging
import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from timewise_sup.plots import plots_dir, bandcolors, status_linestyle
from timewise_sup.mongo import DatabaseConnector


logger = logging.getLogger(__name__)


def make_rise_fade_time_plot(
        base_name: str,
        database_name: str
):
    """
    Make a plot of the rise and fade times for all flares in the sample.

    :param base_name: the base name of the sample
    :type base_name: str
    :param database_name: the name of the database
    :type database_name: str
    """
    logger.info("making rise/fade time plot")
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    ids = database_connector.get_ids(("1", "2"))

    status = database_connector.get_status(tuple(ids))
    rise_times = database_connector.get_rise_time(ids)
    fade_times = database_connector.get_fade_time(ids)
    data = pd.concat([status, np.log10(rise_times), np.log10(fade_times)], axis=1)

    fig, axs = plt.subplots(
        nrows=1, ncols=2, sharex="all", sharey="all",
        gridspec_kw={"hspace": 0, "wspace": 0},
        figsize=(3*2, 5)
    )
    for b, ax in zip(["W1", "W2"], axs):
        # logger.debug(f"band {b}, status {i_status}, n={len(data)}")
        for i_status in ["1", "2"]:
            d = data[(data["status"] == i_status)]
            logger.debug(f"band {b}, status {i_status}, n={len(d)}")
            sns.kdeplot(
                data=d,
                x=f"e_rise_{b}",
                y=f"e_fade_{b}",
                ax=ax,
                color=bandcolors[b],
                alpha=1,
                linestyles=status_linestyle[i_status],
                levels=3,
                fill=False,
                hatches=["\\\\", "///", "xxx"],
                label=i_status,
                zorder=2
            )

        if len(data) < 100:
            sns.scatterplot(
                data=data,
                x=f"e_rise_{b}",
                y=f"e_fade_{b}",
                ax=ax,
                style="status",
                color=bandcolors[b],
                zorder=1
            )

        ax.set_aspect("equal", adjustable="box")
        ax.grid(ls=":", zorder=10, alpha=0.5)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.legend()

    fig.supxlabel("rise time [log$_{10}$(days)]")
    fig.supylabel("fade time [log$_{10}$(days)]")
    fig.tight_layout()
    fn = os.path.join(plots_dir("rise_fade_times", base_name), "rise_fade_times.pdf")
    logger.info(f"saving under {fn}")
    fig.savefig(fn)
    plt.close()
