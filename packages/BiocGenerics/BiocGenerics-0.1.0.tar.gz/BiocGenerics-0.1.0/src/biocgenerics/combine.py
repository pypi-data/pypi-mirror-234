from functools import singledispatch
from typing import Any

from numpy import ndarray

from .combine_rows import combine_rows
from .combine_seqs import combine_seqs
from .utils import _is_1d_dense_arrays, _is_1d_sparse_arrays, _is_package_installed

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@singledispatch
def combine(*x: Any):
    """Generic combine that delegates calls to :py:func:`~biocgenerics.combine_seqs.combine_seqs` for 1-dimensional or
    vector like objects, or :py:func:`~biocgenerics.combine_rows.combine_rows` for n-dimensional objects.

    Args:
        x (Any): Objects to combine.

            All elements of ``x`` are expected to be the same class or
            atleast compatible with each other.

    Returns:
        A combined object, typically the same type as the first element in ``x``.
    """

    raise NotImplementedError("`combine` method is not implemented for objects.")


@combine.register(list)
def _combine_lists(*x: list):
    return combine_seqs(*x)


@combine.register(ndarray)
def _combine_dense_arrays(*x: ndarray):
    if _is_1d_dense_arrays(x) is True:
        return combine_seqs(*x)

    return combine_rows(*x)


if _is_package_installed("scipy") is True:
    import scipy.sparse as sp

    def _combine_sparse(*x):
        if _is_1d_sparse_arrays(x) is True:
            return combine_seqs(*x)

        return combine_rows(*x)

    combine_seqs.register(sp.sparray, _combine_sparse)
    combine_seqs.register(sp.spmatrix, _combine_sparse)


if _is_package_installed("pandas") is True:
    from pandas import DataFrame, Series

    @combine.register(Series)
    def _combine_series(*x):
        return combine_seqs(*x)

    @combine.register(DataFrame)
    def _combine_df(*x):
        return combine_seqs(*x)
