"""
Make histograms of the chi2 values for each chunk using the ``WISEDataDESYCluster.make_chi2_plot()`` method.

* :func:`make_timewise_chi2_histograms` makes histograms of the chi2 values for each chunk using the
``WISEDataDESYCluster.make_chi2_plot()`` method.
"""

import logging
import numpy as np
from timewise import WISEDataDESYCluster

from timewise_sup.meta_analysis.agn import get_agn_mask_from_color


logger = logging.getLogger(__name__)


def make_timewise_chi2_histograms(
        base_name: str,
        wise_data: WISEDataDESYCluster,
        chunks: list | None = None,
        plot_options: dict | None = None
):
    """
    Make histograms of the chi2 values for each chunk using the ``WISEDataDESYCluster.make_chi2_plot()`` method.
    See the ``timewise`` `documentation <https://timewise.readthedocs.io/en/latest/api.html#timewise.wise_bigdata_desy_cluster.WISEDataDESYCluster.make_chi2_plot>`_
    for more information.

    :param base_name: base name for storage directories
    :type base_name: str
    :param wise_data: instance of WISEDataDESYCluster
    :type wise_data: WISEDataDESYCluster
    :param chunks: list of chunks to use
    :type chunks: list
    :param plot_options: options for the plot, see ``WISEDataDESYCluster.make_chi2_plot()``
    :type plot_options: dict
    """

    logger.info("making timewise chi2 histograms")

    if chunks is None:
        chunks = list(range(wise_data.n_chunks))

    logger.debug(f"using chunks {chunks}")

    wise_mag_keys = ["W1_mag", "W2_mag", "W3_mag"]
    if np.any([k not in wise_data.parent_sample.default_keymap for k in wise_mag_keys]):
        logger.warning(f"One of {','.join(wise_mag_keys)} not in ParentSample's default keymap: \n"
                       f"{wise_data.parent_sample.default_keymap}.\n"
                       f"Not making separate histograms for AGNs.")
        index_mask = {}

    else:
        agn_mask, w1w2, w2w3 = get_agn_mask_from_color(base_name, wise_data)
        agn_indices = agn_mask.index[agn_mask].astype(str)
        non_agn_indices = agn_mask.index[~agn_mask].astype(str)
        index_mask = {
            "AGNs": agn_indices,
            "non-AGNs": non_agn_indices,
        }

    if plot_options is None:
        plot_options = {}

    wise_data.make_chi2_plot(
        chunks=chunks,
        load_from_bigdata_dir=True,
        lum_key="_flux_density",
        index_mask=index_mask,
        save=True,
        **plot_options
    )
