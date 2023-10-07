import numpy as np
import pandas as pd


def _get_file_dataframe(data_file, name):
    with open(data_file) as myfile:
        _ = next(myfile)
        ncol = int(next(myfile).rstrip(" \n"))
        colArray = [next(myfile).split()[0] for _ in range(0, ncol)]
        colArray[-1] = name
        data = np.loadtxt(myfile, skiprows=0)
        return pd.DataFrame(data, columns=colArray)


def preprocess(dat_files):
    for source, col_name in dat_files.items():
        df = _get_file_dataframe(source, col_name)
        yield source, col_name, df
