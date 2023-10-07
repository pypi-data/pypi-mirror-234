import os.path
from itertools import chain, repeat
from multiprocessing.pool import ThreadPool
from pathlib import Path

import numpy as np
import pandas as pd

from preprocessing.facilities.network import preprocess as preprocess_network

VARIABLES = [
    "VolumeFlowrateOilStockTank",
    "VolumeFlowrateLiquidStockTank",
    "Pressure",
    "Watercut",
    "VolumeFlowrateOilInSitu",
    "VolumeFlowrateLiquidInSitu",
    "TotalDistance",
]


def preprocess(
    download_func,
    output_source,
    network,  # network.csv
    flowlines,  # (cases/{group}/SIMULATION_{case}/flowline.csv, ...)
    workers=None,
    progress=None,
    proc_name=None,
    **_,
):
    network_file = network
    flowline_files = flowlines
    output_sub_directory = Path(flowline_files[0]).parents[1]  # cases/{group}  # noqa

    networks = preprocess_network(output_source, network_file, trust_existing=True, include_topology=False)

    branches = pd.DataFrame(
        list(
            chain(
                *(
                    zip(x["branches"].keys(), repeat(int(n), len(x["branches"])))
                    for n, x in networks["networks"].items()
                )
            )
        ),
        columns=["branch", "network"],
    )
    branches.set_index(["branch"], inplace=True)

    def _download_file_data(args):
        input_file_idx, input_file = args
        download_func(input_file, output_source.uri)
        input_file_name = Path(output_source.uri) / input_file

        raw_file_data = pd.read_csv(input_file_name, delimiter=",", dtype=str)

        # raw_file_data.sort_values(['network', 'BranchEquipment', 'TotalDistance'], inplace=True)

        # Add check here only network per branch

        to_retrieve_networks = raw_file_data["BranchEquipment"].isin(branches.index)
        branch_data = raw_file_data[to_retrieve_networks][VARIABLES].astype(np.float32)
        branch_data["branch"] = raw_file_data[to_retrieve_networks]["BranchEquipment"]
        branch_data = branch_data.join(branches, how="left", on=["branch"])
        branch_data["case_no"] = input_file_idx
        branch_data.sort_values(
            ["case_no", "network", "branch", "TotalDistance"], ascending=[True, True, True, True], inplace=True
        )

        return input_file_idx, branch_data

    data_by_file_idx = {}
    max_proc_idx = 0
    with ThreadPool(processes=(workers or 4)) as pool:
        branch_datas = pool.imap(
            _download_file_data,
            sorted((int(x.split(os.path.sep)[-2].split("SIMULATION_")[-1]), x) for x in flowline_files),
        )
        for input_file_idx, branch_data in branch_datas:
            data_by_file_idx[input_file_idx] = branch_data

            if progress:
                max_cur_idx = max(input_file_idx, max_proc_idx)
                if max_cur_idx > max_proc_idx:
                    max_proc_idx = max_cur_idx

                    if proc_name:
                        progress.set_description(proc_name)

                    progress.set_postfix({"process": "flowline", "input": f"{max_proc_idx}/{len(flowline_files)}"})

    merged_dataframe = pd.concat(chain(data_by_file_idx[idx] for idx in sorted(data_by_file_idx.keys())))

    merged_dataframe.to_hdf(output_source.uri / output_sub_directory / "flowline.h5", key="flowline")

    return merged_dataframe
