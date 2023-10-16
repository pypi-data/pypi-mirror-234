from functools import singledispatch
from typing import Any
from warnings import warn

from numpy import concatenate, ndarray

from .utils import (
    _convert_sparse_to_dense,
    _do_arrays_match,
    _is_package_installed,
    is_list_of_type,
)

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@singledispatch
def combine_rows(*x: Any):
    """Combine n-dimensional objects along their first dimension.

    If all elements are :py:class:`~numpy.ndarray`,
    we combine them using numpy's :py:func:`~numpy.concatenate`.

    If all elements are either :py:class:`~scipy.sparse.spmatrix` or
    :py:class:`~scipy.sparse.sparray`, these objects are combined
    using scipy's :py:class:`~scipy.sparse.vstack`.

    If all elements are :py:class:`~pandas.DataFrame` objects, they are combined using
    :py:func:`~pandas.concat` along the first axis.

    Args:
        x (Any): n-dimensional objects to combine.

            All elements of x are expected to be the same class or
            atleast compatible with each other.

    Returns:
        A combined object, typically the same type as the first element in ``x``.
        A :py:class:`~numpy.ndarray`, if the elements are a mix of dense and sparse objects.
    """

    raise NotImplementedError("`combine_rows` method is not implemented for objects.")


def _generic_combine_rows_dense_sparse(x):
    elems = []

    for elem in x:
        if not isinstance(elem, ndarray):
            elem = _convert_sparse_to_dense(elem)

        elems.append(elem)

    if _do_arrays_match(elems, 1) is not True:
        raise ValueError("2nd dimension does not match across all elements.")

    return concatenate(elems)


@combine_rows.register(ndarray)
def _combine_rows_dense_arrays(*x: ndarray):
    if is_list_of_type(x, ndarray):
        if _do_arrays_match(x, 1) is not True:
            raise ValueError("2nd dimension does not match across all elements.")

        return concatenate(x)

    warn("Not all elements are numpy ndarrays.")

    if all([hasattr(y, "shape") for y in x]) is True:
        # assuming it's a mix of numpy and scipy arrays
        return _generic_combine_rows_dense_sparse(x)

    raise ValueError("All elements must be 2-dimensional matrices.")


if _is_package_installed("scipy") is True:
    import scipy.sparse as sp

    def _combine_rows_sparse_arrays(*x):
        if is_list_of_type(x, (sp.sparray, sp.spmatrix)):
            sp_conc = sp.vstack(x)

            if _do_arrays_match(x, 1) is not True:
                raise ValueError("2nd dimension does not match across all elements.")

            first = x[0]
            if isinstance(first, (sp.csr_matrix, sp.csr_array)):
                return sp_conc.tocsr()
            elif isinstance(first, (sp.csc_matrix, sp.csc_array)):
                return sp_conc.tocsc()
            elif isinstance(first, (sp.bsr_matrix, sp.bsr_array)):
                return sp_conc.tobsr()
            elif isinstance(first, (sp.coo_matrix, sp.coo_array)):
                return sp_conc.tocoo()
            elif isinstance(first, (sp.dia_matrix, sp.dia_array)):
                return sp_conc.todia()
            elif isinstance(first, (sp.lil_matrix, sp.lil_array)):
                return sp_conc.tolil()
            else:
                return sp_conc

        warn("Not all elements are scipy sparse arrays.")

        if is_list_of_type(x, (ndarray, sp.sparray, sp.spmatrix)):
            return _generic_combine_rows_dense_sparse(x)

        raise ValueError("All elements must be 2-dimensional matrices.")

    combine_rows.register(sp.sparray, _combine_rows_sparse_arrays)
    combine_rows.register(sp.spmatrix, _combine_rows_sparse_arrays)


if _is_package_installed("pandas") is True:
    from pandas import DataFrame, concat

    @combine_rows.register(DataFrame)
    def _combine_rows_pandas_dataframe(*x):
        if is_list_of_type(x, DataFrame):
            return concat(x, axis=1)

        raise TypeError("All elements must be Pandas DataFrame objects.")
