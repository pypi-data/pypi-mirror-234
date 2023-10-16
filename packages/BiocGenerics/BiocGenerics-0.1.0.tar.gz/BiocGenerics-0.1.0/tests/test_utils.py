from biocgenerics.utils import _is_package_installed

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_for_pandas():
    pkg = _is_package_installed("pandas")

    assert pkg is True


def test_for_scipy():
    pkg = _is_package_installed("scipy")

    assert pkg is True
