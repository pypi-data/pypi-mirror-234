"""
This module contains the function to get the number of objects per rejection reason. The rejection reason is given in
the description of the ``AMPEL`` ``T2DustEchoEval`` unit output.

* :func:`get_rejection_reason` gets the number of objects per rejection reason for the whole sample
* :func:`calculate_rejection_reasons` calculates the rejection reasons for the given index
* :func:`get_individual_rejection_reasons` gets the individual rejection reasons for the given index and caches to disk
"""

import logging
import json
import numpy as np
import pandas as pd

from timewise_sup.mongo import DatabaseConnector, Index


logger = logging.getLogger(__name__)


def get_rejected_ids(
        base_name: str,
        database_name: str,
):
    """
    Get the ids of the rejected objects. The rejection reason is given in the description of the
    ``AMPEL`` ``T2DustEchoEval`` unit output.

    :param base_name: base name of the wise data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :return: ids of the rejected objects
    :rtype: list
    """
    logger.info(f"getting rejected ids for {base_name}")
    rejected = (
        "No further investigation",
        "1_maybe_interesting",
        "2_maybe_interesting",
        "3", "3_maybe_interesting",
        "4", "4_maybe_interesting"
    )
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    ids = database_connector.get_ids(rejected)
    return ids


def get_rejection_reason(
        base_name: str,
        database_name: str
) -> dict:
    """
    Get the number of objects per rejection reason. The rejection reason is given in the description of the
    ``AMPEL`` ``T2DustEchoEval`` unit output.

    :param base_name: base name of the wise data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :return: dictionary with the rejection reason as key and the number of objects as value
    :rtype: dict
    """
    logger.info(f"getting rejection reason for {base_name}")
    ids = get_rejected_ids(base_name, database_name)
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    desc = database_connector.get_t2_dust_echo_eval_descriptions(ids)
    desc_counts = desc.description.value_counts()  # type: pd.Series

    # when there is a gap in the lightcurve before a potential excess, the status will be "_maybe_interesting"
    # but can have the accepted description. We can replace it with the more meaningful "gap"
    ac_str = 'Baseline before excess region, Excess region exists, Baseline before excess region, Excess region exists'
    desc_counts.rename(index={ac_str: "gap"}, inplace=True)

    individual_reasons = dict()
    for ir, n in desc_counts.items():
        # descriptions are given per band
        # here we make sure to only count them once
        already_counted = []
        for irsi in ir.split(", "):
            if irsi in already_counted:
                continue
            if irsi not in individual_reasons:
                individual_reasons[irsi] = n
            else:
                individual_reasons[irsi] += n
            already_counted.append(irsi)

    # sort by number
    individual_reasons_df = pd.DataFrame.from_dict(individual_reasons, orient="index").sort_values(0, ascending=False)

    # find individual reasons in descriptions
    accept = ['Baseline before excess region', 'Excess region exists']
    masks: dict[str, bool] = {
        rt: desc_counts.index.str.contains(rt)
        for rt in individual_reasons_df.index if rt not in accept
    }

    # find individual reasons that exclude the object with descending order of appearance
    masks_exclusive = {rt: im & ~np.logical_or.reduce(list(masks.values())[:i])
                       for i, (rt, im) in enumerate(masks.items())}

    # find the corresponding numbers of objects
    numbers_exclusive = {rt: int(desc_counts[m].sum()) for rt, m in masks_exclusive.items()}
    logger.debug(json.dumps(numbers_exclusive, indent=4))

    return numbers_exclusive


def calculate_rejection_reasons(
        base_name: str,
        database_name: str,
        index: Index
) -> pd.DataFrame:
    """
    Calculate the rejection reasons for the given index.

    :param base_name: base name of the wise data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param index: index of the objects
    :type index: Index
    :return: dataframe with the rejection reasons
    :rtype: pd.DataFrame
    """
    connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    _index = pd.Index(index)
    info = pd.DataFrame(index=_index, columns=["rejection_reason"], dtype=str)

    # find rejected ids
    rejected_ids = get_rejected_ids(base_name, database_name)

    # find indices that have not been run, probably because of chi2 cut
    accepted_index = pd.Index(connector.get_ids(("1", "2")))
    info.loc[_index[_index.isin(index)], "rejection_reason"] = "accepted"

    # find indices that have not been run, probably because of chi2 cut
    not_run_index = _index[~_index.isin(accepted_index) & ~_index.isin(rejected_ids)]
    info.loc[not_run_index, "rejection_reason"] = "not run"

    # get the descriptions for the rejected indices
    desc = connector.get_t2_dust_echo_eval_descriptions(_index[_index.isin(rejected_ids)])

    # where the description suggests acception but the objects was rejected, we have a gap in the lightcurve
    ac_str = 'Baseline before excess region, Excess region exists, Baseline before excess region, Excess region exists'
    gap_mask = desc.description.str.contains(ac_str) & desc.index.isin(rejected_ids)
    desc.loc[gap_mask, "description"] = "gap"

    # set the rejection reason for the rejected indices
    global_reasons_dict = get_rejection_reason(base_name, database_name)
    global_reasons = pd.DataFrame.from_dict(global_reasons_dict, orient="index").sort_values(0, ascending=True)
    for r in global_reasons.index:
        i = desc.index[desc.description.str.contains(r)]
        info.loc[_index.astype(str).isin(i.astype(str)), "rejection_reason"] = r

    return info


def get_individual_rejection_reasons(
        base_name: str,
        database_name: str,
        index: Index
) -> pd.DataFrame:
    """
    Get the individual rejection reasons for the given index. If the individual rejection reasons are not yet
    calculated, they will be calculated and saved.

    :param base_name: base name of the wise data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param index: index of the objects
    :type index: Index
    :return: dataframe with the individual rejection reasons
    :rtype: pd.DataFrame
    """

    connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    filename = connector.cache_dir / f"individual_rejection_reasons.csv"

    if filename.is_file():
        logger.debug(f"loading individual rejection reasons from {filename}")
        individual_reasons = pd.read_csv(filename, index_col=0)
    else:
        individual_reasons = pd.DataFrame()

    _index = pd.Index(index)
    is_calculated_mask = _index.isin(individual_reasons.index)

    if any(~is_calculated_mask):
        logger.debug(f"calculating individual rejection reasons for {sum(~is_calculated_mask)} objects of {base_name} "
                     f"in {database_name}")
        new_reasons = calculate_rejection_reasons(base_name, database_name, _index[~is_calculated_mask])
        individual_reasons = pd.concat([individual_reasons, new_reasons], axis=0)
        logger.debug(f"saving individual rejection reasons to {filename}")
        individual_reasons.to_csv(filename)

    return individual_reasons.loc[_index]

