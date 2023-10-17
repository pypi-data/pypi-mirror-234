"""
Implements the creation of :class:`AMPEL` job files

* :class:`ampel_job_file_filename()`: centralised function to get job file filenames
* :class:`keys_in_list()`: utility function to check of any key in a list is in a list of lists
* :class:`make_ampel_job_file()`: Creates the actual job file
"""

import json
import logging
import os.path
import yaml
import copy
from timewise.wise_data_base import WISEDataBase

from timewise_sup.environment import load_environment
from timewise_sup.plots import plots_dir as get_plots_dir
from timewise_sup.ampel_conf import (
    create_ampel_config_file,
    ampel_conf_filename,
    get_catalogue_match_conf,
    get_local_catalogue_match_conf,
    get_filter_config
)


logger = logging.getLogger(__name__)


def ampel_job_file_filename(
        base_name,
        chunk,
        t2units,
        precut_filter,
):
    """Get the filename for a job file with the given arguments. See :class:`make_ampel_job_file()` for arguments."""
    units_str = "run"
    if keys_in_list(["bayesian", "dust"], t2units):
        units_str += "_bayeblocks"
    if keys_in_list(["redshift", "catalogue"], t2units):
        units_str += "_xmatch"
    if keys_in_list(["local_catalogue"], t2units):
        units_str += "_localxmatch"
    if keys_in_list(["redshift"], t2units):
        units_str += "_zdigest"

    tsup_data = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(
        tsup_data,
        base_name,
        "ampel_job_files",
        f"{chunk}__{units_str}__filter{precut_filter}.yml"
    )
    return fn


def keys_in_list(keys, arr):
    """Checks if any of the keys is in any of the lists"""
    return any([any([k in element for element in arr]) for k in keys])


