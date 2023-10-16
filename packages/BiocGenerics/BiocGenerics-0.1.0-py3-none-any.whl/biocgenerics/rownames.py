from functools import singledispatch
from typing import Any, List

from .utils import _is_package_installed

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@singledispatch
def rownames(x) -> List[str]:
    """Access row names from 2-dimensional representations.

    Args:
        x: Any object.

    Raises:
        NotImplementedError: If ``x`` is not a supported type.

    Returns:
        List[str]: List of row names.
    """
    if hasattr(x, "rownames"):
        return x.rownames

    raise NotImplementedError(f"`rownames` do not exist for class: '{type(x)}'.")


if _is_package_installed("pandas") is True:
    from pandas import DataFrame

    @rownames.register(DataFrame)
    def _rownames_dataframe(x: DataFrame) -> list:
        return x.index


@singledispatch
def set_rownames(x: Any, names: List[str]):
    """Set row names.

    Args:
        x (Any): supported object.
        names (List[str]): New names.

    Raises:
        NotImplementedError: If ``x`` is not a supported type.

    Returns:
        An object with the same type as ``x``.
    """
    raise NotImplementedError(f"Cannot set `rownames` for class: {type(x)}")


if _is_package_installed("pandas") is True:
    from pandas import DataFrame

    @set_rownames.register(DataFrame)
    def _set_rownames_dataframe(x: DataFrame, names: List[str]):
        x.index = names

        return x
