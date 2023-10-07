import json
import os.path
import re
from collections import OrderedDict
from itertools import chain
from pathlib import Path
from threading import Lock

import numpy as np
import pandas as pd
from scipy import sparse
from sknetwork.data import Bunch
from sknetwork.topology import get_core_decomposition
from sknetwork.visualization import svg_graph

ACQUIRE_DICT_LOCK = Lock()
LOCK_DICT = {}


def preprocess(output_source, network, subsurface_mapping=None, trust_existing=False, include_topology=True, **_):
    output_file_name = Path(output_source.uri) / "network.json"
    output_file_image_name = Path(output_source.uri) / "network.svg"

    with ACQUIRE_DICT_LOCK:
        output_file_lock = LOCK_DICT.get(output_file_name)
        if output_file_lock is None:
            output_file_lock = Lock()
            LOCK_DICT[output_file_name] = output_file_lock

    with output_file_lock:
        if trust_existing and os.path.exists(output_file_name):
            with open(output_file_name, "r") as r:
                return json.load(r)

        df = pd.read_csv(Path(output_source.uri) / network)

        topology, svg_image = get_network_topology(df) if include_topology else (None, None)
        network = get_network_segment_info(df, topology)

        subsurface_mapping = (
            get_subsurface_mapping(Path(output_source.uri) / subsurface_mapping)
            if subsurface_mapping is not None
            else None
        )

        network_info = {
            "networks": network,
            "subsurface_mapping": subsurface_mapping,
            "topology": [
                {
                    "from": {
                        "network": c["Network"] if c["Network"].__class__ != pd.NA.__class__ else None,
                        "segment": [c["BranchEquipment"], c["Segment"]],
                    },
                    "to": {
                        "network": c["Network_b"] if c["Network_b"].__class__ != pd.NA.__class__ else None,
                        "segment": [c["BranchEquipment_b"], c["Segment_b"]],
                    },
                }
                for c in (topology.to_dict("records") if topology is not None else [])
            ],
        }

        with open(output_file_name, "w") as output_file:
            json.dump(network_info, output_file)

        if svg_image:
            with open(output_file_image_name, "w") as output_file:
                output_file.write(svg_image)

    return network_info


def get_subsurface_mapping(file_path):
    df = pd.read_csv(file_path)

    # Try to sort cluster numerically and
    cluster_names = [(next(iter(re.findall(r"\d+", x)), None), x) for x in df["ClusterName"].unique()]
    cluster_with_numbers = [
        ((cluster_name.split(cluster_no, 1)[0], int(cluster_no)), cluster_name)
        for (cluster_no, cluster_name) in cluster_names
        if cluster_no is not None
    ]
    max_cluster_number = max(x[0][1] for x in cluster_with_numbers) + 1
    cluster_with_no_numbers = [((x, max_cluster_number), max_cluster_number) for x in cluster_names if x[0] is None]

    sorted_clusters = [x[1] for x in sorted(chain(cluster_with_no_numbers, cluster_with_numbers), key=lambda x: x[0])]

    mapping = OrderedDict()
    for cluster_name in sorted_clusters:
        mapping[cluster_name] = list(
            set(df[df["ClusterName"] == cluster_name]["SubSurfaceName"].dropna().sort_values().to_list())
        )

    assert set(mapping.keys()) == set(df["ClusterName"].unique())

    return mapping


def get_network_segment_info(df, topology=None):
    unique_counts = df.groupby(["Elevation", "Lat", "Long"]).transform("nunique")
    df["num_connections"] = unique_counts["BranchEquipment"]
    network_number = sorted(
        x.item() for x in df["Network"].unique()
    )  # Since these values are going to be seralized, ensure they are python primitives

    if set(network_number) - set(range(1, len(network_number) + 1)):
        raise RuntimeError("Network numbers for flowlines must start in 1 and be consecutive (PE: 1,2,3,4...)")

    network = OrderedDict()
    for n in sorted(network_number):
        network_df = df[df["Network"] == n]
        branches = network_df["BranchEquipment"].unique().tolist()
        network[n] = {
            "connections_by_network": [
                {"from": [c["BranchEquipment"], c["Segment"]], "to": [c["BranchEquipment_b"], c["Segment_b"]]}
                for c in topology[(topology["Network"] == n) & (topology["Network_b"] == n)].to_dict("records")
            ]
            if topology is not None
            else [],
            "connections": [
                {
                    "from": {
                        "network": c["Network"] if c["Network"].__class__ != pd.NA.__class__ else None,
                        "segment": [c["BranchEquipment"], c["Segment"]],
                    },
                    "to": {
                        "network": c["Network_b"] if c["Network_b"].__class__ != pd.NA.__class__ else None,
                        "segment": [c["BranchEquipment_b"], c["Segment_b"]],
                    },
                }
                for c in topology[
                    topology["BranchEquipment"].isin(branches) | topology["BranchEquipment_b"].isin(branches)
                ].to_dict("records")
            ]
            if topology is not None
            else [],
            "branches": {
                b: {
                    "segments": OrderedDict(
                        (data.pop("s"), data)
                        for data in (
                            network_df[network_df["BranchEquipment"] == b]
                            .drop(columns=["BranchEquipment", "Network"])
                            .rename(
                                columns={
                                    "MeasuredDistance": "measured_distance",
                                    "HorizontalDistance": "horizontal_distance",
                                    "Elevation": "elevation",
                                    "IsVertex": "is_vertex",
                                    "IsSink": "is_sink",
                                    "Lat": "lat",
                                    "Long": "long",
                                    "Segment": "s",
                                }
                            )
                            .sort_values("s")
                            .to_dict("records")
                        )
                    ),
                }
                for b in branches
            },
        }

    return network


