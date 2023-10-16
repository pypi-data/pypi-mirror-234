"""
Module to interface with the :class:`MongoDB` database.

* :class:`DatabaseConnector`:
    The main class to interface with the database. It is initialized with the :attr:`base_name` and
    :attr:`database_name` and provides methods to get data from the database that was produced by :code:`AMPEL`.
"""

import logging
import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
from pymongo import MongoClient, collection, database
from collections.abc import Sequence
from pydantic import BaseModel
from pathlib import Path

from timewise_sup.environment import load_environment


logger = logging.getLogger(__name__)


jd_offset = -2400000.5


################################################################################
# -----------------------         utilities            ----------------------- #
# --------------------------------  START  ----------------------------------- #
#


Index = Sequence[str | int] | str | int
Status = str | Sequence[str]


def as_list(
        index: Index
) -> list:
    """
    Creates a list from input and transforms np.int64 to int

    :param index: objects to transform to list
    :type index: Index
    :return: the list
    :rtype: list
    """
    indices = list(np.atleast_1d(index))

    for i, ii in enumerate(indices):
        if isinstance(ii, np.int64):
            indices[i] = int(ii)

    return indices


def chunks(
        the_list: Sequence,
        length: int
):
    """
    Yield sequential chunks from l with fixed length

    :param the_list: sequence to be split into chunks
    :type the_list: Sequence
    :param length: length of isngle chunk
    :type length: int
    :return: generator creating the chunks
    :rtype: generator
    """
    number_of_chunks = int(np.ceil(len(the_list) / length))
    logger.debug(f"splitting {len(the_list)} into {number_of_chunks} chunks of length {length}")
    d, r = divmod(len(the_list), number_of_chunks)
    for i in range(number_of_chunks):
        logger.debug(f"chunk {i}")
        si = (d+1)*(i if i < r else r) + d*(0 if i < r else i - r)
        yield the_list[si:si+(d+1 if i < r else d)]


#
# -----------------------         utilities            ----------------------- #
# --------------------------------   END   ----------------------------------- #
################################################################################


################################################################################
# -----------------------      DatabaseConnector       ----------------------- #
# --------------------------------  START  ----------------------------------- #
#


