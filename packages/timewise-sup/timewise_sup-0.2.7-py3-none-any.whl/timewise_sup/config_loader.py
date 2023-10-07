"""
This module contains the :class:`TimewiseSUPConfig` and :class:`TimewiseSUPConfigLoader` classes which are used to
load the configuration for ``timewise-sup``.

* :class:`TimewiseSUPConfig` is a subclass of :class:`timewise.config_loader.TimewiseConfig` used to run the config
* :class:`TimewiseSUPConfigLoader` is a subclass of :class:`timewise.config_loader.TimewiseConfigLoader` used to load the config from a YAML file
"""

import logging
import inspect
from pydantic import validator
from timewise.config_loader import TimewiseConfig, TimewiseConfigLoader

from timewise_sup.ampel_conf import create_ampel_config_file
from timewise_sup.analyse_lightcurves.bayesian_blocks import bayesian_blocks
from timewise_sup.meta_analysis.baseline_subtraction import get_baseline_subtracted_lightcurves
from timewise_sup.plots.plot_lightcurves import plot_sample_lightcurves
from timewise_sup.meta_analysis.ztf import download_ztffp_per_status
from timewise_sup.analyse_lightcurves.cluster import run_bayesian_blocks_on_cluster
from timewise_sup.plots.diagnostic_plots import chunk_distribution_plots, positional_outliers


logger = logging.getLogger(__name__)


functions = {
    "create_ampel_config_file": create_ampel_config_file,
    "bayesian_blocks": bayesian_blocks,
    "baseline_subtraction": get_baseline_subtracted_lightcurves,
    "plot": plot_sample_lightcurves,
    "download_ztffp_per_status": download_ztffp_per_status,
    "run_cluster": run_bayesian_blocks_on_cluster,
    "plot_distributions_among_chunks": chunk_distribution_plots,
    "plot_positional_outliers": positional_outliers
}

_functions_str = "\n".join(
    [f"\n\t* ``{fct_name}``: :func:`{fct.__module__}.{fct.__name__}` " for fct_name, fct in functions.items()]
)


class TimewiseSUPConfigLoader(TimewiseConfigLoader):
    __doc__ = f"""
    Loads the config for ``timewise-sup`` from a YAML file.
    The config is validated and parsed into a :class:`TimewiseSUPConfig` object.
    In addition to the parameters of :class:`timewise.config_loader.TimewiseConfigLoader`, the following parameters
    are available:
    
    :param timewise_sup_instructions: a list of dictionaries containing the instructions for ``timewise-sup``.
        Each dictionary must contain a single key-value pair, where the key is the name of the function to be called
        and the value is a dictionary of arguments for the function. The arguments must be valid for the function.
        The functions are called in the order they appear in the list. The possible functions are:
        {_functions_str}
    :type timewise_sup_instructions: list
    :param database_name: the name of the database in the ``MongoDB`` to be used for the analysis
    :type database_name: str
    """

    timewise_sup_instructions: list[dict] = list()
    database_name: str

    def parse_config(self):
        timewise_config = super().parse_config()
        return TimewiseSUPConfig(
            database_name=self.database_name,
            timewise_sup_instructions=self.timewise_sup_instructions,
            **timewise_config.dict()
        )


class TimewiseSUPConfig(TimewiseConfig):
    """
    Config for ``timewise-sup``.
    In addition to running the ``timewise`` config, it runs the functions specified in
    :attr:`timewise_sup_instructions` in the order they appear in the list.
    """

    timewise_sup_instructions: list[dict] = list()
    database_name: str

    @validator("timewise_sup_instructions")
    def validate_timewise_sup_instructions(cls, v: list[dict]):
        for instructions in v:
            for fct_name, arguments in instructions.items():

                if fct_name not in functions:
                    available = ", ".join(list(functions.keys()))
                    raise ValueError(f"timewise-sup has no function {fct_name}! Must be either of {available}")

                fct = functions[fct_name]
                # this is a mypy bug: https://github.com/python/mypy/issues/10740

                signature = inspect.signature(fct)  # type: ignore
                param_list = list(signature.parameters)
                # check if the function needs default arguments
                _arguments = arguments or dict()  # supply empty dict if arguments is None
                for k in ["base_name", "database_name", "wise_data"]:
                    if k in param_list:
                        # enter dummy string in arguments
                        _arguments[k] = ""
                # check validity of arguments
                try:
                    signature.bind(**_arguments)
                except TypeError as e:
                    raise ValueError(f"{fct_name}: {e}!")

        return v

    def run_config(self):
        logger.info("running config")
        super().run_config()

        for instructions in self.timewise_sup_instructions:
            for fct_name, arguments in instructions.items():
                _arguments = arguments or dict()  # supply empty dict if arguments is None
                fct = functions[fct_name]
                params = list(inspect.signature(fct).parameters)

                if "base_name" in params:
                    _arguments["base_name"] = self.wise_data.base_name
                if "database_name" in params:
                    _arguments["database_name"] = self.database_name
                if "wise_data" in params:
                    _arguments["wise_data"] = self.wise_data

                logger.info(f"running {fct_name} with arguments {_arguments}")
                fct(**_arguments)

        logger.info("successfully ran config")
