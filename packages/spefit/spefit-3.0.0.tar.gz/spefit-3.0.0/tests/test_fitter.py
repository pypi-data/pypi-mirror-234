from spefit.fitter import minimize_with_iminuit, minimize_with_scipy, CameraFitter
from spefit.cost import BinnedNLL, Cost
import numpy as np
import pytest


@pytest.fixture(scope="module")
def charge_arrays(example_charges):
    n_pixels = 10
    return [c.values[:, None] * np.ones((1, n_pixels)) for c in example_charges]


def test_minimize_with_iminuit(example_pdf, example_params, example_charges):
    cost = BinnedNLL(example_pdf, example_charges)
    values, errors = minimize_with_iminuit(cost)
    values_array = np.array(list(values.values()))
    errors_array = np.array(list(errors.values()))

    assert values_array.size == errors_array.size
    assert values_array.size == example_params.size
    np.testing.assert_allclose(values_array, example_params, rtol=1e-2)
    assert (errors_array > 0).all()


def test_minimize_with_scipy(example_pdf, example_params, example_charges):
    cost = BinnedNLL(example_pdf, example_charges)
    values, errors = minimize_with_scipy(cost)
    values_array = np.array(list(values.values()))
    errors_array = np.array(list(errors.values()))

    assert values_array.size == errors_array.size
    assert values_array.size == example_params.size
    np.testing.assert_allclose(values_array, example_params, rtol=1e-2)
    assert (errors_array > 0).all()


# noinspection PyPep8Naming
@pytest.mark.parametrize("CostSubclass", Cost.__subclasses__())
def test_camera_fitter(CostSubclass, example_pdf, example_params, charge_arrays):
    name = CostSubclass.__name__
    fitter = CameraFitter(pdf=example_pdf, n_bins=60, range_=(-2, 2), cost_name=name)
    assert fitter.n_pdfs == 2
    fitter._apply_pixel(charge_arrays, 0)
    assert len(fitter.pixel_values) == 1
    assert len(fitter.pixel_errors) == 1
    assert len(fitter.pixel_scores) == 1
    assert len(fitter.pixel_arrays) == 1

    values_array = np.array(list(fitter.pixel_values[0].values()))
    errors_array = np.array(list(fitter.pixel_errors[0].values()))

    np.testing.assert_allclose(values_array, example_params, rtol=1e-2)
    assert (errors_array > 0).all()
    p_value = fitter.pixel_scores[0]["p_value"]
    if not np.isnan(p_value):
        assert fitter.pixel_scores[0]["p_value"] > 0.01
    assert fitter.pixel_arrays[0][0]["hist_y"].size == 60


# noinspection DuplicatedCode
def test_camera_fitter_process(example_pdf, example_params, charge_arrays):
    fitter = CameraFitter(pdf=example_pdf, n_bins=60, range_=(-2, 2))
    fitter.process(charge_arrays)
    n_pixels = charge_arrays[0].shape[1]
    assert len(fitter.pixel_values) == n_pixels
    for ipix in range(n_pixels):
        values_array = np.array(list(fitter.pixel_values[ipix].values()))
        np.testing.assert_allclose(values_array, example_params, rtol=1e-2)


# noinspection DuplicatedCode
def test_camera_fitter_multiprocess(example_pdf, example_params, charge_arrays):
    fitter = CameraFitter(pdf=example_pdf, n_bins=60, range_=(-2, 2))
    fitter.multiprocess(charge_arrays, n_processes=2)
    n_pixels = charge_arrays[0].shape[1]
    assert len(fitter.pixel_values) == n_pixels
    for ipix in range(n_pixels):
        values_array = np.array(list(fitter.pixel_values[ipix].values()))
        np.testing.assert_allclose(values_array, example_params, rtol=1e-2)
