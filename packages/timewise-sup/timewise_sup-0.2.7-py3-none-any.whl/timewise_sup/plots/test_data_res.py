import logging
import pandas as pd
import matplotlib.pyplot as plt
from timewise import WISEDataDESYCluster
import numpy as np
import os

from timewise_sup.mongo import DatabaseConnector
from timewise_sup.plots import plots_dir


logger = logging.getLogger(__name__)


def get_red_chi2(
        wise_data: WISEDataDESYCluster,
) -> pd.DataFrame:
    logger.info(f"compiling red chi2 for {wise_data.base_name}")
    red_chi2_list = [
        wise_data.get_red_chi2(c, "_flux_density", use_bigdata_dir=True)
        for c in range(wise_data.n_chunks)
    ]
    logger.debug(f"loaded info for {len(red_chi2_list)} chunks")
    red_chi2_cit = {
        b: pd.concat([
            d[b][["chi2"]].rename(columns={"chi2": f"{b}_red_chi2"})
            for d in red_chi2_list
        ], axis=0)
        for b in wise_data.bands
    }
    red_chi2 = pd.concat(red_chi2_cit.values(), axis=1)
    red_chi2["pass_red_chi2_cut"] = (red_chi2["W1_red_chi2"] > 1) & (red_chi2["W2_red_chi2"] > 1)
    logger.info("done")
    return red_chi2


def get_res_info(
        base_name: str,
        database_name: str,
        wise_data: WISEDataDESYCluster
) -> pd.DataFrame:
    logger.info(f"getting result infos for {base_name}")
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    status = database_connector.get_status(wise_data.parent_sample.df.index)
    desc = database_connector.get_t2_dust_echo_eval_descriptions(wise_data.parent_sample.df.index)
    red_chi2 = get_red_chi2(wise_data=wise_data)
    info = pd.concat([status, desc, red_chi2], axis=1)

    logger.info("done")
    return info


def make_autopct(values, relative=True):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return f'{pct:.0f}' if relative else f"{val:.0f}"
    return my_autopct


def make_res_plot(
        base_name: str,
        database_name: str,
        wise_data: WISEDataDESYCluster,
        relative: bool = True
):
    logger.info(f"making result plot for {base_name}")
    info = get_res_info(base_name, database_name, wise_data)
    s = list(info.status[~info.status.isna()].unique())
    labels = ["Low $\chi^2$"] + s

    counts = [sum(~info.pass_red_chi2_cut)] + [
        np.sum(info.status[info.pass_red_chi2_cut & info.in_airflares] == si) for si in s]

    fig, ax = plt.subplots()

    ax.pie(
        counts, labels=labels,
        autopct=make_autopct(counts, relative=relative),
        pctdistance=0.8,
        labeldistance=1.08,
        colors=['grey', 'darkgrey', '#762A83', 'lightgrey', '#9970AB', '#C2A5CF'],
        textprops={'fontsize': 15},
        shadow=True,
        radius=2,
        startangle=40,
    )
    fig.tight_layout()

    this_plots_dir = plots_dir("test_data_res", base_name)

    fn = os.path.join(this_plots_dir, f"{base_name}_relative.pdf" if relative else f"{base_name}_total.pdf")
    logger.info(f"saving under {fn}")
    fig.savefig(fn)
    plt.close()
