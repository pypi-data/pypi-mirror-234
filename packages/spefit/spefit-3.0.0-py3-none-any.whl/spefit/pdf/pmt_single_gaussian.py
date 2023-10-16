from spefit.pdf.base import PDF, PDFParameter, PDFSimultaneous
from spefit.common.stats import poisson, normal_pdf
from numba import njit
import numpy.typing as npt
from math import exp, sqrt
from typing import List, Optional
from dataclasses import replace


__all__ = [
    "DEFAULT_PARAMETERS",
    "PMTSingleGaussian",
    "PMTSingleGaussianMultiIllumination",
    "pmt_single_gaussian",
]


DEFAULT_PARAMETERS = dict(
    eped=PDFParameter("eped", 0.0, limits=(-2, 2)),
    eped_sigma=PDFParameter("eped_sigma", 0.1, limits=(0, 2)),
    pe=PDFParameter("pe", 1.0, limits=(0, 3)),
    pe_sigma=PDFParameter("pe_sigma", 0.1, limits=(0, 2)),
    lambda_=PDFParameter("lambda_", 0.7, limits=(0, 5)),
)


class PMTSingleGaussian(PDF):
    def __init__(
        self,
        eped=DEFAULT_PARAMETERS["eped"],
        eped_sigma=DEFAULT_PARAMETERS["eped_sigma"],
        pe=DEFAULT_PARAMETERS["pe"],
        pe_sigma=DEFAULT_PARAMETERS["pe_sigma"],
        lambda_=DEFAULT_PARAMETERS["lambda_"],
    ):
        """
        SPE PDF for a Photomultiplier Tube consisting of a single gaussian
        per photoelectron.

        Parameters
        ----------
        eped : PDFParameter
            Distance of the zeroth peak (electronic pedestal) from the origin.
        eped_sigma : PDFParameter
            Sigma of the zeroth peak, represents spread of electronic noise.
        pe : PDFParameter
            Distance of the first peak (1 photoelectron) from the origin.
        pe_sigma : PDFParameter
            Sigma of the 1 photoelectron peak.
        lambda_ : PDFParameter
            Poisson mean (average illumination in p.e.).
        """
        parameters = [eped, eped_sigma, pe, pe_sigma, lambda_]
        super().__init__(parameters)

    def __call__(
        self,
        x: npt.NDArray[float],
        parameters: npt.NDArray[float],
        _: int = 0,
    ) -> npt.NDArray[float]:
        return pmt_single_gaussian(x, *parameters, disable_pedestal=False)


class PMTSingleGaussianMultiIllumination(PDFSimultaneous):
    def __init__(
        self,
        eped=DEFAULT_PARAMETERS["eped"],
        eped_sigma=DEFAULT_PARAMETERS["eped_sigma"],
        pe=DEFAULT_PARAMETERS["pe"],
        pe_sigma=DEFAULT_PARAMETERS["pe_sigma"],
        lambda_: Optional[List[PDFParameter]] = None,
    ):
        """
        SPE PDF for a Photomultiplier Tube consisting of a single gaussian
        per photoelectron.

        Supports fitting of multiple illuminations simultaneously.

        Parameters
        ----------
        eped : PDFParameter
            Distance of the zeroth peak (electronic pedestal) from the origin.
        eped_sigma : PDFParameter
            Sigma of the zeroth peak, represents spread of electronic noise.
        pe : PDFParameter
            Distance of the first peak (1 photoelectron) from the origin.
        pe_sigma : PDFParameter
            Sigma of the 1 photoelectron peak.
        lambda_ : PDFParameter
            A list of PDFParameters for the poisson mean (average illumination in p.e.).
            Length of the list defines the number of illuminations for the
            simultaneous fit. Default: 3 illuminations.
        """
        lambda_ = lambda_ or [
            replace(DEFAULT_PARAMETERS["lambda_"], name=f"lambda_{i}") for i in range(3)
        ]
        pdfs = []
        for illumination in lambda_:
            parameters = [eped, eped_sigma, pe, pe_sigma, illumination]
            pdfs.append(PMTSingleGaussian(*parameters))
        super().__init__(pdfs)


@njit(fastmath=True)
def pmt_single_gaussian(
    x: npt.NDArray[float],
    eped,
    eped_sigma,
    pe,
    pe_sigma,
    lambda_,
    disable_pedestal,
) -> npt.NDArray[float]:
    """
    Simple description of the SPE spectrum PDF for a traditional
    Photomultiplier Tube, with the underlying 1 photoelectron PDF described by
    a single gaussian.

    Parameters
    ----------
    x : ndarray
        The x values to evaluate at.
    eped : float
        Distance of the zeroth peak (electronic pedestal) from the origin.
    eped_sigma : float
        Sigma of the zeroth peak, represents spread of electronic noise.
    pe : float
        Distance of the first peak (1 photoelectron) from the origin.
    pe_sigma : float
        Sigma of the 1 photoelectron peak.
    lambda_ : float
        Poisson mean (average illumination in p.e.).
    disable_pedestal : bool
        Set to True if no pedestal peak exists in the charge spectrum
        (e.g. when triggering on a threshold or "dark counting").

    Returns
    -------
    spectrum : ndarray
        The y values of the total spectrum.
    """
    # Obtain pedestal peak
    p_ped = 0 if disable_pedestal else exp(-lambda_)
    spectrum = p_ped * normal_pdf(x, eped, eped_sigma)

    p_max = 0  # Track when the peak probabilities start to become insignificant

    # Loop over the possible total number of photoelectrons
    for k in range(1, 100):
        p = poisson(k, lambda_)  # Probability to get k avalanches

        # Skip insignificant probabilities
        if p > p_max:
            p_max = p
        elif p < 1e-4:
            break

        # Combine spread of pedestal and pe peaks
        total_sigma = sqrt(k * pe_sigma**2 + eped_sigma**2)

        # Evaluate probability at each value of x
        spectrum += p * normal_pdf(x, eped + k * pe, total_sigma)

    return spectrum
