from spefit.dataset import Dataset
from spefit.cost import UnbinnedNLL, BinnedNLL, LeastSquares
from spefit.pdf import PDF
import numpy as np
import pytest


def test_charge_container():
    rng = np.random.default_rng(seed=0)
    samples = rng.uniform(0, 100, 10000)
    bins = 100
    range_ = (40, 60)
    charge = Dataset(samples, n_bins=bins, range_=range_)
    assert (charge.values >= range_[0]).all()
    assert (charge.values <= range_[1]).all()
    assert charge.hist.size == bins


def test_prebinned(example_pdf: PDF, example_params):
    x = np.linspace(-1, 5, 1000)
    charges = []
    for i in range(example_pdf.n_pdfs):
        y = example_pdf(x, example_params, i)
        charges.append(Dataset.from_prebinned(x, y))

    with pytest.raises(ValueError):
        UnbinnedNLL(example_pdf, charges)

    cost = BinnedNLL(example_pdf, charges)
    cost(example_params)

    cost = LeastSquares(example_pdf, charges)
    cost(example_params)
