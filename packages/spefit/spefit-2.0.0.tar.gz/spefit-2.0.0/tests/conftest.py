"""global pytest fixtures"""
from spefit.pdf.base import PDF, PDFParameter
from spefit.container import ChargeContainer
from spefit.common.stats import normal_pdf
import pytest
import numpy as np


@pytest.fixture(scope="session")
def example_pdf():
    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0.1, 1), multi=True),
    )
    return PDF(2, normal_pdf, parameters)


@pytest.fixture(scope="session")
def example_params():
    return np.array([0.5, 0.3, 0.4])


@pytest.fixture(scope="session")
def example_charges(example_pdf, example_params):
    charges = []
    rng = np.random.default_rng(seed=1)
    x = np.linspace(-1, 6, 10000)
    for i in range(example_pdf.n_illuminations):
        y = example_pdf(x, example_params, i)
        p = y / y.sum()
        samples = rng.choice(x, p=p, size=10000)
        charges.append(ChargeContainer(samples, n_bins=60, range_=(-3, 3)))
    return charges