def get_network_topology(df):

    # Obtain the coordinates and elevation of the first and last segment of each branch equipment
    segment = (
        df.groupby(["Network", "BranchEquipment"])["Segment"]
        .agg({"max", "min"})
        .rename(columns={"max": "Segment_max", "min": "Segment_min"})
    )

    segment_max_mins = (
        pd.concat(
            [
                df.merge(
                    segment,
                    left_on=["Segment", "Network", "BranchEquipment"],
                    right_on=["Segment_min", "Network", "BranchEquipment"],
                    suffixes=("", "_"),
                ),
                df.merge(
                    segment,
                    left_on=["Segment", "Network", "BranchEquipment"],
                    right_on=["Segment_max", "Network", "BranchEquipment"],
                    suffixes=("", "_"),
                ),
            ]
        )
        .sort_values(["Network", "BranchEquipment", "Segment"])
        .drop(columns=["Segment_max", "Segment_min"])
    )

    # Discover segments whose ends overlap by coordinates with other segment ends
    max_min_coordinates = segment_max_mins.merge(segment_max_mins, on=["Long", "Lat", "Elevation"], suffixes=("", "_"))
    # Remove overlapping with itself
    max_min_coordinates = max_min_coordinates[
        max_min_coordinates["BranchEquipment"] != max_min_coordinates["BranchEquipment_"]
    ]
    # Remove unnecesary columns
    max_min_coordinates = max_min_coordinates.rename(
        columns={"BranchEquipment_": "BranchEquipment_b", "Segment_": "Segment_b", "Network_": "Network_b"}
    )
    max_min_coordinates.drop(columns=[x for x in max_min_coordinates.columns if x.endswith("_")], inplace=True)
    max_min_coordinates.drop(
        columns=[
            x
            for x in max_min_coordinates.columns
            if "Segment" not in x and "BranchEquipment" not in x and "Network" not in x
        ],
        inplace=True,
    )

    # Ensure that the segment at left is always lower than the one at right.
    # Like that we can remove duplicates like (0,1), (1, 0)
    bigger = max_min_coordinates[max_min_coordinates["Segment"] > max_min_coordinates["Segment_b"]].copy()
    lower = max_min_coordinates[max_min_coordinates["Segment_b"] >= max_min_coordinates["Segment"]].copy()

    bigger.rename(
        inplace=True,
        columns={
            "Segment": "Segment_b",
            "Segment_b": "Segment",
            "BranchEquipment_b": "BranchEquipment",
            "BranchEquipment": "BranchEquipment_b",
            "Network_b": "Network",
            "Network": "Network_b",
        },
    )

    topology_between_branches = pd.concat(
        [
            bigger[["BranchEquipment", "Segment", "Network", "BranchEquipment_b", "Segment_b", "Network_b"]],
            lower[["BranchEquipment", "Segment", "Network", "BranchEquipment_b", "Segment_b", "Network_b"]],
        ]
    )
    topology_between_branches.drop_duplicates(inplace=True)

    # Next, the necessary connection between the start and end segments of the same branch.
    branch_equipment_min_edges = segment_max_mins.groupby("BranchEquipment")["Segment"].agg("min").reset_index()
    branch_equipment_max_edges = segment_max_mins.groupby("BranchEquipment")["Segment"].agg("max").reset_index()

    # Build the final complete topology. Connections between segments of the same branch belong to branch np.nan
    topology_between_branch_edges = pd.DataFrame().assign(
        BranchEquipment=branch_equipment_min_edges["BranchEquipment"],
        Segment=branch_equipment_min_edges["Segment"],
        Network=np.nan,
        BranchEquipment_b=branch_equipment_max_edges["BranchEquipment"],
        Segment_b=branch_equipment_max_edges["Segment"],
        Network_b=np.nan,
    )

    topology = pd.concat((topology_between_branches, topology_between_branch_edges)).sort_values(
        ["BranchEquipment", "Segment", "BranchEquipment_b", "Segment_b", "Network", "Network_b"]
    )
    topology["Network"] = topology["Network"].astype(float).astype("Int64")
    topology["Network_b"] = topology["Network_b"].astype(float).astype("Int64")

    # Obtain a final compressed topology. Shorten the tuple ('<branch>', <segment>) to '<branch>+<segment')
    # Check first that no branch equipment contains the '+' symbol
    branches_with_plus_sign = segment_max_mins[segment_max_mins["BranchEquipment"].str.contains(r"\+")].size
    if branches_with_plus_sign > 0:
        raise RuntimeError("Some branches are using the plus sign (+) in their names. This is disallowed")

    topology_compressed = pd.DataFrame().assign(
        a=topology["BranchEquipment"] + "+" + topology["Segment"].astype(str),
        b=topology["BranchEquipment_b"] + "+" + topology["Segment_b"].astype(str),
    )

    # Scikit topoly works only with numeric values. We need to assign numerical IDs to each '<branch>+<segment>'
    branch_edge_ids = (
        pd.concat((topology_compressed["a"], topology_compressed["b"]))
        .drop_duplicates()
        .sort_values(0)
        .reset_index()
        .drop(columns="index")
        .reset_index()
        .rename(columns={"index": "id", 0: "edge"})
    )

    full_topology_compressed_with_ids = (
        topology_compressed.merge(branch_edge_ids, left_on="a", right_on="edge", copy=False)
        .drop(columns="edge")
        .rename(columns={"id": "a_id"})
        .merge(branch_edge_ids, left_on="b", right_on="edge", copy=False)
        .drop(columns="edge")
        .rename(columns={"id": "b_id"})
        .sort_values(["a_id", "b_id"])
    )

    # Get a map of all '<branch>+<segment>' and their numerical ids
    key_label_map = full_topology_compressed_with_ids[["a", "a_id"]].drop_duplicates().set_index("a_id").to_dict()["a"]
    key_label_map.update(
        full_topology_compressed_with_ids[["b", "b_id"]].drop_duplicates().set_index("b_id").to_dict()["b"]
    )
    sorted_labels = [key_label_map.get(x) for x in sorted(key_label_map)]
    key_label_df = pd.DataFrame().assign(id=sorted(key_label_map), label=sorted_labels)

    # Number of different '<branch>+<segment>'
    dimens = len(
        pd.concat((full_topology_compressed_with_ids["a"], full_topology_compressed_with_ids["b"])).drop_duplicates()
    )

    # Now build the scikit adjacent csr matrix.
    row = full_topology_compressed_with_ids["a_id"].to_numpy()
    col = full_topology_compressed_with_ids["b_id"].to_numpy()

    graph = Bunch()
    graph.adjacency = sparse.csr_matrix((np.ones(len(row), dtype=bool), (row, col)), shape=(dimens, dimens))
    graph.names = sorted_labels
    graph.name = "facilities_network"

    # Calculate x,y by node k level (directed graph). Improves the presentation in the SVG
    # FIXME: get_core_decomposition is not the best strategy
    k_levels = get_core_decomposition(graph.adjacency)
    # adjacency_matrix = get_largest_connected_component(graph.adjacency)
    key_label_df["k_level"] = k_levels
    key_label_df["x"] = key_label_df["k_level"] * 10
    min_id_by_k_level = key_label_df.groupby("k_level")["id"].min().reset_index().rename(columns={"id": "min_id"})
    key_label_df = key_label_df.merge(min_id_by_k_level, left_on="k_level", right_on="k_level")
    key_label_df["y"] = (key_label_df["id"] - key_label_df["min_id"]) * 30
    key_label_df.drop(columns=["min_id"], inplace=True)
    key_label_df.sort_values("id", inplace=True)

    graph.position = np.stack((key_label_df["x"].to_numpy(), key_label_df["y"].to_numpy())).T

    image = svg_graph(
        graph.adjacency, position=graph.position, names=graph.names, scores=k_levels, scale=10, directed=True
    )

    return topology, image
