from spefit.pdf.base import PDFParameter, PDF
from spefit.common.stats import normal_pdf
import numpy as np
from numpy.testing import assert_allclose
import pytest


def test_pdf_parameter():
    initial = 1
    limits = (0, 4)
    fixed = True
    multi = True

    param = PDFParameter(initial=initial, limits=limits, fixed=fixed, multi=multi)
    assert param.initial == initial
    assert param.limits == limits
    assert param.fixed is fixed
    assert param.multi is multi

    param = PDFParameter(initial=initial, limits=limits)
    assert param.initial == initial
    assert param.limits == limits
    assert param.fixed is False
    assert param.multi is False


def test_pdf_class():
    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2)),
    )
    pdf = PDF(1, normal_pdf, parameters)
    assert pdf.function == normal_pdf
    assert pdf.n_illuminations == 1
    assert len(pdf.parameters) == 2
    assert pdf.parameters["sigma"].initial == 0.1
    assert np.array_equal(pdf._lookup, np.array([[0, 1]]))

    pdf = PDF(2, normal_pdf, parameters)
    assert pdf.function == normal_pdf
    assert pdf.n_illuminations == 2
    assert len(pdf.parameters) == 2
    assert pdf.parameters["sigma"].initial == 0.1
    assert np.array_equal(pdf._lookup, np.array([[0, 1], [0, 1]]))

    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2), multi=True),
    )
    pdf = PDF(2, normal_pdf, parameters)
    assert pdf.function == normal_pdf
    assert pdf.n_illuminations == 2
    assert len(pdf.parameters) == 3
    assert pdf.parameters["sigma0"].initial == 0.1
    assert pdf.parameters["sigma1"].initial == 0.1
    assert np.array_equal(pdf._lookup, np.array([[0, 1], [0, 2]]))

    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2), multi=True),
        sigma=PDFParameter(initial=0.1, limits=(0, 2), multi=True),
    )
    pdf = PDF(2, normal_pdf, parameters)
    assert pdf.function == normal_pdf
    assert pdf.n_illuminations == 2
    assert len(pdf.parameters) == 4
    assert pdf.parameters["sigma0"].initial == 0.1
    assert pdf.parameters["sigma1"].initial == 0.1
    assert np.array_equal(pdf._lookup, np.array([[0, 2], [1, 3]]))
    key_array = np.array(list(pdf.parameters.keys()))
    assert np.array_equal(key_array[pdf._lookup[0]], ["mean0", "sigma0"])
    assert np.array_equal(key_array[pdf._lookup[1]], ["mean1", "sigma1"])


def test_lookup_parameters():
    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2), multi=True),
    )
    pdf = PDF(2, normal_pdf, parameters)
    pdf.update_parameters_initial(sigma1=0.3)
    pdf.update_parameters_limits(sigma1=(0, 5))
    initial = np.array(list(pdf.initial.values()))
    assert np.array_equal(pdf._lookup_parameters(initial, 0), np.array([0, 0.1]))
    assert np.array_equal(pdf._lookup_parameters(initial, 1), np.array([0, 0.3]))
    assert pdf.limits == dict(mean=(-2, 2), sigma0=(0, 2), sigma1=(0, 5))


def test_call():
    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2), multi=True),
    )
    pdf = PDF(2, normal_pdf, parameters)

    x = np.linspace(-1, 6, 100)
    assert_allclose(pdf(x, np.array([0, 0.1, 0.2]), 0), pdf._function(x, 0, 0.1))
    assert_allclose(pdf(x, np.array([0, 0.1, 0.2]), 1), pdf._function(x, 0, 0.2))

    with pytest.raises(IndexError):
        pdf(x, np.array([0, 0.1, 0.2]), 2)

    with pytest.raises(IndexError):
        pdf(x, np.array([0, 0.1]), 1)

    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        pdf(x, [0, 0.1, 0.2], 1)


def test_update_parameters_initial():
    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2)),
    )
    pdf = PDF(2, normal_pdf, parameters)
    assert pdf.parameters["mean"].initial == 0
    assert pdf.parameters["sigma"].initial == 0.1
    pdf.update_parameters_initial(mean=2, sigma=0.4)
    assert pdf.parameters["mean"].initial == 2
    assert pdf.parameters["sigma"].initial == 0.4

    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2), multi=True),
    )
    pdf = PDF(2, normal_pdf, parameters)
    assert pdf.parameters["mean"].initial == 0
    assert pdf.parameters["sigma0"].initial == 0.1
    assert pdf.parameters["sigma1"].initial == 0.1
    pdf.update_parameters_initial(mean=2, sigma=0.4)
    assert pdf.parameters["mean"].initial == 2
    assert pdf.parameters["sigma0"].initial == 0.4
    assert pdf.parameters["sigma1"].initial == 0.4
    pdf.update_parameters_initial(mean=2, sigma0=0.4, sigma1=0.5)
    assert pdf.parameters["mean"].initial == 2
    assert pdf.parameters["sigma0"].initial == 0.4
    assert pdf.parameters["sigma1"].initial == 0.5

    with pytest.raises(ValueError):
        pdf.update_parameters_initial(mean0=2, sigma0=0.4, sigma1=0.5)

    with pytest.raises(ValueError):
        pdf.update_parameters_initial(mean=2, sigma0=0.4, sigma1=0.5, sigma2=0.5)


