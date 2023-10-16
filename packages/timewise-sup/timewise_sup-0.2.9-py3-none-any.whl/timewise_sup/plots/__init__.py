import os.path
import argparse
import logging
import json

from timewise_sup.environment import load_environment


tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
logger = logging.getLogger(__name__)


bandcolors = {
    "W1": "purple",
    "W2": "plum",
    "ZTF_g": "forestgreen",
    "ZTF_r": "crimson",
    "ZTF_i": "khaki"
}


status_linestyle = {
    "1": "-",
    "2": "--",
    "2_maybe_interesting": ":",
    "3": "-.",
    "4": "-.",
    "No_further_investigation": "-.",
}


types_colors = {
    "agn": "mediumpurple",
    "tde": "darkviolet",
    "failed": "tomato",
    "sn_other": "darkturquoise",
    "snia": "deepskyblue",
    "star": "beige",
    "unclass": "lightgrey"
}


type_labels = {
    "agn": "AGN",
    "tde": "TDE",
    "sn_other": "SN ($\\ne$ Ia)",
    "snia": "SN Ia",
    "failed": "failed fit",
    "star": "Star",
    "unclass": "unclassified"
}


def plots_dir(module: str, base_name: str) -> str:
    d = os.path.join(tsup_data_dir, "plots", module, base_name)
    if not os.path.isdir(d):
        os.makedirs(d)
    return d
