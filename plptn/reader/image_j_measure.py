"""read the table created by ImageJ multiple measure"""
import csv
from typing import Tuple

import numpy as np
import pandas as pd


def read(file_path: str, sample_rate: float) -> pd.DataFrame:
    """open and extract the csv file created by imageJ as multiple measurements of ROIs across time
    The 4th columns are named Mean1, Mean2, ... and that is what we read
    Args:
        file_path: full file path, often the return value of uifunc.FileSelector or
            filename_to_open
        sample_rate: the frame rate of 2p image scanning, load the cfg file to find out.
            Usually its 10.039 or 20
    Returns:
        pandas DataFrame, with each cell a column, each measurement a row
    """
    dialect = csv.Sniffer().sniff(open(file_path, 'r').readline())
    data = pd.read_csv(file_path, dialect=dialect)  # type: pd.DataFrame
    columns_need_filter = False
    for column_name in data.columns:
        if 'Mean' in column_name:
            columns_need_filter = True
            break
    if columns_need_filter:
        result = data[[column_name for column_name in data.columns if "Mean" in column_name]]
        result.columns = np.array([int(column_name[4:]) for column_name in result.columns], dtype=int)
    else:
        result = data[[column_name for column_name in data.columns
                       if ("Unnamed:" not in column_name) and ("time" not in column_name)]]
        result.columns = np.array([int(x) for x in result.columns], dtype=int)
    result.index = (result.index + 0.5) / sample_rate
    return result


def _extract_int(line: str) -> Tuple[int, int]:
    slice_id, _, x, _, y = line.split()
    return int(round(float(x.split(':')[1]))), int(round(float(y.split(':')[1])))


def get_ij_displacement(file_path: str) -> np.ndarray:
    data = open(file_path, 'r')
    return np.array([_extract_int(line) for line in data], np.int)
