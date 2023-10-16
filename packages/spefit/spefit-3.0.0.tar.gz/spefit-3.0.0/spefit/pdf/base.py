from typing import Tuple, List, Sequence
from dataclasses import dataclass, replace
import numpy as np
import numpy.typing as npt
from abc import ABC, abstractmethod
from typing import Optional

__all__ = [
    "PDFParameter",
    "PDF",
    "PDFSimultaneous",
    "PDFMulti",
]


@dataclass(frozen=True)
class PDFParameter:
    """
    Parameter of a PDF.

    Parameters
    ----------
    initial : float
        Starting value for the parameter during the fit.
    limits : Tuple[float, float]
        Range of allowed values for the parameter during the fit.
    fixed : bool
        If True, the parameter is fixed to its initial value and will not
        be optimised in the fit.
    """

    name: str
    initial: float
    limits: Tuple[Optional[float], Optional[float]] = (None, None)
    fixed: bool = False


class PDF(ABC):
    def __init__(self, parameters: List[PDFParameter]):
        """
        Defines a function for the fit to data.

        Parameters
        ----------
        parameters
            ``PDFParameters`` corresponding to the arguments of the pdf function.
            Ordered according to the arguments of the underlying function.
        """
        self._parameters = parameters
        self._names = [p.name for p in self._parameters]
        self._initial = np.array([p.initial for p in self._parameters])
        self._limits = [p.limits for p in self._parameters]
        self._fixed = [p.fixed for p in self._parameters]

        if len(self._names) != len(set(self._names)):
            raise ValueError(f"Duplicate names among parameters: {self._names}")

    @abstractmethod
    def __call__(
        self,
        x: npt.NDArray[float],
        parameters: npt.NDArray[float],
        _: int = 0,  # Placeholder to match signature with PDFSimultaneous
    ) -> npt.NDArray[float]:
        """
        Evaluates the PDF.

        Parameters
        ----------
        x : ndarray
            Values to evaluate the fit function at
        parameters : ndarray
            Array of the parameter values for the fit function.
            Ordered according to the `self._names`.

        Returns
        -------
        ndarray
        """

    @property
    def parameters(self) -> List[PDFParameter]:
        return self._parameters

    @property
    def names(self) -> List[str]:
        """Names for all parameters in the contained PDFs."""
        return self._names

    @property
    def initial(self) -> npt.NDArray[float]:
        """Initial value for all parameters in the contained PDFs."""
        return self._initial

    @property
    def limits(self) -> List[Tuple[float, float]]:
        """Limits for all parameters in the contained PDFs."""
        return self._limits

    @property
    def fixed(self) -> List[bool]:
        """Fixed value for all parameters in the contained PDFs."""
        return self._fixed

    @property
    def n_free_parameters(self) -> int:
        return sum([not i for i in self.fixed])

    @property
    def n_pdfs(self) -> int:
        return 1

    def get_parameter_array(self, **values) -> npt.NDArray[float]:
        """
        Convert named parameter args into the correctly ordered array
        to use with __call__.
        """
        array = np.zeros(len(self._parameters), dtype=float)
        for key, value in values.items():
            index = self._names.index(key)
            array[index] = value
        return array


class PDFSimultaneous(PDF):
    def __init__(self, pdfs: Sequence["PDF"]):
        """
        Combine multiple PDFs which share some parameters for a simultaneous
        fit against a corresponding number of datasets.
        """
        self._pdfs = pdfs

        # Identify the unique parameters
        parameters = set()
        for pdf in self._pdfs:
            for parameter in pdf.parameters:
                parameters.add(parameter)
        self._parameters = list(parameters)  # Freeze the order

        # Build parameter lookup
        self._lookup = []
        for pdf in self._pdfs:
            lookup = np.zeros(len(pdf.parameters), dtype=int)
            for i, parameter in enumerate(pdf.parameters):
                lookup[i] = self._parameters.index(parameter)
            self._lookup.append(lookup)

        super().__init__(parameters=self._parameters)

    def __call__(
        self,
        x: npt.NDArray[float],
        parameters: npt.NDArray[float],
        i_pdf: int = 0,
    ) -> npt.NDArray[float]:
        """
        Evaluates the ith PDF with the parameters which are relevant to it.

        Parameters
        ----------
        x : ndarray
            Values to evaluate the fit function at.
        parameters : ndarray
            Array of the parameter values for all contained PDFs.
            Ordered according to the `self._names`.
        i_pdf : int
            PDF index to evaluate the fit function for.

        Returns
        -------
        ndarray
        """
        pdf = self._pdfs[i_pdf]
        pdf_parameters = parameters[self._lookup[i_pdf]]
        return pdf(x, pdf_parameters)

    @property
    def n_pdfs(self) -> int:
        return len(self._pdfs)


class PDFMulti(PDFSimultaneous):
    def __init__(self, pdf: PDF, n_multi: int, unshared_parameters: List[str]):
        """
        Convenience subclass to PDFSimultaneous to use a single PDF in a
        simultaneous fit where some of the PDFParameters vary between the
        datasets.

        Parameters
        ----------
        pdf : PDF
            The PDF which describes all the datasets.
        n_multi : int
            Number of simultaneous fits to perform (equal to number of datasets).
        unshared_parameters : list(str)
            The names of parameters which vary between the datasets.
        """
        self._n_multi = n_multi
        pdfs = []
        for i in range(n_multi):
            parameters = pdf.parameters.copy()
            for name in unshared_parameters:
                if name not in pdf.names:
                    raise ValueError(f"Expected parameter with name: {name}")

                index = pdf.names.index(name)
                parameters[index] = replace(parameters[index], name=f"{name}{i}")
            parameters_kwargs = dict(zip(pdf.names, parameters))
            pdf_illumination = pdf.__class__(**parameters_kwargs)
            pdfs.append(pdf_illumination)
        super().__init__(pdfs=pdfs)
