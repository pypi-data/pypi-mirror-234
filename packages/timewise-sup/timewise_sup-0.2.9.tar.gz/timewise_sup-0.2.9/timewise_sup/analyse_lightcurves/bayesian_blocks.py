"""
This module implements a function that creates an :class:`AMPEL` job file and runs it

* :class:`bayesian_blocks()`: Creates and runs an :class:`AMPEL` job file
"""

import logging
import subprocess
from timewise.wise_data_base import WISEDataBase

from timewise_sup.ampel_conf import ampel_conf_filename
from timewise_sup.analyse_lightcurves.create_job_file_yaml import make_ampel_job_file

logger = logging.getLogger("timewise_sup.analyze_lightcurves.bayesian_blocks")


def bayesian_blocks(
    base_name: str,
    database_name: str,
    wise_data: WISEDataBase,
    chunk: int | None,
    t2units: list[str],
    load_from_bigdata_dir: bool = True,
    service: str = "tap",
    precut_filter: bool | None = False,
):
    """
    1. Uses :class:`make_ampel_job_file() to create an :class:`AMPEL` job file.
    2. Assumes that :class:`create_ampel_job_file()` has been run.
    3. Executes :code:`ampel job -config <config_file> -schema <job_file>`

    See :class:`timewise_sup.analyse_lightcurves.create_job_file_yaml.make_ampel_job_file()` for arguments.
    """

    fn = make_ampel_job_file(
        base_name=base_name,
        wise_data=wise_data,
        database_name=database_name,
        chunk=chunk,
        t2units=t2units,
        precut_filter=precut_filter,
        concurrent=False,
        split_units=False,
        load_from_bigdata_dir=load_from_bigdata_dir,
        service=service
    )

    logger.info("running ampel")
    with subprocess.Popen(["ampel", "job", "-config", ampel_conf_filename(), "-schema", fn]) as p:
        out, err = p.communicate()
        if out is not None:
            logger.info(out.decode())
        if err is not None:
            logger.error(err.decode())
