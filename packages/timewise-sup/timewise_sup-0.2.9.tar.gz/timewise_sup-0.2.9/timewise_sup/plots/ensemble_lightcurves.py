"""
Plot all lightcurves for a given status for all flares in a given sample.

* :func:`make_lightcurves_ensemble_plot` makes a plot of the ensemble lightcurves for a given status.
"""

import logging
import os
import matplotlib.pyplot as plt
from astropy.time import Time
import numpy as np
from timewise import WISEDataDESYCluster

from timewise_sup.samples.sjoerts_flares import get_test_flares_config, sjoerts_base_name, sjoerts_database_name
from timewise_sup.meta_analysis.baseline_subtraction import get_baseline_subtracted_lightcurves, get_lightcurves
from timewise_sup.mongo import DatabaseConnector, Index, Status
from timewise_sup.plots import plots_dir


logger = logging.getLogger(__name__)


def make_lightcurves_ensemble_plot(
        base_name: str,
        database_name: str,
        wise_data: WISEDataDESYCluster,
        status: Status
):
    """
    Make a plot of all lightcurves for a given status.

    :param base_name: base name of the sample
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataDESYCluster
    :type wise_data: WISEDataDESYCluster
    :param status: status to plot
    :type status: Status
    """
    logger.info(f"making ensemble plot for {base_name} in {database_name} (status {status})")

    # get difference photometry lightcurves
    diff_lcs = get_baseline_subtracted_lightcurves(base_name, database_name, wise_data, status)

    # get peak times
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    sample_ids = database_connector.get_ids(status)
    peak_t = database_connector.get_peak_time_jd(sample_ids)
    # move to MJD
    for b in peak_t.columns:
        peak_t[f"{b}_mjd"] = Time(peak_t[b], format="jd").mjd

    # try to get flares from https://arxiv.org/abs/2111.09391
    sjoerts_sample = get_test_flares_config().wise_data
    m = np.array([n in ["AT2019dsg"] for n in sjoerts_sample.parent_sample.df.name])
    sjoert_ids = list(sjoerts_sample.parent_sample.df.index[m])
    sjoert_lcs = get_lightcurves(sjoerts_base_name, sjoerts_database_name, sjoerts_sample, sjoert_ids)
    sjoerts_connector = DatabaseConnector(base_name=sjoerts_base_name, database_name=sjoerts_database_name)
    sjoerts_peaks = sjoerts_connector.get_peak_time_jd(sjoert_ids)

    # make plot

    e = list()
    fig, axs = plt.subplots(
        nrows=2,
        sharex="all",
        figsize=[5, 7],
        sharey="all",
        gridspec_kw={"hspace": 0}
    )

    for f, ax in zip(["W1", "W2"], axs):
        logger.debug(f"plotting {f}")

        for i, (k, v) in enumerate(diff_lcs.items()):

            try:
                ipeak = peak_t.loc[k, f"max_mag_jd_{f}_mjd"]
                mjds = np.array(list(v["mean_mjd"].values()))
                diff_f = np.array(list(v[f"{f}_diff_mean_flux_density"].values()))
                label = f"AIR-FLARES (status {status})" if i == 0 else ""
                ax.plot(mjds - ipeak, diff_f, color="grey", marker="", alpha=0.1, label=label)

            except KeyError:
                e.append(k)

        for k, v in sjoert_lcs.items():
            ipeak = Time(sjoerts_peaks.loc[k, f"max_mag_jd_{f}"], format='jd').mjd
            mjds = np.array(list(v["mean_mjd"].values()))
            diff_f = np.array(list(v[f"{f}_diff_mean_flux_density"].values()))
            diff_f_e = np.array(list(v[f"{f}_diff_flux_density_rms"].values()))
            name = sjoerts_sample.parent_sample.df.loc[int(k), "name"]
            logger.debug(name)

            ax.errorbar(
                mjds - ipeak,
                diff_f,
                yerr=diff_f_e,
                marker="s",
                ms=3,
                capsize=2,
                label=name,
                ls=":"
            )

        ax.grid(":")
        ax.set_ylabel(f)

    if len(e) > 0:
        logger.warning(f"l{len(e)} KeyErrors! {e}")

    axs[0].legend()
    axs[0].set_ylim(1e-2, 80)
    axs[0].set_xlim(-1000, 1000)
    axs[0].set_yscale("log")
    axs[-1].set_xlabel("days from IR peak")
    fig.text(0.0, 0.5, r"$\nu$ F$_\nu$ [erg s$^{-1}$ cm$^{-2}$]", va='center', rotation='vertical')

    fn = os.path.join(plots_dir("ensemble_lightcurves", base_name), f"ensemble_lightcurves_status{status}.pdf")
    logger.info(f"saving under {fn}")
    fig.tight_layout()
    fig.savefig(fn)
    plt.close()