def test_update_parameters_limits():
    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2)),
    )
    pdf = PDF(1, normal_pdf, parameters)
    assert pdf.parameters["mean"].limits == (-2, 2)
    assert pdf.parameters["sigma"].limits == (0, 2)
    pdf.update_parameters_limits(mean=(-3, 3), sigma=(0, 4))
    assert pdf.parameters["mean"].limits == (-3, 3)
    assert pdf.parameters["sigma"].limits == (0, 4)

    # Test mutable
    limit = [2, 3]
    # noinspection PyTypeChecker
    pdf.update_parameters_limits(mean=limit)
    assert tuple(pdf.parameters["mean"].limits) == (2, 3)
    limit[0] = 1
    assert tuple(pdf.parameters["mean"].limits) == (2, 3)


def test_update_parameters_fixed():
    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2)),
    )
    pdf = PDF(1, normal_pdf, parameters)
    assert pdf.parameters["mean"].fixed is False
    assert pdf.parameters["sigma"].fixed is False
    pdf.update_parameters_fixed(mean=True, sigma=True)
    assert pdf.parameters["mean"].fixed is True
    assert pdf.parameters["sigma"].fixed is True


# noinspection DuplicatedCode
def test_prepare_multi_illumination_parameters():
    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2)),
    )
    results = PDF._prepare_parameters(parameters, 1)
    parameters, is_multi, lookup = results
    assert len(parameters) == 2
    assert len(is_multi) == 2
    assert len(lookup) == 1
    assert len(lookup[0]) == 2

    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2), multi=True),
        sigma=PDFParameter(initial=0.1, limits=(0, 2), multi=True),
    )
    results = PDF._prepare_parameters(parameters, 1)
    parameters, is_multi, lookup = results
    assert len(parameters) == 2
    assert len(is_multi) == 2
    assert len(lookup) == 1
    assert len(lookup[0]) == 2

    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2), multi=True),
        sigma=PDFParameter(initial=0.1, limits=(0, 2), multi=True),
    )
    results = PDF._prepare_parameters(parameters, 2)
    parameters, is_multi, lookup = results
    assert len(parameters) == 4
    assert len(is_multi) == 2
    assert len(lookup) == 2
    assert len(lookup[0]) == 2


def test_initial():
    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2), multi=True),
    )
    pdf = PDF(2, normal_pdf, parameters)
    pdf.update_parameters_initial(sigma1=0.2)
    assert pdf.initial == dict(mean=0, sigma0=0.1, sigma1=0.2)


def test_n_free_parameters():
    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2), multi=True),
    )
    pdf = PDF(2, normal_pdf, parameters)
    assert pdf.n_free_parameters == 3
    pdf.update_parameters_fixed(sigma1=True)
    assert pdf.n_free_parameters == 2


def test_parameter_names():
    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2), multi=True),
    )
    pdf = PDF(2, normal_pdf, parameters)
    assert pdf.parameter_names == ["mean", "sigma0", "sigma1"]


def test_iminuit_kwargs():
    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2), multi=True),
    )
    pdf = PDF(2, normal_pdf, parameters)
    pdf.update_parameters_initial(sigma1=0.2)
    pdf.update_parameters_limits(sigma1=(1, 2))
    pdf.update_parameters_fixed(sigma1=True)
    kwargs = pdf.iminuit_kwargs
    assert len(kwargs) == 9
    assert kwargs["mean"] == 0
    assert kwargs["sigma0"] == 0.1
    assert kwargs["sigma1"] == 0.2
    assert kwargs["limit_mean"] == (-2, 2)
    assert kwargs["limit_sigma0"] == (0, 2)
    assert kwargs["limit_sigma1"] == (1, 2)
    assert kwargs["fix_mean"] is False
    assert kwargs["fix_sigma0"] is False
    assert kwargs["fix_sigma1"] is True


def test_scipy_kwargs():
    parameters = dict(
        mean=PDFParameter(initial=0, limits=(-2, 2)),
        sigma=PDFParameter(initial=0.1, limits=(0, 2), multi=True),
    )
    pdf = PDF(2, normal_pdf, parameters)
    pdf.update_parameters_initial(sigma1=0.2)
    pdf.update_parameters_limits(sigma1=(1, 2))
    pdf.update_parameters_fixed(sigma1=True)
    kwargs = pdf.scipy_kwargs
    assert len(kwargs) == 2
    assert len(kwargs["x0"]) == 3
    assert kwargs["x0"][0] == 0
    assert kwargs["x0"][1] == 0.1
    assert kwargs["x0"][2] == 0.2
    assert kwargs["bounds"][0] == (-2, 2)
    assert kwargs["bounds"][1] == (0, 2)
    assert kwargs["bounds"][2] == (1, 2)


# noinspection PyPep8Naming,PyArgumentList
@pytest.mark.parametrize("PDFSubclass", PDF.__subclasses__())
def test_pdf_subclasses(PDFSubclass):
    pdf = PDFSubclass(n_illuminations=1)
    x = np.linspace(-5, 100, 1000)
    y = pdf(x, np.array(list(pdf.initial.values())), 0)
    np.testing.assert_allclose(np.trapz(y, x), 1, rtol=1e-3)


# noinspection PyPep8Naming,PyArgumentList
@pytest.mark.parametrize("PDFSubclass", PDF.__subclasses__())
def test_disable_pedestal(PDFSubclass):
    pdf = PDFSubclass(n_illuminations=1, disable_pedestal=True)
    x = np.linspace(-5, 100, 1000)
    y = pdf(x, np.array(list(pdf.initial.values())), 0)
    lambda_ = pdf.initial["lambda_0"]
    pedestal_contribution = np.exp(-lambda_)
    np.testing.assert_allclose(np.trapz(y, x), 1 - pedestal_contribution, rtol=1e-3)


def test_from_name():
    pdf = PDF.from_name("SiPMGentile", n_illuminations=1)
    assert pdf.__class__.__name__ == "SiPMGentile"

    with pytest.raises(ValueError):
        PDF.from_name("NULL", n_illuminations=1)
