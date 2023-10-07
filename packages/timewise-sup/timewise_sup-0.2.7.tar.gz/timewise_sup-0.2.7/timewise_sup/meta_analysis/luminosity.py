"""
Calculates the IR luminosities of the lightcurves in the database.

* :func:`get_band_nu` returns the frequency of a given band
* :func:`nuFnu` calculates the flux density value of a given spectral flux density
* :func:`calculate_ir_luminosities` calculates the IR luminosities for a given index
* :func:`get_ir_luminosities` calculates the IR luminosities for a given status
"""

import logging
import os
import json

import astropy.units
import numpy as np
from numpy import typing as npt
import pandas as pd
from astropy import units as u
from astropy.cosmology import Planck18
from astropy import constants
from timewise.wise_data_base import WISEDataBase

from timewise_sup.environment import load_environment
from timewise_sup.mongo import DatabaseConnector, Index, Status
from timewise_sup.meta_analysis.baseline_subtraction import get_lightcurves


logger = logging.getLogger(__name__)


band_wavelengths = {
    # from Wright et al. (2010) ( 10.1088/0004-6256/140/6/1868 )
    "W1": 3.4 * 1e-6 * u.m,
    "W2": 4.6 * 1e-6 * u.m,
    # from http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php?id=Palomar/ZTF.g&&mode=browse&gname=Palomar&gname2=ZTF
    "ZTF_g": 4804.79 * u.AA,
    "ZTF_r": 6436.92 * u.AA,
    "ZTF_i": 7968.22 * u.AA
}


def get_band_nu(band: str) -> astropy.units.Quantity:
    """Returns the frequency of a given band"""
    wl = band_wavelengths[band]
    return constants.c / wl


def nuFnu(
        spectral_flux_density: list[float],
        spectral_flux_density_unit: str,
        band: str,
        out_unit: str = "erg s-1 cm-2"
) -> npt.NDArray:
    """
    Calculates the flux density value of a given spectral flux density. The flux density is calculated by multiplying
    the spectral flux density with the frequency of the given band.

    :param spectral_flux_density:
    :type spectral_flux_density: list[float]
    :param spectral_flux_density_unit:
    :type spectral_flux_density_unit: str
    :param band:
    :type band: str
    :param out_unit:
    :type out_unit: str
    :return:
    """
    _flux = np.array(spectral_flux_density) * u.Unit(spectral_flux_density_unit)
    nu = get_band_nu(band)
    return np.array(u.Quantity(_flux * nu).to(out_unit).value)


def calculate_ir_luminosities(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        redshift: dict[str, float] | pd.Series,
        redshift_err: dict[str, float] | pd.Series,
) -> dict:
    """
    Calculates the IR luminosities for a given index. The IR luminosity is calculated by multiplying the flux density
    with the area of the sphere with the radius of the luminosity distance. The luminosity distance is calculated
    using the Planck18 cosmology. The area is calculated using the formula for the surface area of a sphere.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param index: index of the object
    :type index: Index
    :param redshift: redshift of the object
    :type redshift: dict[str, float] | pd.Series
    :param redshift_err: redshift error of the object
    :type redshift_err: dict[str, float] | pd.Series
    :return: dictionary with the index as key and the IR luminosities as value
    :rtype: dict
    """
    indices = tuple(np.atleast_1d(index).astype(int))
    logger.info(f"calculating luminosities for {len(indices)} objects")

    if len(indices) != len(redshift):
        raise ValueError("redshift and index must have the same length!")

    lcs = get_lightcurves(base_name, database_name, wise_data, indices)
    logger.debug(f"got {len(lcs)} lightcurves")
    lcs_with_luminosities = dict()
    for i, lc_dict in lcs.items():
        lc = pd.DataFrame.from_dict(lc_dict, orient="columns")
        iredshift = redshift[i]
        iredshift_err = redshift_err[i]

        lum_dist = Planck18.luminosity_distance(iredshift)
        area = 4 * np.pi * lum_dist ** 2

        lum_dist_ic = Planck18.luminosity_distance(iredshift + iredshift_err * np.array([-1, 1]))
        area_ic = 4 * np.pi * lum_dist_ic ** 2

        for b in ["W1", "W2"]:
            lc[f"{b}_nuFnu_erg_per_s_per_sqcm"] = nuFnu(lc[f"{b}_diff_mean_flux_density"],
                                                        spectral_flux_density_unit="mJy", band=b,
                                                        out_unit="erg s-1 cm-2")

            lc[f"{b}_nuFnu_err_erg_per_s_per_sqcm"] = nuFnu(lc[f"{b}_diff_flux_density_rms"],
                                                            spectral_flux_density_unit="mJy", band=b,
                                                            out_unit="erg s-1 cm-2")

            nuFnu_val = u.Quantity(lc[f"{b}_nuFnu_erg_per_s_per_sqcm"] * u.Unit("erg s-1 cm-2"))
            nuFnu_valerr = u.Quantity(lc[f"{b}_nuFnu_err_erg_per_s_per_sqcm"] * u.Unit("erg s-1 cm-2"))

            lum = u.Quantity(nuFnu_val * area).to("erg s-1").value
            lum_err = u.Quantity(
                np.sqrt(
                    (nuFnu_valerr * area) ** 2 + (nuFnu_val * max(abs(area-area_ic))) ** 2
                )
            ).to("erg s-1").value

            lc[f"{b}_ir_luminosity_erg_per_s"] = lum
            lc[f"{b}_ir_luminosity_err_erg_per_s"] = lum_err

        lcs_with_luminosities[i] = lc.to_dict()

    return lcs_with_luminosities


