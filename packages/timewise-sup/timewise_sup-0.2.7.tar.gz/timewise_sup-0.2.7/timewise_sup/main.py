import logging
import json
from argparse import ArgumentParser

from timewise_sup.config_loader import TimewiseSUPConfigLoader


logger = logging.getLogger(__name__)


def main():
    parser = ArgumentParser()
    parser.add_argument("config", type=str, help="Path to timewise_sup config file")
    parser.add_argument("-l", "--logging-level", default="INFO", type=str)
    cfg = vars(parser.parse_args())

    logging_level = cfg.pop("logging_level")
    logging.getLogger("timewise_sup").setLevel(logging_level)
    logging.getLogger("timewise").setLevel(logging_level)
    logger.debug(f"Running timewise_sup with args {json.dumps(cfg, indent=4)}")
    TimewiseSUPConfigLoader.run_yaml(cfg["config"])
