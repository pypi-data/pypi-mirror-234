from pathlib import Path
from threading import Lock

import pandas as pd

from preprocessing.facilities.network import preprocess as preprocess_network

ACQUIRE_DICT_LOCK = Lock()
LOCK_DICT = {}


def preprocess(output_source, bsw, bfpd, network, subsurface_mapping, trust_existing=False, **_):
    """
    Validates bsw and bfpd files comming from a pre-processing
    """
    bfpd_file_name = Path(output_source.uri) / bsw
    bsw_file_name = Path(output_source.uri) / bfpd
    network_file_name = Path(output_source.uri) / network

    if not bfpd_file_name.exists() or not bsw_file_name.exists() or not network_file_name.exists():
        return

    with ACQUIRE_DICT_LOCK:
        output_file_lock_bfpd = LOCK_DICT.get(bfpd_file_name)
        if output_file_lock_bfpd is None:
            output_file_lock_bfpd = Lock()
            LOCK_DICT[bfpd_file_name] = output_file_lock_bfpd

    with output_file_lock_bfpd:
        networks = preprocess_network(
            output_source, network, subsurface_mapping, trust_existing=True, include_topology=False
        )

        bfpd = pd.read_csv(bfpd_file_name)
        bsw = pd.read_csv(bsw_file_name)

        network_clusters = set(networks["subsurface_mapping"].keys())
        bfpd_clusters = set(bfpd.columns)
        bsw_clusters = set(bsw.columns)

        clusters_not_present_in_all_files = (
            network_clusters.symmetric_difference(bfpd_clusters)
            .union(network_clusters.symmetric_difference(bsw_clusters))
            .union(bfpd_clusters.symmetric_difference(bsw_clusters))
        )

        if clusters_not_present_in_all_files:
            raise ValueError(
                "The following clusters are not present in all sampling files: "
                + ",".join(sorted(clusters_not_present_in_all_files))
            )

    return {"bfpd": bfpd, "bsw": bsw}
