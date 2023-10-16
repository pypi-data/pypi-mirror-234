"""
Functions for getting catalog match masks.

* :func:`get_catalog_match_mask` gets a mask for the catalog matches of a given base name.
"""

import logging
import pandas as pd

from timewise_sup.mongo import DatabaseConnector, Index


logger = logging.getLogger(__name__)


def get_catalog_match_mask(
        base_name: str,
        database_name: str,
        index: Index
) -> pd.DataFrame:
    """
    Get the catalog match mask for a given base name. True means that the object has a match in any of the catalogs.

    :param base_name: base name of the WISE data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param index: the index of the objects to get the catalog match mask for
    :type index: Index
    :return: the catalog match mask
    :rtype: pd.DataFrame
    """
    logger.info("getting catalog match mask")
    matches = DatabaseConnector(base_name=base_name, database_name=database_name).get_catalog_matches(index)
    has_match_dict = {i: {c: match is not None for c, match in imatches.items()} for i, imatches in matches.items()}
    has_match_masks = pd.DataFrame.from_dict(has_match_dict, orient="index").fillna(False)
    return has_match_masks
