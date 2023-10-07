from spefit.common.basic import binom, xlogy
import scipy.special as scipy_special
import numpy as np
from numpy.testing import assert_allclose


def test_binom():
    n = np.arange(100)
    k = np.arange(100)
    assert_allclose(binom(n, k), scipy_special.binom(n, k))


def test_xlogy():
    x = np.arange(100) - 10
    y = np.arange(100) - 10
    with np.errstate(divide="ignore", invalid="ignore"):
        assert_allclose(xlogy(x, y), scipy_special.xlogy(x, y))
        assert_allclose(xlogy(x, np.nan), scipy_special.xlogy(x, np.nan))
        assert_allclose(xlogy(np.nan, y), scipy_special.xlogy(np.nan, y))
        assert_allclose(xlogy(np.nan, np.nan), scipy_special.xlogy(np.nan, np.nan))
