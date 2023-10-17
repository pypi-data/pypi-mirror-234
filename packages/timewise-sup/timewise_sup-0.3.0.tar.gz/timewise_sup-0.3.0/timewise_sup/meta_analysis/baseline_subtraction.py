"""
Module to subtract the baseline from the lightcurves.

The baseline is determined by the T2BayesianBlocks algorithm and stored in the database. This module reads the
baseline values and subtracts them from the lightcurves. The resulting lightcurves are stored in a json file.

* :func:`apply_baseline_subtraction` reads the baseline values from the database and subtracts them from the lightcurves.
* :func:`get_baseline_subtracted_lightcurves` reads the lightcurves from the json file by status or creates it.
* :func:`get_lightcurves` reads the lightcurves from the json file by indices.
* :func:`get_single_lightcurve` reads the lightcurves from the json file by index.
"""

import json
import os.path
from functools import cache
import numpy as np
import logging
import tqdm

import pandas as pd

from timewise_sup.mongo import DatabaseConnector, Index, Status
from timewise_sup.environment import load_environment
from timewise import WiseDataByVisit, WISEDataDESYCluster


logger = logging.getLogger(__name__)


def apply_baseline_subtraction(
        wise_data: WiseDataByVisit,
        database_name: str,
        service: str = "tap",
        load_from_bigdata_dir: bool = True,
        status: Status | None = None,
        index: Index | None = None
) -> dict:
    """
    Apply baseline subtraction to the lightcurves. The baseline values are read from the database and subtracted from
    the lightcurves. The resulting lightcurves are returned as a dictionary. The dictionary keys are the IDs of the
    lightcurves. The values are the lightcurves themselves.

    :param wise_data: WISEDataByVisit object
    :type wise_data: WiseDataByVisit
    :param database_name: name of the database
    :type database_name: str
    :param service: :class:`timewise` service that was used to download the data, defaults to "tap"
    :type service: str, optional
    :param load_from_bigdata_dir: whether to load the data from the bigdata directory, defaults to True
    :type load_from_bigdata_dir: bool, optional
    :param status: status of the lightcurves to be processed, defaults to None
    :type status: Status, optional
    :param index: IDs of the lightcurves to be processed, defaults to None
    :type index: Index, optional
    :return: dictionary containing the baseline subtracted lightcurves
    :rtype: dict
    """

    logger.debug(f"status {status}")
    logger.debug(f"index {index}")

    database_connector = DatabaseConnector(base_name=wise_data.base_name, database_name=database_name)

    if status is not None:
        logger.debug(f"getting indices from status {status}, ignoring passed value {index}!")
        index = database_connector.get_ids(status=status)
    else:
        if index is None:
            raise ValueError("You must specify either of 'index' or 'status'!")

    logger.info("getting baseline values")

    # keys are stock IDs, values are baseline values
    baselines = database_connector.get_baselines(index=index)
    ids = np.array(list(baselines.keys()))
    logger.debug(f"got baselines for {len(ids)} objects")

    # find the chunk that holds the respective IDs
    chunk_numbers = np.array([wise_data._get_chunk_number(parent_sample_index=s) for s in ids])

    # set up empty directory for baseline corrected lightcurves
    diff_lcs = dict()

    # load the chunks one after the other
    logger.info(f"calculating difference flux for {len(ids)} objects in {len(np.unique(chunk_numbers))} chunks")
    for c in np.unique(chunk_numbers):
        logger.debug(f"chunk {c}")

        if load_from_bigdata_dir or isinstance(wise_data, WISEDataDESYCluster):
            timewise_data_product = wise_data.load_data_product(
                service=service,
                chunk_number=c,
                use_bigdata_dir=load_from_bigdata_dir
            )
        else:
            timewise_data_product = wise_data.load_data_product(
                service=service,
                chunk_number=c
            )

            # loop through IDs in this chunk
        for s in tqdm.tqdm(ids[chunk_numbers == c], desc=f"apply baseline subtraction to chunk {c}"):
            lc_in = pd.DataFrame.from_dict(timewise_data_product[str(s)]["timewise_lightcurve"])
            lc_out = lc_in[["mean_mjd"]].copy()

            for b in ["W1", "W2"]:

                # loop over flux and flux errors
                f_key = WiseDataByVisit.mean_key + WiseDataByVisit.flux_density_key_ext
                ferr_key = WiseDataByVisit.flux_density_key_ext + WiseDataByVisit.rms_key

                try:
                    # f is a dict with keys: index and values: flux_densities
                    f = lc_in[b + f_key]
                    baseline = baselines[s][f"{b}_baseline"]
                    baseline_err = baselines[s][f"{b}_baseline_sigma"]

                    if baseline is None:
                        logger.warning(f"baseline for {s} {b} is None, skipping!")
                        continue

                    f_diff = {k: v - baseline for k, v in f.items()}
                    f_diff_key = "_diff" + f_key
                    lc_out.loc[list(f_diff.keys()), b + f_diff_key] = list(f_diff.values())

                    ferr_diff_key = "_diff" + ferr_key
                    lc_out[b + ferr_diff_key] = np.sqrt(lc_in[b + ferr_key].copy() ** 2 + baseline_err ** 2)

                except KeyError as e:
                    logger.error(
                        f"parent sample index {s}: {e}. "
                        f"LC is \n{json.dumps(lc_out, indent=4)}"
                    )
                    raise KeyError

            # save lightcurve containing baseline corrected flux
            diff_lcs[str(s)] = lc_out.to_dict()

    logger.info("done")

    return diff_lcs


