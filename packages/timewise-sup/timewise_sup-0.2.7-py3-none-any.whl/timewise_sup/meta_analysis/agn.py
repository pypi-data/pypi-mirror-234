"""
This module contains functions for identifying AGN in WISE data.

* :func:`get_agn_mask_from_color` uses the WISE color-color diagram from Hviding et al. (2022) to identify AGN
* :func:`add_agn_box` adds the AGN selection box from Hviding et al. (2022) to a plot
* :func:`get_agn_mask_from_variability` uses the variability in the IR lightcurves to identify AGN
"""

import matplotlib as mpl
import logging
import pandas as pd
from timewise.wise_data_base import WISEDataBase

from timewise_sup.mongo import DatabaseConnector


logger = logging.getLogger(__name__)


# taken from Hviding et al. (2022)
# https://iopscience.iop.org/article/10.3847/1538-3881/ac5e33
agn_box: dict[str, list] = {
    "W2-W3": [1.734, 3.916],
    "W1-W2 / W2-W3 parameters": [
        [0.0771, 0.319],
        [0.261, -0.260],
    ]
}


def get_agn_mask_from_color(
        base_name: str,
        wise_data: WISEDataBase
) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Get the AGN mask based on the WISE color-color diagram from Hviding et al. (2022)

    :param base_name: the base name of the WISE data
    :type base_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :return: the AGN mask, the W1-W2 color, and the W2-W3 color
    :rtype: tuple[pd.DataFrame, pd.Series, pd.Series]
    """
    logger.info(f"getting agn mask for {base_name}")
    parent_sample = wise_data.parent_sample

    wise_mag_keys = ["W1_mag", "W2_mag", "W3_mag"]
    mag_keys = {b: parent_sample.default_keymap[b] for b in wise_mag_keys}
    logger.debug(f"WISE filter mag keys are {mag_keys}")
    parent_sample.df["W1-W2"] = parent_sample.df[mag_keys["W1_mag"]] - parent_sample.df[mag_keys["W2_mag"]]
    parent_sample.df["W2-W3"] = parent_sample.df[mag_keys["W2_mag"]] - parent_sample.df[mag_keys["W3_mag"]]

    W1W2 = parent_sample.df["W1-W2"]
    W2W3 = parent_sample.df["W2-W3"]
    agn_mask = (
            (W2W3 > agn_box["W2-W3"][0]) &
            (W2W3 < agn_box["W2-W3"][1]) &
            (W1W2 > agn_box["W1-W2 / W2-W3 parameters"][0][0] * W2W3 + agn_box["W1-W2 / W2-W3 parameters"][0][1]) &
            (W1W2 > agn_box["W1-W2 / W2-W3 parameters"][1][0] * W2W3 + agn_box["W1-W2 / W2-W3 parameters"][1][1])
    )

    return agn_mask, W1W2, W2W3


def add_agn_box(
        ax: mpl.axes.Axes,
):
    """
    Add the AGN selection box from Hviding et al. (2022) to a plot

    :param ax: the axis to add the box to
    :type ax: mpl.axes.Axes
    """
    logger.info("adding AGN wedge to plot")
    agn_box_style = {
        "lw": 2,
        "ls": ":",
        "color": "k"
    }

    # store axis limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # calculate the point where the agn wedge lines meet
    x = [
        agn_box["W2-W3"][0],
        agn_box["W2-W3"][0],
        -(agn_box["W1-W2 / W2-W3 parameters"][0][1] - agn_box["W1-W2 / W2-W3 parameters"][1][1]) /
        (agn_box["W1-W2 / W2-W3 parameters"][0][0] - agn_box["W1-W2 / W2-W3 parameters"][1][0]),
        agn_box["W2-W3"][1],
        agn_box["W2-W3"][1],
    ]
    y = [
        1e3,
        agn_box["W1-W2 / W2-W3 parameters"][0][0] * x[1] + agn_box["W1-W2 / W2-W3 parameters"][0][1],
        agn_box["W1-W2 / W2-W3 parameters"][0][0] * x[2] + agn_box["W1-W2 / W2-W3 parameters"][0][1],
        agn_box["W1-W2 / W2-W3 parameters"][1][0] * x[3] + agn_box["W1-W2 / W2-W3 parameters"][1][1],
        1e3
    ]
    logger.debug(f"x: {x}")
    logger.debug(f"y: {y}")

    ax.plot(x, y, label="Hviding et al. (2022)", **agn_box_style)

    # reset axis limits
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


def get_agn_mask_from_variability(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
) -> pd.DataFrame:
    """
    Get the AGN mask based on the variability in the IR lightcurves.

    :param base_name: the base name of the WISE data
    :type base_name: str
    :param database_name: the name of the database to get the variability stocks from
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :return: the AGN mask
    :rtype: pd.DataFrame
    """
    logger.info(f"getting AGN mask based on variability")
    stocks = DatabaseConnector(base_name=base_name, database_name=database_name).get_agn_variability_stocks()
    logger.debug(f"got {len(stocks)}, making mask")
    mask = pd.DataFrame(
        {"variability_agn_mask": wise_data.parent_sample.df.index.isin(stocks)},
        index=wise_data.parent_sample.df.index
    )
    return mask
