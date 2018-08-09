"""read the table created by ImageJ multiple measure"""
from typing import Tuple
import csv
import numpy as np
from algorithm.array.main import DataFrame

def read(file_path: str, sample_rate: float) -> DataFrame:
    """open and extract the csv file created by imageJ as multiple measurements of ROIs across time
    The 4th columns are named Mean1, Mean2, ... and that is what we read
    Args:
        file_path: full file path, often the return value of uifunc.FileSelector or
            filename_to_open
        sample_rate: the frame rate of 2p image scanning, load the cfg file to find out.
            Usually its 10.039 or 20
    Returns:
        DataFrame, with each cell a column, each measurement a row
        (data_array, {index_name: index}, {column_level: column_name})
    """
    # sniff the csv file
    header_str = next(open(file_path, 'r'))
    dialect = csv.Sniffer().sniff(header_str)
    all_headers = [x.strip(dialect.quotechar) for x in header_str.split(dialect.delimiter)]
    needed_columns = [idx for idx, x in enumerate(all_headers) if x.startswith('Mean')]
    # load the csv
    if len(needed_columns) > 0:  # if filter for Mean columns
        data = np.genfromtxt(file_path, delimiter=dialect.delimiter, skip_header=1,
                             usecols=[0] + needed_columns)
        index, data = data[:, 0], data[:, 1:]
        headers = [int(all_headers[idx][4:]) for idx in needed_columns]
    else:
        data = np.genfromtxt(file_path, delimiter=dialect.delimiter, skip_header=1)
        index, data = data[:, 0], data[:, 1:]
        headers = [int(x) for x in all_headers[1:]]
    return DataFrame(data.T, [np.array(headers), (index - 1) / sample_rate])

def _extract_int(line: str) -> Tuple[int, int]:
    slice_id, _, x, _, y = line.split()
    return int(round(float(x.split(':')[1]))), int(round(float(y.split(':')[1])))


def get_ij_displacement(file_path: str) -> np.ndarray:
    data = open(file_path, 'r')
    return np.array([_extract_int(line) for line in data], np.int)
