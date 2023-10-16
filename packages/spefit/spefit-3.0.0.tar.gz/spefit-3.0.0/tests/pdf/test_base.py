from spefit.pdf.base import PDFParameter, PDF, PDFSimultaneous, PDFMulti
from spefit.common.stats import normal_pdf
import numpy as np
from numpy.testing import assert_allclose
import pytest


class Normal(PDF):
    def __init__(
        self,
        mean=PDFParameter("mean", 0.0, limits=(-2, 2)),
        sigma=PDFParameter("sigma", 0.1, limits=(0, 2)),
    ):
        super().__init__([mean, sigma])

    def __call__(self, x, parameters, _=0):
        return normal_pdf(x, *parameters)


def test_base():
    pdf = Normal(
        mean=PDFParameter("mean", 0.0, limits=(-2, 2)),
        sigma=PDFParameter("sigma", 0.1, limits=(0, 2)),
    )
    assert len(pdf.parameters) == 2
    assert pdf.parameters[0].name == "mean"
    assert pdf.parameters[1].name == "sigma"
    assert pdf.names == ["mean", "sigma"]
    assert np.array_equal(pdf.initial, [0.0, 0.1])
    assert pdf.limits == [(-2, 2), (0, 2)]
    assert pdf.fixed == [False, False]
    assert pdf.n_free_parameters == 2
    assert pdf.n_pdfs == 1

    x = np.linspace(-1, 6, 100)
    assert_allclose(pdf(x, np.array([0, 0.1]), 0), normal_pdf(x, 0, 0.1))


def test_fixed():
    pdf = Normal(
        mean=PDFParameter("mean", 0.0, limits=(-2, 2)),
        sigma=PDFParameter("sigma", 0.1, limits=(0, 2), fixed=True),
    )
    assert pdf.fixed == [False, True]
    assert pdf.n_free_parameters == 1


def test_simultaneous():
    mean = PDFParameter("mean", 0.0, limits=(-2, 2))
    sigma0 = PDFParameter("sigma0", 0.1, limits=(0, 2))
    sigma1 = PDFParameter("sigma1", 0.5, limits=(0, 3))
    pdf = PDFSimultaneous(
        [
            Normal(mean=mean, sigma=sigma0),
            Normal(mean=mean, sigma=sigma1),
        ]
    )
    assert len(pdf.parameters) == 3
    assert set(pdf.names) == {"mean", "sigma0", "sigma1"}
    assert pdf.n_free_parameters == 3
    assert pdf.n_pdfs == 2

    x = np.linspace(-1, 6, 100)
    array = pdf.get_parameter_array(mean=0, sigma0=0.1, sigma1=0.5)
    assert_allclose(pdf(x, array, 0), normal_pdf(x, 0, 0.1))
    assert_allclose(pdf(x, array, 1), normal_pdf(x, 0, 0.5))


def test_multi():
    pdf = PDFMulti(Normal(), n_multi=3, unshared_parameters=["sigma"])
    assert len(pdf.parameters) == 4
    assert set(pdf.names) == {"mean", "sigma0", "sigma1", "sigma2"}
    assert pdf.n_free_parameters == 4
    assert pdf.n_pdfs == 3

    x = np.linspace(-1, 6, 100)
    array = pdf.get_parameter_array(mean=0, sigma0=0.1, sigma1=0.5, sigma2=0.7)
    assert_allclose(pdf(x, array, 0), normal_pdf(x, 0, 0.1))
    assert_allclose(pdf(x, array, 1), normal_pdf(x, 0, 0.5))
    assert_allclose(pdf(x, array, 2), normal_pdf(x, 0, 0.7))

    with pytest.raises(ValueError):
        PDFMulti(Normal(), n_multi=3, unshared_parameters=["unknown"])


SUBCLASSES = [i for i in PDF.__subclasses__() if i not in [PDFSimultaneous, PDFMulti]]


# noinspection PyArgumentList
@pytest.mark.parametrize("subclass", SUBCLASSES)
def test_pdf_subclasses(subclass):
    pdf = subclass()
    x = np.linspace(-5, 100, 1000)
    for i in range(pdf.n_pdfs):
        y = pdf(x, np.array(list(pdf.initial)), i)
        np.testing.assert_allclose(np.trapz(y, x), 1, rtol=1e-3)
