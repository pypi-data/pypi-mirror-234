import numpy as np
import pandas as pd
from biocgenerics.combine_seqs import combine_seqs
from scipy import sparse as sp

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_basic_list():
    x = [1, 2, "c"]
    y = ["a", "b"]

    z = combine_seqs(x, y)

    assert z == x + y
    assert isinstance(z, list)
    assert len(z) == len(x) + len(y)


def test_basic_dense():
    x = [1, 2, 3]
    y = [0.1, 0.2]
    xd = np.array([1, 2, 3])
    yd = np.array([0.1, 0.2], dtype=float)

    zcomb = combine_seqs(xd, yd)

    z = x + y
    zd = np.array(z)

    assert all(np.isclose(zcomb, zd)) is True
    assert isinstance(zcomb, np.ndarray)
    assert len(zcomb) == len(zd)


def test_basic_mixed_dense_list():
    x = [1, 2, 3]
    y = [0.1, 0.2]
    xd = np.array([1, 2, 3])

    zcomb = combine_seqs(xd, y)

    z = x + y

    assert zcomb == z
    assert isinstance(zcomb, list)
    assert len(zcomb) == len(xd) + len(y)


def test_basic_mixed_tuple_list():
    x = [1, 2, 3]
    y = (0.1, 0.2)
    xd = np.array([1, 2, 3])

    zcomb = combine_seqs(xd, y, x)

    z = x + list(y) + x

    assert zcomb == z
    assert isinstance(zcomb, list)
    assert len(zcomb) == 2 * len(xd) + len(y)


def test_basic_sparse():
    x = np.array([1, 2, 3])
    y = np.array([0.1, 0.2])

    sx = sp.csr_array(x)
    sy = sp.csr_array(y)

    z = combine_seqs(sx, sy)

    assert isinstance(z, sp.spmatrix)
    assert z.shape[1] == len(x) + len(y)

    # mixed sparse arrays
    sx = sp.csr_array(x)
    sy = sp.coo_array(y)

    z = combine_seqs(sx, sy)

    assert isinstance(z, sp.spmatrix)
    assert z.shape[1] == len(x) + len(y)


def test_mixed_sparse_list():
    x = [1, 2, 3]
    y = [0.1, 0.2]
    xd = np.array([1, 2, 3])
    sy = sp.csr_array(y)

    zcomb = combine_seqs(sy, x)

    assert isinstance(zcomb, list)
    assert len(zcomb) == len(xd) + len(y)


def test_mixed_sparse_dense():
    x = np.array([1, 2, 3])
    y = np.array([0.1, 0.2])

    sy = sp.csr_array(y)

    z = combine_seqs(x, sy)

    assert isinstance(z, np.ndarray)
    assert z.shape[0] == len(x) + len(y)


def test_pandas_series():
    s1 = pd.Series(["a", "b"])
    s2 = pd.Series(["c", "d"])

    z = combine_seqs(s1, s2)

    assert isinstance(z, pd.Series)
    assert len(z) == 4

    x = ["gg", "ff"]

    z = combine_seqs(s1, x)
    assert isinstance(z, pd.Series)
    assert len(z) == 4