class DatabaseConnector(BaseModel):
    """
    Class to connect to `MongoDB`

    :param base_name: The name given to the :class:`WISEData`
    :type base_name: str
    :param database_name: The name of the database in the :class:`MongoDB`
    :type database_name: str
    :param database: The database object from :class:`pymongo`
    :type database: :class:`pymongo.database.Database`
    :param t2collection: The collection object representing the tier 2 collection as used by :class:`AMPEL`
    :type t2collection: :class:`pymongo.collection.Collection`
    """

    base_name: str
    database_name: str
    database: database.Database
    t2collection: collection.Collection

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        # get the client, database and t2 collections
        client: MongoClient = DatabaseConnector.connect_to_db()
        _database_name = kwargs["database_name"]

        if _database_name not in client.list_database_names():
            logger.warning(f"No database with name {_database_name} registered in client!")

        _database = client[_database_name]
        kwargs["database"] = _database
        kwargs["t2collection"] = _database["t2"]

        super().__init__(**kwargs)

    @property
    def cache_dir(self) -> Path:
        """Directory used to store cache"""
        tsup_data = Path(load_environment("TIMEWISE_SUP_DATA"))
        return tsup_data / self.base_name / self.database_name

    ################################################################################
    # -----------------------  interface with MongoDB      ----------------------- #
    # --------------------------------  START  ----------------------------------- #
    #

    @staticmethod
    def connect_to_db() -> MongoClient:
        """Return the :class:`MongoClient`"""
        mongodb_port = load_environment("TIMEWISE_SUP_MONGODB_PORT")
        logger.debug(f"connecting to MongoDB at {mongodb_port}")
        client: MongoClient = MongoClient(f"mongodb://localhost:{mongodb_port}/")
        logger.debug("connected")
        return client

    def get_dataframe(
            self,
            collection_name: str,
            field_name_lists: list[list[str | int]],
            filter: dict | None = None
    ) -> pd.DataFrame:
        """
        Get fields from a collection in the database and return as :class:`pandas.DataFrame`.

        :param collection_name: Name of the collection
        :type collection_name: str
        :param field_name_lists: The "path" to the value in the collection
        :type field_name_lists: list of lists
        :param filter: filter to apply to the entries
        :type filter: dict
        :return: the selected data
        :rtype: pandas.DataFrame
        """
        logger.info(f"making dataframe from {field_name_lists} of {self.database_name}.{collection_name}")
        col = self.database[collection_name]  # type: collection.Collection
        filter = dict() if filter is None else filter

        res: dict[str, list] = {f"field{i}": list() for i in range(len(field_name_lists))}
        for entry in col.find(filter):
            for i_field_names, field_names in enumerate(field_name_lists):

                # loop through the list of field names / indices to dig down to the value
                val = entry
                for field_name in field_names:
                    if field_name not in val:
                        val = np.nan
                        break
                    val = val[field_name]

                res[f"field{i_field_names}"].append(val)

        return pd.DataFrame.from_dict(res)

    def drop_stocks(self, stocks: Index, tiers: list[int] | None = None):
        """Drop lightcurves and related results from the database"""
        indices = as_list(stocks)
        _tiers = [0, 1, 2] if tiers is None else tiers
        logger.debug(f"dropping {len(indices)} indices of {self.base_name} from {self.database_name} (tiers {_tiers})")

        f = {"stock": {"$in": indices}}

        if 0 in _tiers:
            t0 = self.database["t0"]
            logger.info("dropping datapoints")
            for index in tqdm(indices, desc="dropping datapoints"):
                t0.delete_many({"stock": int(index)})

        if 1 in _tiers:
            t1 = self.database["t1"]
            logger.info("dropping lightcurves")
            t1.delete_many(f)

        if 2 in _tiers:
            logger.info("dropping T2 results")
            self.t2collection.delete_many(f)

    #
    # -----------------------  interface with MongoDB      ----------------------- #
    # --------------------------------   END   ----------------------------------- #
    ################################################################################

    ################################################################################
    # ------------------     get T2DustEchoEval results       -------------------- #
    # --------------------------------  START  ----------------------------------- #
    #

    def get_status(
            self,
            index: Index
    ) -> pd.DataFrame:
        """
        Get the status of objects as determined by the pipline.

        :param index: The index of the objects in the :class:`timewise.ParentSample`
        :type index: Index
        :return: Status of the objects
        :type: pandas.DataFrame
        """
        indices = as_list(index)
        logger.debug(f"getting status for {len(indices)} IDs ({self.base_name} in {self.database_name})")

        columns = {
            "stock": 1,
            "body.status": 1
        }

        i = None
        status = dict()
        for chunked_indices in chunks(indices, int(1e6)):
            dust_echo_filter = {
                "unit": "T2DustEchoEval",
                "code": 0,
                "stock": {"$in": chunked_indices}
            }
            for i, x in enumerate(self.t2collection.find(dust_echo_filter, columns)):
                status[str(x["stock"])] = {"status": x['body'][-1]['status']}

        if len(status) == 0:
            return pd.DataFrame({"status": []})

        return pd.DataFrame.from_dict(status, orient="index")

    def get_unique_statuses(self) -> list:
        """Returns a :class:`list` of all unique statuses"""
        filter = {
            "unit": "T2DustEchoEval",
            "code": 0
        }
        statuses = self.t2collection.distinct("body.status", filter)
        return statuses

    def _calculate_ids(self, status: str) -> list:
        """
        Finds the IDs for a status

        :param status: The status for which the IDs should be calculated for
        :type status: str
        :return: The IDs
        :rtype: list
        """
        logger.debug(f"calculating all IDs for status {status} ({self.base_name} in {self.database_name})")

        filter = {
            "unit": "T2DustEchoEval",
            "body.status": status,
            "code": 0
        }

        columns = {"stock": 1, "body.status": 1}
        stocks = list()
        n_wrong = 0
        for i in tqdm(self.t2collection.find(filter, columns), desc=f"getting IDs for status {status}"):
            stock = i["stock"]
            if i["body"][-1]["status"] != status:
                n_wrong += 1
            else:
                stocks.append(stock)

        stocks = as_list(np.unique(stocks))
        logger.debug(f"found {len(stocks)} stocks, {n_wrong} had matching status from previous run.")
        return stocks

    def get_ids(self, status: Status) -> list:
        """
        Get the IDs for a status. When called for the first time, caches the results to a file
        that will be loaded subsequently.

        :param status: The status
        :type status: Status
        :return: The IDs
        :rtype: list
        """
        logger.debug(f"getting all IDs for status {status} ({self.base_name} in {self.database_name})")

        ids_cache_dir = self.cache_dir / "ids"
        ids_cache_dir.mkdir(parents=True, exist_ok=True)

        stocks = list()

        for istatus in np.unique(status).astype(str):
            fn = ids_cache_dir / f"status{istatus.replace(' ', '_')}.json"

            if not os.path.isfile(fn):
                istocks = self._calculate_ids(istatus)
                logger.debug(f"caching to {fn}")
                with open(fn, "w") as f:
                    json.dump(istocks, f)

            else:
                logger.debug(f"loading cache from {fn}")
                with open(fn, "r") as f:
                    istocks = json.load(f)

                logger.debug(f"got {len(istocks)} ids")

            stocks.extend(istocks)

        return stocks

    def get_excess_mjd(self, index: Index) -> dict:
        """
        Get the excess time for the given index

        :param index: The wanted index
        :type index: Index
        :return: Modified Julian Days of the excess, per filter, start, end and if flare ended
        :rtype: dict
        """
        indices = as_list(index)
        logger.debug(f"getting excess time for {len(indices)} IDs ({self.base_name} in {self.database_name})")

        excess_mjds = dict()

        for chunked_indices in chunks(indices, int(1e6)):
            bayesian_blocks_filter = {
                "unit": "T2BayesianBlocks",
                "stock": {"$in": chunked_indices},
                "code": 0
            }

            for i, x in enumerate(self.t2collection.find(bayesian_blocks_filter)):
                i_excess_mjds = dict()
                for f in ["W1", "W2"]:
                    excess_mags = np.array(x["body"][-1][f"Wise_{f}"]["max_mag_excess_region"])
                    excess_jds = x["body"][-1][f"Wise_{f}"]["jd_excess_regions"]
                    max_excess_mjds = np.array(excess_jds)[np.argmax(excess_mags)] + jd_offset

                    baseline_mjds = np.array(x["body"][-1][f"Wise_{f}"]["jd_baseline_regions"]).flatten() + jd_offset
                    excess_ended = max(baseline_mjds) > max(max_excess_mjds)

                    i_excess_mjds[f"{f}_excess_start_mjd"] = min(max_excess_mjds)
                    i_excess_mjds[f"{f}_excess_end_mjd"] = max(max_excess_mjds)
                    i_excess_mjds[f"{f}_flare_ended"] = excess_ended

                excess_mjds[str(x["stock"])] = i_excess_mjds

        return excess_mjds

    def get_baselines(self, index: Index) -> dict:
        """
        Returns the baseline for the lightcurves.

        :param index: The index of the lightcurves
        :type index: Index
        :returns: The value of the baseline flux and the :math:`1\sigma` uncertainty per filter
        :rtype: dict
        """
        baseline = dict()

        indices = as_list(index)
        logger.debug(f"reading baseline values for {len(indices)} objects")

        for chunked_indices in chunks(indices, int(5e5)):

            dust_echo_filter = {
                "unit": "T2DustEchoEval",
                "stock": {"$in": chunked_indices},
                "code": 0
            }

            for x in self.t2collection.find(
                    dust_echo_filter,
                    {"stock": 1}
            ):
                i_baseline = dict()
                for y in self.t2collection.find(
                        {"unit": "T2BayesianBlocks", "stock": x["stock"], "code": 0},
                        {f"body.Wise_{b}.baseline{s}": 1 for b in ["W1", "W2"] for s in ["", "_sigma"]},
                        limit=1
                ):
                    for b in ["W1", "W2"]:
                        i_baseline[f"{b}_baseline"] = y["body"][-1][f"Wise_{b}"]["baseline"]
                        i_baseline[f"{b}_baseline_sigma"] = y["body"][-1][f"Wise_{b}"]["baseline_sigma"]

                baseline[str(x["stock"])] = i_baseline

        return baseline

    def _calculate_t2_dust_echo_eval_descriptions(self, index: Index) -> pd.DataFrame:
        """
        Get the description for the lightcurves

        :param index: The index of the lightcurves
        :type index: Index
        :return: Description per lightcurves, separated by ", "
        :rtype: dict
        """
        indices = as_list(index)
        logger.debug(f"getting description for {len(indices)} objects of {self.base_name} in {self.database_name}")

        values = dict()

        for chunked_indices in chunks(indices, int(5e5)):
            filter = {
                "code": 0,
                "unit": "T2DustEchoEval",
                "stock": {"$in": chunked_indices}
            }

            for lc in self.t2collection.find(filter):
                value = dict()

                try:
                    value[f"description"] = ", ".join(lc["body"][-1]["description"])
                except KeyError as e:
                    raise KeyError(f"{lc}: {e}")

                values[str(lc["stock"])] = value

        logger.debug(f"returning {len(values)} results")

        return pd.DataFrame.from_dict(values, orient="index")

    def get_t2_dust_echo_eval_descriptions(self, indices: Index) -> pd.DataFrame:
        """
        Get the description of the lightcurves. Caches result to file when first called.

        :param indices: The index of the lightcurves
        :type indices: Index
        :return: Description per lightcurves, separated by ", "
        :rtype: dict
        """
        fn = self.cache_dir / "T2DustEchoEvalDescriptions.csv"
        fn.parents[0].mkdir(parents=True, exist_ok=True)

        if not os.path.isfile(fn):
            logger.debug(f"no file {fn}")
            desc = self._calculate_t2_dust_echo_eval_descriptions(indices)
            logger.debug(f"saving to {fn}")
            desc.to_csv(fn)

        else:
            logger.debug(f"loading {fn}")
            desc = pd.read_csv(fn, index_col=0)

        indices_series = pd.Series(indices)
        indices_present = indices_series.astype(str).isin(desc.index.astype(str))
        if np.any(~indices_present):
            logger.debug(f"{np.sum(~indices_present)} indices not found. calculating")
            desc_suplement = self._calculate_t2_dust_echo_eval_descriptions(indices_series[~indices_present])
            desc = pd.concat([desc, desc_suplement])
            logger.debug(f"saving {len(desc)} descriptions to {fn}")
            desc.to_csv(fn)

        return desc.loc[indices_series.astype(type(desc.index[0]))]

    def get_agn_variability_stocks(self) -> list:
        logger.debug("getting AGN stock IDs based on variability")

        filter = {
            '$and': [
                {"code": 0},
                {"unit": "T2DustEchoEval"},
                # {"body": {"$elemMatch": {"description": "Excess region exists"}}},
                {"body.description": {"$elemMatch": {"$ne": "Baseline only"}}},
                {"body.description": {"$elemMatch": {"$ne": "Stage transition"}}},
                {"body.status": {"$ne": "1"}}
                ]
        }

        cols = {"stock": 1}

        stocks = list()
        for lc in self.t2collection.find(filter, cols):
            stocks.append(lc["stock"])

        logger.debug(f"returning {len(stocks)} stock IDs")
        return stocks

    def get_t2_dust_echo_eval_values(self, index: Index, value: str) -> pd.DataFrame:
        """
        Get a value per filter and lightcurve as produced by the :class:`AMPEL` :class:`T2DustEchoEval`

        :param index: The index of the lightcurves
        :type index: Index
        :param value: The key of the value
        :type value: str
        :return: The value per lightcurves and filter
        :rtype: pandas.DataFrame
        """

        indices = as_list(index)
        logger.debug(f"getting {value} for {len(indices)} objects of {self.base_name} in {self.database_name}")

        filter = {
            "unit": "T2DustEchoEval",
            "stock": {"$in": as_list(index)},
            "code": 0
        }

        n = self.t2collection.count_documents(filter)
        logger.debug(f"found {n} documents")

        values = dict()

        for lc in self.t2collection.find(filter):
            ivalue = dict()

            for i, b in enumerate(["W1", "W2"]):
                try:
                    ivalue[f"{value}_{b}"] = lc["body"][-1]["values"][value][i]
                except KeyError as e:
                    raise KeyError(f"{lc}: {e}")
                except IndexError as e:
                    raise IndexError(f"{lc}: {e}")

            values[str(lc["stock"])] = ivalue

        logger.debug(f"returning {len(values)} results")

        return pd.DataFrame.from_dict(values, orient="index")

    def get_peak_time_jd(self, index: Index) -> pd.DataFrame:
        """Get the peak time in Julian Days"""
        return self.get_t2_dust_echo_eval_values(index, "max_mag_jd")

    def get_excess_start_jd(self, index: Index) -> pd.DataFrame:
        """Get the start of the excess in Julian Days"""
        return self.get_t2_dust_echo_eval_values(index, "excess_jd")

    def get_dust_echo_strength(self, index: Index) -> pd.DataFrame:
        """Get the strength of the dust echo"""
        return self.get_t2_dust_echo_eval_values(index, "strength_sjoert")

    def get_fade_time(self, index: Index) -> pd.DataFrame:
        """Get the fade time"""
        return self.get_t2_dust_echo_eval_values(index, "e_fade")

    def get_rise_time(self, index: Index) -> pd.DataFrame:
        """Get the rise time"""
        return self.get_t2_dust_echo_eval_values(index, "e_rise")

    #
    # ------------------     get T2DustEchoEval results       -------------------- #
    # --------------------------------   END   ----------------------------------- #
    ################################################################################

    ############################################################################################
    # -------------     get T2CatalogMatch and T2DigestRedshifts results       --------------- #
    # -------------------------------------  START  ------------------------------------------ #
    #

    def get_catalog_matches(self, index: Index) -> dict:
        """
        Get the matches as determined by the :class:`AMPEL` :class:`T2CatalogMatch`

        :param index: Index of the Lightcurves
        :type index: Index
        :return: All matches in the catalogues
        :rtype: dict
        """
        logger.debug(f"getting catalog match info for {self. base_name} in {self.database_name}")
        indices = as_list(index)
        logger.debug(f"getting catalog match info for {len(indices)} objects")

        matches = dict()

        for chunked_indices in chunks(indices, 1000000):

            filter = {
                "code": 0,
                "stock": {"$in": chunked_indices},
                "unit": "T2CatalogMatch"
            }

            for i in self.t2collection.find(filter):
                matches[i["stock"]] = i["body"][-1]

        return matches

    def get_redshift(self, index: Index) -> pd.DataFrame:
        """
        Get the redshifts as determined by the :class:`AMPEL` :class:`T2DigestRedshifts`

        :param index: Index of the lightcurves
        :type index: Index
        :return: The redshift, distance to the match and the uncertainty associated to the redshift measurement method
        :rtype: pandas.DataFrame
        """
        filter = {
            "unit": "T2DigestRedshifts",
            "stock": {"$in": as_list(index)},
            "body.ampel_z": {"$exists": True}
        }

        n = self.t2collection.count_documents(filter)
        logger.debug(f"found {n} documents")

        redshift = dict()

        for lc in self.t2collection.find(filter):
            try:
                d = {k: lc["body"][-1][k]
                     for k in ["ampel_z", "ampel_dist", "group_z_precision"]}
                redshift[str(lc["stock"])] = d
            except KeyError as e:
                raise KeyError(f"{lc}: {e}")

        logger.debug(f"returning {len(redshift)} results")

        return pd.DataFrame.from_dict(redshift, orient="index")

    #
    # -------------     get T2CatalgueMatch and T2DigestRedshifts results       --------------- #
    # --------------------------------------   END   ------------------------------------------ #
    #############################################################################################

#
# -----------------------      DatabaseConnector       ----------------------- #
# --------------------------------   END   ----------------------------------- #
################################################################################
