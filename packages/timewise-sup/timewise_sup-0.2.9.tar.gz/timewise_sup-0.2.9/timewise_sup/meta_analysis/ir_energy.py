"""
Calculate the IR energy of the flares. This is done by integrating the luminosity over the duration of the flare.

The IR energy is calculated and stored in a json file. The file is named
ir_eng_status{status}.json, where status is the status of the flare. The file is stored in the directory
`timewise_sup_data/{base_name}`. If the file already exists, it is loaded from there. If it does not exist, it is
calculated and stored there.

* :func:`ir_energy_integral` calculates the IR energy for a given light curve
* :func:`calculate_ir_energy` calculates the IR energy for a given status
* :func:`get_ir_energy_status` calculates the IR energy for a given status
* :func:`get_ir_energy_index` calculates the IR energy for a given index

"""

import logging
import os
import json
from collections.abc import Mapping
import numpy as np
import pandas as pd
from scipy import integrate
from timewise.wise_data_base import WISEDataBase

from timewise_sup.environment import load_environment
from timewise_sup.mongo import DatabaseConnector, Index, Status
from timewise_sup.meta_analysis.luminosity import get_ir_luminosities


logger = logging.getLogger(__name__)


def ir_energy_integral(
        lc: pd.DataFrame,
        t0: Mapping[str, float],
        t1: Mapping[str, float],

) -> float:
    """
    Calculate the IR energy of a flare by integrating the luminosity over the duration of the flare.

    :param lc:
    :type lc: pd.DataFrame
    :param t0:
    :param t1:
    :return:
    """

    mjd = lc["mean_mjd"]
    bol_eng = 0

    for b in ["W1", "W2"]:
        mask = (mjd >= t0[b]) & (mjd <= t1[b])
        fit_lum = lc[f"{b}_ir_luminosity_erg_per_s"][mask]
        fit_mjd = mjd[mask]

        # integrate using trapezoidal rule
        integral = integrate.trapezoid(fit_lum, fit_mjd * 24 * 3600)
        bol_eng += integral

    return bol_eng


def calculate_ir_energy(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        status: Status,
) -> dict:
    """
    Calculate the IR energy of the flares. This is done by integrating the luminosity over the duration of the flare.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param status: status of the flare
    :type status: Status
    :return: dictionary with the index as key and the IR energy as value
    :rtype: dict
    """
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    ids = database_connector.get_ids(status)
    indices = np.atleast_1d(ids)
    logger.info(f"calculating luminosities for {len(indices)} objects")
    lcs = get_ir_luminosities(base_name, database_name, wise_data, status)
    excess_mjd = database_connector.get_excess_mjd(indices)

    engs = dict()

    for k, lc in lcs.items():
        ieng = dict()
        ieng["ir_energy_erg"] = ir_energy_integral(pd.DataFrame.from_dict(lc, orient="columns"),
                                                      {b: excess_mjd[k][f"{b}_excess_start_mjd"] for b in ["W1", "W2"]},
                                                      {b: excess_mjd[k][f"{b}_excess_end_mjd"] for b in ["W1", "W2"]})
        ieng["ir_energy_is_lower_limit"] = bool(np.any([excess_mjd[k][f"{b}_flare_ended"] for b in ["W1", "W2"]]))
        engs[k] = ieng

    return engs


def get_ir_energy_status(
        base_name: str,
        database_name: str,
        status: Status,
        wise_data: WISEDataBase | None = None,
        force_new: bool = False,
) -> dict:
    """
    Get the IR energy of the flares per status. If the cache file `ir_eng_status{status}.json` exists, it is loaded from there.
    If it does not exist, it is calculated by :func:`calculate_ir_energy` and stored there.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param status: status for which the IR energy should be calculated
    :type status: Status
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param force_new: if True, the IR energy is calculated and stored in the cache file, even if it already exists
    :type force_new: bool
    :return: dictionary with the index as key and the IR energy as value
    :rtype: dict
    """
    logger.info(f"getting bolometric luminosities for status {status}")
    tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(tsup_data_dir, base_name, f"ir_eng_status{status}.json")

    if (not os.path.isfile(fn)) or force_new:

        if wise_data is None:
            raise ValueError("wise_data must be given when calculating IR energies!")
        else:
            logger.debug(f"No file {fn}.")
            logger.info("Making bolometric luminosities")
            engs = calculate_ir_energy(
                base_name=base_name,
                database_name=database_name,
                wise_data=wise_data,
                status=status
            )

        with open(fn, "w") as f:
            json.dump(engs, f)

    else:
        logger.debug(f"loading {fn}")
        with open(fn, "r") as f:
            engs = json.load(f)

    return engs


def get_ir_energy_index(
        base_name: str,
        database_name: str,
        index: Index,
        wise_data: WISEDataBase,
        forcenew: bool = False,
) -> dict:
    """
    Get the IR energy of the flares per index by getting the status and calling :func:`get_ir_energy_status`
    for each status.

    :param base_name:
    :type base_name: str
    :param database_name:
    :type database_name: str
    :param index: index of the lightcurve
    :type index: Index
    :param forcenew: if True, the IR energy is calculated and stored in the cache file, even if it already exists
    :type forcenew: bool
    :return: dictionary with the index as key and the IR energy as value
    :rtype: dict
    """

    statuses = DatabaseConnector(base_name=base_name, database_name=database_name).get_status(index)

    engs_all = dict()

    for status in statuses.status.unique():
        eng = get_ir_energy_status(base_name, database_name, status, wise_data, forcenew)
        selected_lums = {k: v for k, v in eng.items() if k in statuses.index[statuses.status == status]}
        engs_all.update(selected_lums)

    return engs_all
