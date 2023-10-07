from spefit.pdf.sipm_modified_poisson import (
    modified_poisson,
    sipm_mpoisson,
)
import numpy as np


def test_modified_poisson():
    y = np.zeros(100)
    for i in range(y.size):
        y[i] = modified_poisson(i, 1, 0.4)
    np.testing.assert_allclose(np.sum(y), 1, rtol=1e-3)


def test_sipm_modified_poisson():
    x = np.linspace(-1, 20, 1000)
    lambda_ = 1.0
    y = sipm_mpoisson(x, 0.0, 0.2, 1.0, 0.1, 0.2, lambda_, False)
    np.testing.assert_allclose(np.trapz(y, x), 1, rtol=1e-3)

    y = sipm_mpoisson(x, 0.0, 0.2, 1.0, 0.1, 0.2, lambda_, True)
    pedestal_contribution = np.exp(-lambda_)
    np.testing.assert_allclose(np.trapz(y, x), 1 - pedestal_contribution, rtol=1e-3)
