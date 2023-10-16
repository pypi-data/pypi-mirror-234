"""
This module contains functions to create an ampel config file and to
create a catalogue match config dictionary.

* :func:`create_ampel_config_file` creates an ampel config file in the ``timewise_sup`` data directory.
* :func:`get_catalogue_match_conf` returns a catalogue match config dictionary.
* :func:`get_local_catalogue_match_conf` returns a catalogue match config dictionary for local catalogues.
* :func:`get_filter_config` returns a filter config dictionary that selects data from one of the two WISE bands
    and optionally applies a red chi2 cut.
"""

import os
import logging
import subprocess

from timewise_sup.environment import load_environment


logger = logging.getLogger(__name__)


def ampel_conf_filename():
    tsup_data = load_environment("TIMEWISE_SUP_DATA")
    return os.path.join(tsup_data, "ampel_config.yml")


def create_ampel_config_file():
    """
    Creates an ampel config file in the `timewise_sup` data directory.
    """

    conf_filename = ampel_conf_filename()

    dir = os.path.dirname(conf_filename)
    if not os.path.isdir(dir):
        os.makedirs(dir)

    cmd = ["ampel", "config", "build", "-out", conf_filename]
    logger.debug(f"executing {' '.join(cmd)}")

    with subprocess.Popen(cmd) as p:
        out, err = p.communicate()
        if out is not None:
            logger.info(out.decode())
        if err is not None:
            logger.error(err.decode())

    logger.debug("manually replacing MongoDB port")

    with open(conf_filename, "r") as f:
        content = f.read()
        new_content = content.replace(
            'mongodb://localhost:27017',
            'mongodb://localhost:' + load_environment('TIMEWISE_SUP_MONGODB_PORT')
        )

    with open(conf_filename, "w") as f:
        f.write(new_content)


def get_catalogue_match_conf(match_dist: float) -> dict:
    """
    Returns a catalogue match config dictionary. with the following catalogues:

    - SDSS_spec
    - NEDz
    - NEDz_extcats
    - GLADEv23
    - LSPhotoZZou
    - wiseScosPhotoz
    - twoMPZ
    - TNS
    - milliquas

    :param match_dist: the maximum distance in arcsec for a match
    :type match_dist: float
    :return: a catalogue match config dictionary
    :rtype: dict
    """
    cat_conf = {
        "catalogs": {
            "SDSS_spec": {"use": "extcats", "rs_arcsec": match_dist, "keys_to_append": None},
            "NEDz": {
                "use": "catsHTM",
                "rs_arcsec": match_dist,
                "keys_to_append": ["ObjType", "Velocity", "z"],
            },
            "NEDz_extcats": {
                "use": "extcats",
                "rs_arcsec": match_dist,
                "keys_to_append": ["ObjType", "Velocity", "z"],
            },
            "GLADEv23": {
                "use": "extcats",
                "rs_arcsec": match_dist,
                "keys_to_append": ["z", "dist", "dist_err", "flag1", "flag2", "flag3"],
            },
            "LSPhotoZZou": {
                "use": "extcats",
                "rs_arcsec": match_dist,
                "keys_to_append": [
                    "photoz",
                    "ra",
                    "dec",
                    "e_photoz",
                    "specz",
                    "_6",
                    "logMassBest",
                    "logMassInf",
                    "logMassSup",
                ],
                "pre_filter": None,
                "post_filter": None,
                "all": False,
            },
            "wiseScosPhotoz": {
                "use": "extcats",
                "rs_arcsec": match_dist,
                "keys_to_append": [
                    "zPhoto_Corr",
                    "ra",
                    "dec",
                    "wiseID",
                    "w1mCorr",
                    "w2mCorr",
                ],
                "pre_filter": None,
                "post_filter": None,
            },
            "twoMPZ": {
                "use": "extcats",
                "rs_arcsec": match_dist,
                "keys_to_append": ["zPhoto", "ra", "dec", "zSpec"],
                "pre_filter": None,
                "post_filter": None,
            },
            "TNS": {
                "use": "extcats",
                "rs_arcsec": match_dist,
                "keys_to_append": None,
            },
            "milliquas": {
                "use": "extcats",
                "rs_arcsec": match_dist,
                "keys_to_append": ["broad_type", "name", "redshift", "qso_prob"],
                "pre_filter": None,
                "post_filter": None,
            },
        }
    }
    return cat_conf


