"""
This module contains functions for calculating diagnostics for the meta-analysis. The diagnostics are saved to files
in the ``timewise_sup_data`` directory. The diagnostics are:

* ``statuses_per_chunk.json``: the status of the objects in each chunk
* ``catalog_matches_per_chunk.json``: the number of catalog matches in each chunk
* ``positional_outlier_mjds``: the MJDs of the positional outliers in each chunk

The functions are:

* :func:`calculate_positional_outlier_times` calculates the MJDs of the positional outliers in a given chunk
* :func:`get_statuses_per_chunk` gets the statuses of the objects in each chunk
* :func:`get_catalog_matches_per_chunk` gets the number of catalog matches in each chunk
* :func:`get_positional_outliers_times` gets the MJDs of the positional outliers in each chunk

"""

import logging
import os
import json
import tqdm
from timewise.wise_data_base import WISEDataBase

from timewise_sup.environment import load_environment
from timewise_sup.mongo import DatabaseConnector
from timewise_sup.meta_analysis.catalog_match import get_catalog_match_mask


logger = logging.getLogger(__name__)


def get_statuses_per_chunk(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase
) -> dict:
    """
    Get the statuses of the objects in each chunk. The statuses are saved to a file in the ``timewise_sup_data``
    directory. If the file already exists, it is loaded from there. Otherwise, it is calculated and saved.

    :param base_name: base name of the WISE data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :return: the statuses of the objects in each chunk
    :rtype: dict
    """
    logger.info(f"getting statuses per chunk for {base_name}")
    tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(tsup_data_dir, base_name, "statuses_per_chunk.json")

    if not os.path.isfile(fn):
        logger.debug(f"No file {fn}. Calculating")
        chunks = list(range(wise_data.n_chunks))

        logger.info("getting statusees")
        statusees = dict()
        for c in chunks:
            m = wise_data.chunk_map == c
            ids = wise_data.parent_sample.df.index[m]
            status = DatabaseConnector(base_name=base_name, database_name=database_name).get_status(ids)
            statusees[c] = list(status.status)

        logger.debug(f"saving under {fn}")
        with open(fn, "w") as f:
            json.dump(statusees, f)

    else:
        logger.debug(f"loading {fn}")
        with open(fn, "r") as f:
            statusees = json.load(f)

    return statusees


def get_catalog_matches_per_chunk(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase
) -> dict:
    """
    Get the number of catalog matches in each chunk. The number of catalog matches are saved to a file in the
    ``timewise_sup_data`` directory. If the file already exists, it is loaded from there. Otherwise, it is calculated
    and saved.

    :param base_name: base name of the WISE data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :return: the number of catalog matches in each chunk
    :rtype: dict
    """
    logger.info("getting catalog matches per chunk")

    tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(tsup_data_dir, base_name, "catalog_matches_per_chunk.json")

    if not os.path.isfile(fn):
        logger.debug(f"No file {fn}. Calculating")

        chunks = list(range(wise_data.n_chunks))

        matches_per_chunk = dict()
        for c in chunks:
            m = wise_data.chunk_map == c
            ids = wise_data.parent_sample.df.index[m]
            chunk_match_mask = get_catalog_match_mask(base_name, database_name, ids)

            chunk_matches = dict()
            for catalogue_name in chunk_match_mask.columns:
                chunk_matches[catalogue_name] = int(chunk_match_mask[catalogue_name].sum())

            matches_per_chunk[c] = chunk_matches

        logger.debug(f"saving to {fn}")
        with open(fn, "w") as f:
            json.dump(matches_per_chunk, f)

    else:
        logger.debug(f"loading {fn}")
        with open(fn, "r") as f:
            matches_per_chunk = json.load(f)

    return matches_per_chunk


def calculate_positional_outlier_times(
        wise_data: WISEDataBase,
        chunk_number: int
) -> list:
    """
    Use :class:`timewise` to calculate the MJDs of the positional outliers in a given chunk.
    See the `documentation
    <https://timewise.readthedocs.io/en/latest/api.html#timewise.wise_data_base.WISEDataBase.get_position_mask>`_
    for more information.

    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :param chunk_number: the chunk number
    :type chunk_number: int
    :return: the MJDs of the positional outliers in the chunk
    :rtype: list
    """
    logging.getLogger("timewise").setLevel(logging.getLogger("timewise_sup").getEffectiveLevel())
    unbinned_lcs = wise_data.get_unbinned_lightcurves(chunk_number=chunk_number)
    position_masks = wise_data.get_position_mask(service="tap", chunk_number=chunk_number)

    mjds = list()

    for ind, position_mask in tqdm.tqdm(position_masks.items(), desc="going through lightcurves"):
        lc = unbinned_lcs[unbinned_lcs[wise_data._tap_orig_id_key] == int(ind)]
        mjds.extend(list(lc.loc[position_mask].mjd.values))

    return mjds


def get_positional_outliers_times(
        base_name,
        wise_data: WISEDataBase
) -> dict:
    """
    Get the MJDs of the positional outliers in each chunk. The MJDs are saved to files in the ``timewise_sup_data``
    directory. If the files already exist, they are loaded from there. Otherwise, they are calculated and saved.

    :param base_name: base name of the WISE data
    :type base_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :return: the MJDs of the positional outliers in each chunk
    :rtype: dict
    """
    logger.info(f"getting positional outlier times")

    tsup_data = load_environment("TIMEWISE_SUP_DATA")
    cache_dir = os.path.join(tsup_data, base_name, "positional_outlier_mjds")
    os.makedirs(cache_dir, exist_ok=True)

    mjds_per_chunk = dict()

    for c in tqdm.tqdm(range(wise_data.n_chunks), desc="going through chunks"):
        fn = os.path.join(cache_dir, f"{c}.json")

        if not os.path.isfile(fn):
            logger.debug(f"file {fn} not found. Calculating")
            mjds = calculate_positional_outlier_times(wise_data, c)
            logger.debug(f"saving to {fn}")

            with open(fn, "w") as f:
                json.dump(mjds, f)

        else:
            logger.debug(f"loading {fn}")
            with open(fn, "r") as f:
                mjds = json.load(f)

        mjds_per_chunk[c] = mjds

    return mjds_per_chunk
