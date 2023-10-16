"""
Makes color-color plots for the WISE data.

* :func:`color_plot` makes a color-color plot given the wise data and a list of color keys in the parent sample.
* :func:`agn_box_plot` makes a color-color plot in the W1-W2 - W2-W3 plane and indicates the `AGN-Wedge`
"""

import logging
import os.path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import corner
import pandas as pd
from timewise import WISEDataDESYCluster

from timewise_sup.plots import plots_dir
from timewise_sup.meta_analysis.agn import add_agn_box, get_agn_mask_from_color
from timewise_sup.mongo import DatabaseConnector, Status


logger = logging.getLogger(__name__)


def color_plot(
        base_name: str,
        database_name: str,
        wise_data: WISEDataDESYCluster,
        color_keys: list[str],
        status: Status | None = None,
        colors: list[str] | None = None,
        level_sigma: list[float] | None = None,
        data: pd.DataFrame | None = None,
) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
    """
    Makes a color-color plot given the wise data and a list of color keys in the parent sample.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataDESYCluster
    :type wise_data: WISEDataDESYCluster
    :param color_keys: list of color keys in the parent sample (or ``data``)
    :type color_keys: list
    :param status: statuses to include in the plot, defaults to ``["1", "2"]``
    :type status: list, optional
    :param colors: colors to use for the different statuses, defaults to ``["k", "grey"]``
    :type colors: list, optional
    :param level_sigma: sigma levels for the contours, defaults to ``[1, 2, 5]``
    :type level_sigma: list, optional
    :param data: data to use for the plot, defaults to ``wise_data.parent_sample.df``
    :type data: pd.DataFrame, optional
    :return: figure and axes
    :rtype: tuple
    """

    if status is None:
        status = ["1", "2"]

    if colors is None:
        colors = ["k", "grey"]

    if level_sigma is None:
        level_sigma = [1, 2, 5]

    if data is None:
        data = wise_data.parent_sample.df
        data.set_index(data.index.astype(str), inplace=True)

    fig, axs = plt.subplots(
        ncols=len(color_keys),
        nrows=len(color_keys),
        figsize=[6, 6],
        sharex='all',
        sharey='all',
        gridspec_kw={"wspace": 0.1, "hspace": 0.1}
    )

    twinx = [None] * len(color_keys)

    for i_status, c in zip(status, colors):

        ids = DatabaseConnector(base_name=base_name, database_name=database_name).get_ids(i_status)

        for i in range(len(color_keys)):
            for j in range(i + 1, len(color_keys)):
                x = np.array(data.loc[list(ids), color_keys[i]])
                y = np.array(data.loc[list(ids), color_keys[j]])

                logger.debug(f"making corner plot: {color_keys[i]} ({len(x)}) - {color_keys[j]} ({len(y)})")
                nan_m = np.isnan(x) | np.isnan(y)
                logger.debug(f"removing {np.sum(nan_m)} NaNs")

                corner.hist2d(
                    x[~nan_m],
                    y[~nan_m],
                    ax=axs[j][i],
                    plot_density=False,
                    color="k",
                    data_kwargs={"color": c},
                    contour_kwargs={"colors": c},
                    levels=1.0 - np.exp(-0.5 * np.array(level_sigma) ** 2)
                )

                axs[i][j].axis('off')

            if twinx[i] is None:
                twinx[i] = axs[i][i].twinx()

            twinx[i].hist(  # type: ignore
                data.loc[ids, color_keys[i]],
                color=c,
                density=True,
                histtype='step',
                bins=100
            )

            axs[i][0].set_ylabel(color_keys[i])
            axs[-1][i].set_xlabel(color_keys[i])

    return fig, axs


def agn_box_plot(
        base_name: str,
        database_name: str,
        wise_data: WISEDataDESYCluster,
        status: Status | None = None,
        colors: list[str] | None = None,
        level_sigma: list[float] | None = None,
):
    """
    Makes a color-color plot in the W1-W2 - W2-W3 plane and indicates the `AGN-Wedge`
    `(Hvding et al. (2022) <https://iopscience.iop.org/article/10.3847/1538-3881/ac5e33)>`_.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataDESYCluster
    :type wise_data: WISEDataDESYCluster
    :param status: statuses to include in the plot, defaults to ``["1", "2"]``
    :type status: list, optional
    :param colors: colors to use for the different statuses, defaults to ``["g", "purple"]``
    :type colors: list, optional
    :param level_sigma: sigma levels for the contours, defaults to ``[1, 5]``
    :type level_sigma: list, optional
    """

    logger.info("Making AGN-box color plot")

    if status is None:
        status = ["1", "2"]

    if colors is None:
        colors = ["g", "purple"]

    if level_sigma is None:
        level_sigma = [1, 5]

    parent_sample = wise_data.parent_sample
    wise_mag_keys = ["W1_mag", "W2_mag", "W3_mag"]

    if np.any([k not in parent_sample.default_keymap for k in wise_mag_keys]):
        logger.warning(f"One of {','.join(wise_mag_keys)} not in ParentSample's default keymap: \n"
                       f"{parent_sample.default_keymap}.\n"
                       f"Not making AGN-Box plot.")
        return

    agn_mask, W1W2, W2W3 = get_agn_mask_from_color(base_name, wise_data)
    parent_sample.df["W1-W2"] = W1W2
    parent_sample.df["W2-W3"] = W2W3

    n_agn = dict()

    for istatus in status:
        ids = DatabaseConnector(base_name=base_name, database_name=database_name).get_ids(istatus)
        status_agns = agn_mask.loc[ids]
        in_agns = np.sum(status_agns) / len(status_agns)
        logger.info(f"Status {istatus}: {in_agns*100:.2f}% in AGN box")
        n_agn[istatus] = in_agns

    fig, axs = color_plot(
        base_name,
        database_name,
        wise_data,
        status=status,
        colors=colors,
        color_keys=['W2-W3', 'W1-W2'],
        level_sigma=level_sigma,
        data=parent_sample.df
    )

    axs[0][0].set_xlim(-1, 7)
    axs[0][0].set_ylim(-1, 3)

    add_agn_box(axs[1][0])
    axs[1][0].legend()

    lines = [mpl.lines.Line2D([0], [0], color=c) for c in colors]
    labels = [f"{s} ({n_agn[s] * 100:.0f}% in AGN box)" for s in status]
    fig.legend(lines, labels, loc='lower left', fontsize="medium", bbox_to_anchor=(0.56, 0.56))

    fn = os.path.join(plots_dir("color_plots", base_name), "agn_box.pdf")
    logger.debug(f"saving under {fn}")
    fig.savefig(fn)

    plt.close()