def make_ampel_job_file(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        chunk: int | None,
        t2units: list[str],
        precut_filter: bool | None,
        load_from_bigdata_dir: bool = True,
        service: str = "tap",
        concurrent: bool = False,
        split_units: bool = False
):
    """
    Creates the :class:`AMPEL` job file running the specified units.

    :param base_name: base name of the analysis
    :type base_name: str
    :param database_name: Name of the database in the MongoDB
    :type database_name: str
    :param wise_data: The wise data to be analysed
    :type wise_data: timewise.wise_data_base.WISEDataBase
    :param chunk: The chunk of the wise data
    :type chunk: int
    :param t2units:
        The :class:`AMPEL` tier 2 units to run
        (see the `Ampel-hu-astro repo <https://github.com/AmpelAstro/Ampel-HU-astro>`_).

        * :code:`"bayesian"`, :code:`"dust"`:
            Runs :class:`T2BayesianBlocks` to find excess regions and :class:`T2DustEchoEval` to characterise the result.
        * :code:`"catalogue"`: :class:`T2CatalogMatch`
        * :code:`"redshift"`: :class:`T2CatalogMatch` and :class:`T2DigestRedshifts`
        * :code:`"catalogue_local"`: :class:`T2CatalogMatchLocal`

    :type t2units: list[str]
    :param load_from_bigdata_dir: If :code:`True` loads from the wise data's big data directory
    :type load_from_bigdata_dir: bool
    :param service: The :class:`timewise` service used to download the data, either :code:`"tap"` or :class:`"gator"`
    :type service: str
    :param precut_filter: Run :class:`T2DustEchoEval` only for lightcurves with
        significant variation compared to the median :math:`\chi^2/\mathrm{ndoF} > 1`
    :type precut_filter: bool
    :param concurrent: Optimised set-up for running :class:`AMPEL` concurrently
    :type concurrent: bool
    :param split_units: Split units in different tasks
    :type split_units: bool
    :return: Filename of the job file
    :rtype: str
    """
    logger.info(f"making ampel job file for chunk {chunk} of {base_name}")

    # create ampel config file
    AMPEL_CONF = ampel_conf_filename()
    if not os.path.isfile(AMPEL_CONF):
        create_ampel_config_file()

    # ------------------- assemble configurations for T2 units ------------------- #
    # --------------------------------  START  ----------------------------------- #
    #

    # T2CatalogueMatch
    match_dist = 5.
    t2_catalogue_match_config = get_catalogue_match_conf(match_dist)

    # T2LocalCatalogueMatch
    t2_local_cataklogue_match_config = get_local_catalogue_match_conf(match_dist)

    # T2DigestRedshifts
    t2_digest_redshifts_config = {
        "max_redshift_category": 7,
        "t2_dependency": [
            {"unit": "T2CatalogMatch", "config": t2_catalogue_match_config, "link_override": {"filter": "PPSFilter"}}
        ]
    }

    # T2BayesianBlocks
    plots_dir = get_plots_dir("ampel_plots", base_name=base_name)
    bayesian_blocks_db_format = {
        "channel": "wise",
        "BayePlots": False,
        "BayePlotsDir": os.path.join(plots_dir, "T2BayesianBlocks"),
        "DustEchoDir": os.path.join(plots_dir, "T2DustEchoEval")
    }
    t2_bayesian_blocks_config = {
        "debug": logger.getEffectiveLevel() <= logging.DEBUG,
        "debug_dir": bayesian_blocks_db_format["BayePlotsDir"],
        "rej_sigma": 5,
        "plot": bayesian_blocks_db_format["BayePlots"],
        "data_type": "wise",
        "filters": ["Wise_W1", "Wise_W2"],
        "flux": True,
        "Npoints": True,
        "plot_props": {
            "file_name": {"format_str": "%s_%s.svg", "arg_keys": ["stock", "band"]},
            "title": {"format_str": "%s", "arg_keys": ["stock"]},
            "width": 18,
            "height": 23,
            "fig_include_title": False,
            "disk_save": bayesian_blocks_db_format["BayePlotsDir"],
        },
    }

    # T2DustEchoEval
    t2_dust_echo_eval_config = {
        "flux": True,
        "filters": ["Wise_W1", "Wise_W2"],
        "directory": bayesian_blocks_db_format["DustEchoDir"],
        "t2_dependency": [
            {
                "unit": "T2BayesianBlocks",
                "config": t2_bayesian_blocks_config,
            },
        ],
    }

    #
    # ------------------- assemble configurations for T2 units ------------------- #
    # --------------------------------   END   ----------------------------------- #

    # --------------------- assemble directives for T2 units --------------------- #
    # --------------------------------  START  ----------------------------------- #

    # find units to use
    units = [e.lower() for e in t2units]
    directives = list()
    unit_ids = list()
    channels = list()

    # ------- bayesian blocks ------- #

    # check if any of the units specify the T2BayesianBlocks + T2DustEchoEval configuration
    if keys_in_list(["bayesian", "dust"], units):
        filter_config = get_filter_config(logical_connection="AND", red_chi2_threshold=1 if precut_filter else None)
        t2_bayesian_blocks_directives = {
            "channel": bayesian_blocks_db_format["channel"],
            "filter": filter_config,
            "ingest": {
                "mux": {
                    "unit": "ZiMongoMuxer",
                    'config': {"db_complete": False},
                    "combine": [{
                        "unit": "ZiT1Combiner",
                        "state_t2": [
                            {"unit": "T2BayesianBlocks", "config": t2_bayesian_blocks_config},
                            {"unit": "T2DustEchoEval", "config": t2_dust_echo_eval_config}
                        ]
                    }],
                }
            }
        }

        directives.append(t2_bayesian_blocks_directives)
        channels.append(bayesian_blocks_db_format["channel"])
        unit_ids.extend(["T2BayesianBlocks", "T2DustEchoEval"])

    # ------- Catalogue match and Redshift digest  ------- #

    if keys_in_list(["redshift", "catalogue", "catalogue_local"], units):
        catalogue_redshift_channel = "redshift_catalog_match"
        channels.append(catalogue_redshift_channel)

        if keys_in_list(["redshift"], units):
            combine = [{
                "unit": "ZiT1Combiner",
                "state_t2": [{'unit': 'T2DigestRedshifts', 'config': t2_digest_redshifts_config}]
            }]
        else:
            combine = list()

        point_t2: list[dict | list[dict]] = [{
            "unit": "T2CatalogMatch",
            "config": t2_catalogue_match_config,
            "ingest": {"filter": "PPSFilter", "sort": "jd", "select": "first"},
        }]

        if keys_in_list(["local"], units):
            point_t2.append([{"unit": "T2CatalogMatchLocal", "config": t2_local_cataklogue_match_config}])

        t2_catalogue_match_directives = {
            "channel": catalogue_redshift_channel,
            "filter": get_filter_config(logical_connection="OR"),
            "ingest": {
                "mux": {
                    "unit": "ZiMongoMuxer",
                    "config": {"db_complete": False},
                    "combine": combine,
                    "insert": {"point_t2": point_t2}
                }
            }
        }

        directives.append(t2_catalogue_match_directives)

        # check which exact units to run

        if keys_in_list(["redshift", "catalogue"], units):
            unit_ids.append("T2CatalogMatch")

        if keys_in_list(["catalogue_local"], units):
            unit_ids.append("T2LocalCatalogMatch")

        if keys_in_list(["redshift"], units):
            unit_ids.append("T2DigestRedshifts")

    logger.debug(f"unit ids: {unit_ids}")

    #
    # --------------------- assemble directives for T2 units --------------------- #
    # --------------------------------   END   ----------------------------------- #

    # --------------------------- make AMPEL job file ---------------------------- #
    # --------------------------------  START  ----------------------------------- #
    #

    if load_from_bigdata_dir:
        alert_archive = wise_data._data_product_filename(service=service, chunk_number=chunk, use_bigdata_dir=True)
    else:
        alert_archive = wise_data._data_product_filename(service=service, chunk_number=chunk)

    channel_info = [{
        "name": c,
        "version": 0,
        "access": ["ZTF_PUB"],
        "policy": []
    } for c in channels]

    ampel_job_dictionary = {
        "name": 'timewise_sup',
        "mongo":
            {
                "prefix": database_name,
                "reset": False,
            },
        "channel": channel_info,
        "task": [
            {
                "title": 't0',
                "unit": "AlertConsumer",
                "multiplier": 1,
                "config": {
                    "log_profile": "prod",
                    "compiler_opts": "ZiCompilerOptions",
                    "shaper": "ZiDataPointShaper",
                    "supplier": {
                        "unit": "NeoWisePhotometryAlertSupplier",
                        "config": {
                            "dpid": "hash",
                            "loader": {
                                "unit": "WiseFileAlertLoader",
                                "config": {
                                    "file": alert_archive,
                                }
                            }
                        }
                    },
                    "directives": directives,
                    "iter_max": 1000000
                }
            }
        ]
    }

    t2_task_template = {
        'title': "t2",
        'unit': 'T2Worker',
        'multiplier': 1,
        'config': {
            "log_profile": "default",
        }
    }

    if concurrent:
        t2_task_template["config"] = {
            "doc_limit": 1000000,
            "pre_check": False,
            "run_dependent_t2s": False,
            "wait_for_durable_write": False,
            "updates_buffer_size": 500,
            "garbage_collect": False,
            "max_try": 10,
            "log_profile": "prod",
            "code_match": [-1, -6, -2000, -2001, -2004, -2006, -2008],
            "pending_codes": [-2001, -2006, -2004, -2008, -5, -1, -2000, -7],
        }

    if split_units:
        for unit_id in unit_ids:
            task = copy.deepcopy(dict(t2_task_template))  # type: dict
            task["config"]["unit_ids"] = [unit_id]
            logger.debug(f"adding task {json.dumps(task, indent=4)}")
            ampel_job_dictionary["task"].append(task)  # type: ignore

    else:
        logger.debug(f"adding task {json.dumps(t2_task_template, indent=4)}")
        ampel_job_dictionary["task"].append(t2_task_template)  # type: ignore

    filename = ampel_job_file_filename(
        base_name=base_name,
        chunk=chunk,
        t2units=t2units,
        precut_filter=precut_filter
    )

    logger.info(f"writing ampel job file to {filename}")
    d = os.path.dirname(filename)
    if not os.path.isdir(d):
        os.makedirs(d)
    with open(filename, "w") as f:
        yaml.dump(ampel_job_dictionary, f)

    return filename

    #
    # --------------------------- make AMPEL job file ---------------------------- #
    # --------------------------------   END   ----------------------------------- #
