import os
import logging
from pathlib import Path

from timewise.general import data_dir


logger = logging.getLogger(__name__)

environment_variable_defaults = {
    "TIMEWISE_SUP_DATA": str(Path(data_dir) / "subtraction_pipeline"),
    "TIMEWISE_SUP_MONGODB_PORT": "27017",
    "ZTF_FPH": None,
    "ZTF_NUCLEAR_SAMPLE_DB_PATH": None
}


def load_environment(key):
    try:
        return os.environ[key]
    except KeyError:
        default_val = environment_variable_defaults[key]
        logger.debug(f"environment variable {key} not specified. Using default {default_val}")
        return default_val
