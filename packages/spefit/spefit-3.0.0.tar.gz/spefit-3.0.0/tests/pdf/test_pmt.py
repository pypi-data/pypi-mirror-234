from spefit.pdf.pmt_single_gaussian import pmt_single_gaussian
import numpy as np


def test_pmt():
    x = np.linspace(-1, 20, 1000)
    lambda_ = 1.0
    y = pmt_single_gaussian(x, 0.0, 0.2, 1.0, 0.1, lambda_, False)
    np.testing.assert_allclose(np.trapz(y, x), 1, rtol=1e-3)

    y = pmt_single_gaussian(x, 0.0, 0.2, 1.0, 0.1, lambda_, True)
    pedestal_contribution = np.exp(-lambda_)
    np.testing.assert_allclose(np.trapz(y, x), 1 - pedestal_contribution, rtol=1e-3)
