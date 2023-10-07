from spefit.common.stats import poisson, normal_pdf, poisson_logpmf
from scipy.stats import poisson as scipy_poisson, norm as scipy_norm
import numpy as np
from numpy.testing import assert_allclose as allclose


def test_poisson_pmf():
    k = np.arange(100) - 10
    mu = np.arange(100) - 10
    with np.errstate(divide="ignore", invalid="ignore"):

        def compare(k, mu):
            allclose(poisson_logpmf(k, mu), scipy_poisson.logpmf(k, mu), rtol=1e-5)

        compare(k, mu)
        compare(np.nan, mu)
        compare(k, np.nan)
        compare(np.nan, np.nan)


def test_poisson():
    k = np.arange(1, 100)
    mu = np.arange(1, 100)
    allclose(poisson(k, mu), scipy_poisson.pmf(k, mu))


def test_normal_pdf():
    x = np.linspace(-10, 10, 100)
    mean = 0
    std = 5
    allclose(normal_pdf(x, mean, std), scipy_norm.pdf(x, mean, std))
