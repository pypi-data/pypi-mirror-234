"""global pytest fixtures"""
from spefit.pdf.base import PDF, PDFParameter, PDFSimultaneous
from spefit.dataset import Dataset
from spefit.common.stats import normal_pdf
import pytest
import numpy as np


class Normal(PDF):
    def __init__(
        self,
        mean=PDFParameter("mean", 0.0, limits=(-2, 2)),
        sigma=PDFParameter("sigma", 0.1, limits=(0, 2)),
    ):
        super().__init__([mean, sigma])

    def __call__(self, x, parameters, _=0):
        return normal_pdf(x, *parameters)


@pytest.fixture(scope="session")
def example_pdf():
    mean = PDFParameter("mean", 0.0, limits=(-2, 2))
    sigma0 = PDFParameter("sigma0", 0.1, limits=(0.1, 1))
    sigma1 = PDFParameter("sigma1", 0.1, limits=(0.1, 1))
    return PDFSimultaneous(
        [
            Normal(mean=mean, sigma=sigma0),
            Normal(mean=mean, sigma=sigma1),
        ]
    )


@pytest.fixture(scope="session")
def example_params(example_pdf: PDFSimultaneous):
    return example_pdf.get_parameter_array(mean=0.5, sigma0=0.3, sigma1=0.4)


@pytest.fixture(scope="session")
def example_charges(example_pdf: PDF, example_params):
    charges = []
    rng = np.random.default_rng(seed=1)
    x = np.linspace(-1, 6, 10000)
    for i in range(example_pdf.n_pdfs):
        y = example_pdf(x, example_params, i)
        p = y / y.sum()
        samples = rng.choice(x, p=p, size=10000)
        charges.append(Dataset(samples, n_bins=60, range_=(-3, 3)))
    return charges
