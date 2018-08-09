from os.path import join
from pkg_resources import resource_filename, Requirement
import numpy as np
from reader.image_j_measure import read

TEST_DATA = "test/data/"

def test_extract_int():
    file_path = resource_filename(Requirement.parse('reader'), join(TEST_DATA, '20170403-chan-1.csv'))
    data = read(file_path, 20)
    assert(data.axes[0][-1] == 9)
    assert(np.isclose(data.mean().mean().values, 235.571118))
    assert(data.shape == (9, 8000))
    assert(np.isclose(data.mean(0).values[0], 248.685))