def get_ir_luminosities(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        status: Status,
        force_new: bool = False
) -> dict:
    """
    Calculates the IR luminosities of the lightcurves in the database for a given status. If the cache file
    `lum_ir_lcs_status{status}.json` exists, it is loaded from there. If it does not exist, it is calculated by
    :func:`calculate_ir_luminosities` and stored there.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param status: status for which the IR luminosities should be calculated
    :type status: Status
    :param force_new: if True, the luminosities are calculated even if the cache file exists
    :type force_new: bool
    :return: dictionary with the index as key and the IR luminosities as value
    :rtype: dict
    """

    logger.info(f"getting luminosities for status {status}")
    tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(tsup_data_dir, base_name, f"lum_ir_lcs_status{status}.json")

    if (not os.path.isfile(fn)) or force_new:
        logger.debug(f"No file {fn}")
        logger.info("calculating luminosities")

        database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
        indices = database_connector.get_ids(status)
        redshifts = database_connector.get_redshift(indices)
        lcs = calculate_ir_luminosities(
            base_name,
            database_name,
            wise_data,
            redshifts.index,
            redshifts.ampel_z,
            redshifts.group_z_precision
        )

        logger.debug(f"writing to {fn}")
        with open(fn, "w") as f:
            json.dump(lcs, f)

    else:
        logger.debug(f"reading from {fn}")
        with open(fn, "r") as f:
            lcs = json.load(f)

    return lcs


def get_ir_luminosities_index(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        force_new: bool = False
) -> dict:
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    statuses = database_connector.get_status(index)

    lums_all = dict()

    for status in statuses.status.unique():
        lums = get_ir_luminosities(base_name, database_name, wise_data, status, force_new)
        selected_lums = {k: v for k, v in lums.items() if k in statuses.index[statuses.status == status]}
        lums_all.update(selected_lums)

    return lums_all


# def get_peak_ir_luminosity_index(
#         base_name: str,
#         database_name: str,
#         index: Index,
# ) -> dict:
#     logger.info(f"getting peak IR luminosities for index {ind} ({base_name})")
#     lcs = get_ir_luminosities(base_name, database_name, status)
#     logger.debug(f"got {len(lcs)} lightcurves")
#
#     peak_lum = dict()
#     for i, lc_dict in lcs.items():
#         lc = pd.DataFrame.from_dict(lc_dict, orient="columns")
#         peak_lum[i] = dict()
#         for b in ["W1", "W2"]:
#             arg = np.argmax(lc[f"{b}_luminosity_erg_per_s"])
#             peak_lum[i][f"{b}_peak_luminosity_erg_per_s"] = lc[f"{b}_luminosity_erg_per_s"][arg]
#             peak_lum[i][f"{b}_peak_luminosity_err_erg_per_s"] = lc[f"{b}_luminosity_err_erg_per_s"][arg]
#             peak_lum[i][f"{b}_peak_luminosity_mjd"] = lc["mean_mjd"][arg]

