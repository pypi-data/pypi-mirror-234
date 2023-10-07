from spefit.cost import (
    _sum_log_x,
    _bin_nll,
    _total_binned_nll,
    _least_squares,
    UnbinnedNLL,
    BinnedNLL,
    LeastSquares,
    Cost,
)
import numpy as np
import pytest


@pytest.fixture(scope="module")
def incorrect():
    return np.array([0.6, 0.3, 0.4])


def test_sum_log_x():
    x = np.linspace(-100, 100, 1000)
    with np.errstate(invalid="ignore"):
        np.testing.assert_allclose(_sum_log_x(x), np.sum(np.log(x)))


def test_bin_nll():
    assert _bin_nll(2, 0) == 2
    with np.errstate(divide="ignore", invalid="ignore"):
        assert np.array_equal(_bin_nll(np.ones(10), np.zeros(10)), np.ones(10))
    assert _bin_nll(2, 1) < 2


def test_total_bin_likelihood(example_pdf, example_charges, example_params, incorrect):
    f_y_correct = example_pdf(example_charges[0].between, example_params, 0)
    f_y_incorrect = example_pdf(example_charges[0].between, incorrect, 0)
    nll_correct = _total_binned_nll(f_y_correct, example_charges[0].hist)
    nll_incorrect = _total_binned_nll(f_y_incorrect, example_charges[0].hist)
    assert nll_correct < nll_incorrect


def test_least_squares_func(example_pdf, example_charges, example_params, incorrect):
    f_y_correct = example_pdf(example_charges[0].between, example_params, 0)
    f_y_incorrect = example_pdf(example_charges[0].between, incorrect, 0)
    chi2_correct = _least_squares(f_y_correct, example_charges[0].hist)
    chi2_incorrect = _least_squares(f_y_incorrect, example_charges[0].hist)
    assert chi2_correct < chi2_incorrect


def test_unbinned_nll(example_pdf, example_charges, example_params, incorrect):
    # N illuminations mismatch
    with pytest.raises(ValueError):
        UnbinnedNLL(example_pdf, [example_charges[0]])

    cost = UnbinnedNLL(example_pdf, example_charges)
    assert cost(example_params) < cost(incorrect)
    assert cost.dof > 0

    with pytest.raises(ValueError):
        cost.chi2(example_params)

    with pytest.raises(ValueError):
        cost.reduced_chi2(example_params)

    with pytest.raises(ValueError):
        cost.p_value(example_params)


# noinspection DuplicatedCode
def test_binned_nll(example_pdf, example_charges, example_params, incorrect):
    cost = BinnedNLL(example_pdf, example_charges)
    assert cost(example_params) < cost(incorrect)
    assert cost.dof > 0
    assert cost.chi2(example_params) < cost.chi2(incorrect)
    assert cost.reduced_chi2(example_params) < cost.reduced_chi2(incorrect)
    assert cost.p_value(example_params) > cost.p_value(incorrect)


# noinspection DuplicatedCode
def test_least_squares(example_pdf, example_charges, example_params, incorrect):
    cost = LeastSquares(example_pdf, example_charges)
    assert cost(example_params) < cost(incorrect)
    assert cost.dof > 0
    assert cost.chi2(example_params) < cost.chi2(incorrect)
    assert cost.reduced_chi2(example_params) < cost.reduced_chi2(incorrect)
    assert cost.p_value(example_params) > cost.p_value(incorrect)


def test_from_name(example_pdf, example_charges):
    fit = Cost.from_name("BinnedNLL", example_pdf, example_charges)
    assert fit.__class__.__name__ == "BinnedNLL"

    with pytest.raises(ValueError):
        Cost.from_name("NULL", example_pdf, example_charges)


@pytest.mark.parametrize("CostSubclass", Cost.__subclasses__())
def test_nan(CostSubclass, example_pdf, example_charges, example_params, incorrect):
    example_params = example_params.copy()
    example_params[0] = np.nan
    cost = CostSubclass(example_pdf, example_charges)
    assert np.isinf(cost(example_params))