def get_baseline_subtracted_lightcurves(
        base_name: str,
        database_name: str,
        wise_data: WiseDataByVisit,
        status: Status,
        force_new: bool = False,
        service: str = "tap",
        load_from_bigdata_dir: bool = True,
) -> dict:
    """
    Get the baseline subtracted lightcurves from the json file buy status. If the file does not exist, call the function
    :func:`apply_baseline_subtraction` to create it. The resulting lightcurves are returned as a dictionary. The
    dictionary keys are the IDs of the lightcurves. The values are the lightcurves themselves.

    :param base_name: name of the base directory
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: WISEDataByVisit object
    :type wise_data: WiseDataByVisit
    :param status: status of the lightcurves to be processed
    :type status: Status
    :param force_new: whether to force the creation of a new file, defaults to False
    :type force_new: bool, optional
    :param service: :class:`timewise` service that was used to download the data, defaults to "tap"
    :type service: str, optional
    :param load_from_bigdata_dir: whether to load the data from the bigdata directory, defaults to True
    :type load_from_bigdata_dir: bool, optional
    :return: dictionary containing the baseline subtracted lightcurves
    :rtype: dict
    """
    logger.info(f"getting baseline subtracted lightcurves for status {status}")
    tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(tsup_data_dir, base_name, f"diff_lcs_status{status}.json")

    if (not os.path.isfile(fn)) or force_new:
        logger.info(f"No file {fn}.")
        logger.info("Making baseline subtracted lightcurves")
        diff_lcs = apply_baseline_subtraction(
            wise_data=wise_data,
            database_name=database_name,
            service=service,
            load_from_bigdata_dir=load_from_bigdata_dir,
            status=status
        )

        d = os.path.dirname(fn)
        if not os.path.isdir(d):
            os.makedirs(d)

        logger.debug(f"saving under {fn}")
        with open(fn, "w") as f:
            json.dump(diff_lcs, f)

    else:
        logger.debug(f"loading {fn}")
        with open(fn, "r") as f:
            diff_lcs = json.load(f)

    return diff_lcs


def get_lightcurves(
        base_name: str,
        database_name: str,
        wise_data: WiseDataByVisit,
        index: Index,
        service: str = "tap",
        load_from_bigdata_dir: bool = True,
) -> dict:
    """
    Get the baseline subtracted lightcurves from the json file by index. If the file does not exist, call the function
    :func:`get_baseline_subtracted_lightcurves` to create it. The resulting lightcurves are returned as a dictionary.
    The dictionary keys are the IDs of the lightcurves. The values are the lightcurves themselves.

    :param base_name: name of the base directory
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: WISEDataByVisit object
    :type wise_data: WiseDataByVisit
    :param index: IDs of the lightcurves to be processed
    :type index: Index
    :param service: :class:`timewise` service that was used to download the data, defaults to "tap"
    :type service: str, optional
    :param load_from_bigdata_dir: whether to load the data from the bigdata directory, defaults to True
    :type load_from_bigdata_dir: bool, optional
    :return: dictionary containing the baseline subtracted lightcurves
    :rtype: dict
    """
    indices = list(np.atleast_1d(index))
    logger.info(f"getting lightcurves {len(indices)} objects")
    status = DatabaseConnector(base_name=base_name, database_name=database_name).get_status(index=tuple(indices))
    logger.debug(f"found {len(status['status'].unique())} statuses")
    lcs = dict()
    for s in status["status"].unique():
        iids = status.index[status["status"] == s]
        slcs = get_baseline_subtracted_lightcurves(
            base_name=base_name,
            database_name=database_name,
            wise_data=wise_data,
            status=s,
            service=service,
            load_from_bigdata_dir=load_from_bigdata_dir
        )

        for i in iids:
            lcs[str(i)] = slcs[i]

    logger.debug(f"returning {len(lcs)} lightcurves")
    return lcs


@cache
def get_single_lightcurve(
        base_name: str,
        database_name: str,
        wise_data: WiseDataByVisit,
        index: str,
        service: str = "tap",
        load_from_bigdata_dir: bool = True,
) -> pd.DataFrame:
    """
    Get the baseline subtracted lightcurves from the json file by index. If the file does not exist, call the function
    :func:`get_lightcurves` to create it.

    :param base_name: name of the base directory
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: WISEDataByVisit object
    :type wise_data: WiseDataByVisit
    :param index: ID of the lightcurve to be processed
    :type index: str
    :param service: :class:`timewise` service that was used to download the data, defaults to "tap"
    :type service: str, optional
    :param load_from_bigdata_dir: whether to load the data from the bigdata directory, defaults to True
    :type load_from_bigdata_dir: bool, optional
    :return: baseline subtracted lightcurve
    :rtype: pandas.DataFrame
    """
    lcs = get_lightcurves(
        base_name=base_name,
        database_name=database_name,
        wise_data=wise_data,
        index=index,
        service=service,
        load_from_bigdata_dir=load_from_bigdata_dir
    )
    return pd.DataFrame.from_dict(lcs[str(index)])
