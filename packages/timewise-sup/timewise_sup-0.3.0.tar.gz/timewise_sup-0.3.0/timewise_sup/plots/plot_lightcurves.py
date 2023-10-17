"""
Plot single lightcurves or all lightcurves of a given status.

* :func:`plot_sample_lightcurves` plots all lightcurves of a given status
* :func:`plot_single_lightcurve` plots a single lightcurve
* :func:`make_lightcurve_plot` is the actual plotting function
"""

import os.path

import matplotlib.pyplot as plt
import matplotlib as mpl
import logging
import pandas as pd
from timewise.wise_data_base import WISEDataBase

from timewise_sup.meta_analysis.luminosity import nuFnu
from timewise_sup.meta_analysis.baseline_subtraction import get_single_lightcurve, get_baseline_subtracted_lightcurves
from timewise_sup.plots import plots_dir, bandcolors


logger = logging.getLogger(__name__)


def plot_sample_lightcurves(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        status: str,
        service: str = "tap",
        load_from_bigdata_dir: bool = False
):
    """
    Plot all lightcurves of a given status.

    :param base_name: base name of the analysis
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: WISE data object
    :type wise_data: WISEDataBase
    :param status: status of the lightcurves to plot
    :type status: str
    :func:`timewise_sup.meta_analysis.ztf.get_ztf_lightcurve` or
    :func:`timewise_sup.meta_analysis.ztf.download_ztffp_per_status` before
    :param service: serice with which the lightcurves were downloaded by ``timewise`` (default: ``tap``)
    :type service: str, optional
    :param load_from_bigdata_dir: whether to load the lightcurves from the bigdata directory (default: ``False``)
    :type load_from_bigdata_dir: bool, optional
    """
    wise_lcs = get_baseline_subtracted_lightcurves(
        base_name=base_name,
        database_name=database_name,
        wise_data=wise_data,
        status=status,
        service=service,
        load_from_bigdata_dir=load_from_bigdata_dir
    )

    for index, lc_dict in wise_lcs.items():
        logger.debug(f"index {index}")
        wise_lc = pd.DataFrame.from_dict(lc_dict)

        fig, ax = make_lightcurve_plot(wise_lc)

        d = plots_dir("baseline_subtracted_lightcurves", base_name)
        fn = os.path.join(d, status, f"{index}.pdf")

        d = os.path.dirname(fn)
        if not os.path.isdir(d):
            os.makedirs(d)

        logger.debug(f"saving under {fn}")
        fig.savefig(fn)
        plt.close()


def plot_single_lightcurve(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: str,
) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
    """
    Plot a single lightcurve.

    :param base_name: base name of the analysis
    :type base_name: str
    :param index: index of the lightcurve
    :type index: str
    :return: figure and axes
    :rtype: tuple[mpl.figure.Figure, mpl.axes.Axes]
    """

    wise_lc = get_single_lightcurve(
        base_name=base_name,
        database_name=database_name,
        wise_data=wise_data,
        index=index
    )

    return make_lightcurve_plot(wise_lc)


def make_lightcurve_plot(
        wise_lc: pd.DataFrame,
        unit: str = "erg s-1 cm-2"
) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
    """
    Make a lightcurve plot.

    :param wise_lc: The WISE lightcurve
    :type wise_lc: pd.DataFrame
    :param unit: unit of the flux density (default: ``erg s-1 cm-2``)
    :type unit: str, optional
    :return: figure and axes
    :rtype: tuple[mpl.figure.Figure, mpl.axes.Axes]
    """

    fig, ax = plt.subplots()

    for b in ["W1", "W2"]:
        ax.errorbar(
            wise_lc.mean_mjd,
            nuFnu(wise_lc[f"{b}_diff_mean_flux_density"], spectral_flux_density_unit="mJy", band=b, out_unit=unit),
            yerr=nuFnu(wise_lc[f"{b}_diff_flux_density_rms"], spectral_flux_density_unit="mJy", band=b, out_unit=unit),
            marker='s',
            ms=3,
            color=bandcolors[b],
            label=f"WISE {b}",
            ls="",
            zorder=5,
            capsize=2
        )

    ax.set_ylabel(r"$\nu$ F$_{\nu}$ [erg s$^{-1}$ cm$^{-2}$]")
    ax.grid()
    ax.legend()

    return fig, ax
