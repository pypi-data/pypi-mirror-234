"""
This module contains functions to make diagnostic plots of the ``AMPEL`` run.

* :func:`chunk_distribution_plots` plots the number of analysed objects and the distribution of statuses among chunks.
* :func:`positional_outliers` plots the times of positional outliers.
"""

import logging
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.time import Time
from timewise.wise_data_base import WISEDataBase

from timewise_sup.plots import plots_dir
from timewise_sup.meta_analysis.diagnostics import (
    get_statuses_per_chunk,
    get_catalog_matches_per_chunk,
    get_positional_outliers_times
)


logger = logging.getLogger(__name__)


def chunk_distribution_plots(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase
):
    """
    Make diagnostic plots of the chunk distribution. This includes the number of analysed objects per chunk and the
    distribution of statuses among chunks.

    :param base_name: base name of the analysis
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    """
    logger.info(f"making chunk distribution diagnostic plots for {base_name}")
    d = plots_dir("diagnostics", base_name)

    # --- plot analyses stocks per chunk ---#

    statuses = get_statuses_per_chunk(base_name, database_name, wise_data)

    logger.info("plotting number of analysed objects")
    n_stocks = {c: len(v) for c, v in statuses.items()}
    fig, ax = plt.subplots()
    ax.bar(np.array(list(n_stocks.keys())).astype(int), n_stocks.values())
    ax.set_xlabel("chunk number")
    ax.set_ylabel("# of analysed objects")
    for loc in ["top", "right"]:
        ax.spines[loc].set_visible(False)

    ax.grid(ls=":", alpha=0.5)

    fig.tight_layout()
    fn = os.path.join(d, "number_per_chunk.pdf")
    logger.debug(f"saving under {fn}")
    fig.savefig(fn)
    plt.close()

    # --- plot distribution of statuses among chunks ---#

    logger.info("plotting status distribution among chunks")
    _unique_statuses = [
        "1",
        "1_maybe_interesting",
        "2",
        "2_maybe_interesting",
        "3",
        "3_maybe_interesting",
        "4",
        "4_maybe_interesting",
        "No further investigation"
    ]

    n_status = dict()
    for s in _unique_statuses:
        logger.debug(f"getting # of objects for {s}")
        in_status = dict()
        for c, istatus in statuses.items():
            in_status[c] = np.sum(np.array(istatus) == s)

        n_status[s] = in_status

    for s, in_status in n_status.items():
        logger.debug(f"plotting {s}")
        fig, ax = plt.subplots()
        ax.bar(np.array(list(in_status.keys())).astype(int), list(in_status.values()))
        ax.grid(ls=":", alpha=0.5)
        ax.set_xlabel("chunk number")
        ax.set_ylabel("# of objects")
        ax.set_title(s)
        for loc in ["top", "right"]:
            ax.spines[loc].set_visible(False)

        fig.tight_layout()
        fn = os.path.join(d, f"number_per_chunk_status_{s}.pdf")
        logger.debug(f"saving under {fn}")
        fig.savefig(fn)
        plt.close()

    # --- plot distribution of catalogue matches among chunks --- #

    number_of_catalogue_matches = pd.DataFrame.from_dict(
        get_catalog_matches_per_chunk(base_name, database_name, wise_data),
        orient="index"
    ).fillna(0)

    fig, ax = plt.subplots()

    bottom = None
    for i, c in enumerate(number_of_catalogue_matches.columns):
        bottom = (
            0 if i == 0 else
            bottom + number_of_catalogue_matches[number_of_catalogue_matches.columns[i - 1]]
        )
        ax.bar(
            number_of_catalogue_matches.index,
            number_of_catalogue_matches[c],
            bottom=bottom,
            label=c
        )

    for loc in ["top", "right"]:
        ax.spines[loc].set_visible(False)

    ax.grid(ls=":", alpha=0.5)
    ax.legend()
    ax.set_xlabel("chunk number")
    ax.set_ylabel("number of matches")

    fig.tight_layout()
    fn = os.path.join(d, f"number_of_catalog_matches_per_chunk.pdf")
    logger.debug(f"saving under {fn}")
    fig.savefig(fn)
    plt.close()


def positional_outliers(
        base_name: str,
        wise_data: WISEDataBase
):
    """
    Plot the times of positional outliers (see :func:`get_positional_outliers_times`).
    """
    logger.info("plotting times of positional outliers")
    mjds_per_chunk = get_positional_outliers_times(base_name, wise_data)

    ic = 0.9

    data = np.array([
        [c] + list(np.quantile(mjds, [0.5, 0.5 - ic / 2, 0.5 + ic / 2]))
        for c, mjds in mjds_per_chunk.items()
    ])

    # -------- make plot --------- #

    fig, ax = plt.subplots()
    color = "r"
    lw = 2
    ax.plot(data[:, 0], data[:, 1], color=color, ls="-", label="median", lw=lw)
    ax.plot(data[:, 0], data[:, 2], color=color, ls="--", label="IC$_{" + f"{ic*100:.0f}" + "}%$", lw=lw)
    ax.plot(data[:, 0], data[:, 3], color=color, ls="--", lw=lw)
    ax.axhline(Time("2011-02-01").mjd, ls=":", label="WISE decommissioned")
    ax.axhline(Time("2013-09-01").mjd, ls=":", label="WISE reactivated")

    ax.set_xlabel("chunk number")
    ax.set_ylabel("MJD")
    ax.grid(ls=":", alpha=0.5)

    fig.tight_layout()
    fn = os.path.join(plots_dir("diagnostics", base_name), f"positional_outliers_times.pdf")
    logger.info(f"saving under {fn}")
    fig.savefig(fn)
    plt.close()
