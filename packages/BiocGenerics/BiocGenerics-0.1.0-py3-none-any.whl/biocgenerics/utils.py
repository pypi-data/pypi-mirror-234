from typing import Any

__author__ = "jkanche, keviny2"
__copyright__ = "jkanche"
__license__ = "MIT"


def is_list_of_type(x: Any, target_type) -> bool:
    """Checks if ``x`` is a list, and whether all elements of the list are of the same type.

    Args:
        x (Any): Any list-like object.
        target_type (callable): Type to check for, e.g. ``str``, ``int``.

    Returns:
        bool: True if ``x`` is :py:class:`list` or :py:class:`tuple` and
        all elements are of the same type.
    """
    return isinstance(x, (list, tuple)) and all(
        isinstance(item, target_type) for item in x
    )


def _convert_1d_sparse_to_dense(x):
    """Convert 1-dimensional sparse vector to a :py:class:`~numpy.ndarray`.

    Args:
        x: A sparse 1-d array

    Returns:
        ndarray: A numpy ndarray.
    """
    elem = x.todense()

    if elem.shape[0] == 1:
        elem = elem[0]

    return elem


def _convert_sparse_to_dense(x):
    """Convert sparse vector to a :py:class:`~numpy.ndarray`.

    Args:
        x: A sparse 1-d array

    Returns:
        ndarray: A numpy ndarray.
    """
    return x.todense()


def _is_1d_dense_arrays(x) -> bool:
    """Check if all elements in x are 1-dimensional dense arrays.

    Args:
        x: A list of numpy arrays.

    Returns:
        bool: True if all elements are 1d, otherwise False.
    """
    return all(len(y.shape) == 1 for y in x)


def _is_1d_sparse_arrays(x) -> bool:
    """Check if all elements in x are 1-dimensional sparse arrays.

    Args:
        x: A list of scipy arrays.

    Returns:
        bool: True if all elements are 1d, otherwise False.
    """
    return all(y.shape[0] == 1 for y in x)


def _do_arrays_match(x, dim: int):
    all_shapes = [y.shape[dim] for y in x]

    first = all_shapes[0]
    return all(y == first for y in all_shapes)


def _is_package_installed(package_name: str):
    _installed = False
    try:
        exec(f"import {package_name}")
        _installed = True
    except Exception:
        pass

    return _installed