def get_local_catalogue_match_conf(match_dist: float) -> dict:
    """
    Returns a catalogue match config dictionary for local catalogues with the following catalogues:

    - fermi4LAC
    - BROS
    - crates
    - CGRaBS
    - ROMA_BZCAT
    - 3HSP

    :param match_dist: the maximum distance in arcsec for a match
    :type match_dist: float
    :return: a catalogue match config dictionary
    :rtype: dict
    """
    cat_local_conf = {
        'catalogs': {
            'fermi4LAC': {
                'use': 'extcats',
                'rs_arcsec': match_dist,
                'keys_to_append': ['Source_Name', 'ra', 'dec'],
                'pre_filter': None,
                'post_filter': None,
                'all': False,
            },
            'BROS': {
                'use': 'extcats',
                'rs_arcsec': match_dist,
                'keys_to_append': ['Source_Name', 'ra', 'dec'],
                'pre_filter': None,
                'post_filter': None,
                'all': False,
            },
            'crates': {
                'use': 'extcats',
                'rs_arcsec': match_dist,
                'keys_to_append': ['Source_Name', 'ra', 'dec'],
                'pre_filter': None,
                'post_filter': None,
                'all': False,
            },
            'CGRaBS': {
                'use': 'extcats',
                'rs_arcsec': match_dist,
                'keys_to_append': ['Source_Name', 'ra', 'dec'],
                'pre_filter': None,
                'post_filter': None,
                'all': False,
            },
            'ROMA_BZCAT': {
                'use': 'extcats',
                'rs_arcsec': match_dist,
                'keys_to_append': ['Source_Name', 'ra', 'dec'],
                'pre_filter': None,
                'post_filter': None,
                'all': False,
            },
            '3HSP': {
                'use': 'extcats',
                'rs_arcsec': match_dist,
                'keys_to_append': ['Source_Name', 'ra', 'dec'],
                'pre_filter': None,
                'post_filter': None,
                'all': False,
            },
        },
        'closest_match': True
    }
    return cat_local_conf


def get_bandpass_filter_component(fid: int) -> dict:
    return {"attribute": "fid", "value": fid, "operator": "=="}


def get_filter_config(logical_connection, red_chi2_threshold: float | None = None):
    """
    Returns a filter config dictionary that selects data from one of the two WISE bands
    and optionally applies a cut on :math:`\chi2_{red} \leq red_chi2_threshold`.

    :param logical_connection: how to connect the two filters
    :type logical_connection: str
    :param red_chi2_threshold: the maximum value of :math:`\chi2_{red}` to be selected
    :type red_chi2_threshold: float
    :return: a filter config dictionary
    :rtype: dict
    """

    if red_chi2_threshold is not None:
        red_chi2_filter = {"attribute": "red_chi2", "value": red_chi2_threshold, "operator": ">"}
        criterias = [[get_bandpass_filter_component(fid), red_chi2_filter] for fid in [1, 2]]

    else:
        # mypy can not handle list comprehensions well
        criterias = [get_bandpass_filter_component(fid) for fid in [1, 2]]  # type: ignore

    filters = [{"criteria": criterias[0], "len": 1, "operator": ">="},
               {"logicalConnection": logical_connection, "criteria": criterias[1], "len": 1, "operator": ">="}]

    filter_config = {"unit": "BasicMultiFilter", "config": {"filters": filters}}
    return filter_config