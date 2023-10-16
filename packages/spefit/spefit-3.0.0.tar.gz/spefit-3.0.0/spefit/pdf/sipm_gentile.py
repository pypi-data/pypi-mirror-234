from spefit.pdf.base import PDF, PDFParameter, PDFSimultaneous
from spefit.pdf.pmt_single_gaussian import DEFAULT_PARAMETERS as _DEFAULT_PARAMETERS
from spefit.common.stats import poisson, normal_pdf
from spefit.common.basic import binom
from numba import njit
from math import exp, sqrt
import numpy.typing as npt
from typing import List, Optional
from dataclasses import replace

__all__ = [
    "DEFAULT_PARAMETERS",
    "SiPMGentile",
    "sipm_gentile",
    "SiPMGentileMultiIllumination",
]


DEFAULT_PARAMETERS = _DEFAULT_PARAMETERS | dict(
    opct=PDFParameter("opct", 0.2, limits=(0, 1)),
)


class SiPMGentile(PDF):
    def __init__(
        self,
        eped=DEFAULT_PARAMETERS["eped"],
        eped_sigma=DEFAULT_PARAMETERS["eped_sigma"],
        pe=DEFAULT_PARAMETERS["pe"],
        pe_sigma=DEFAULT_PARAMETERS["pe_sigma"],
        opct=DEFAULT_PARAMETERS["opct"],
        lambda_=DEFAULT_PARAMETERS["lambda_"],
    ):
        """SPE PDF for a SiPM. Optical crosstalk is included by considering all
        the possible combinations that could result in N p.e. (as described in
        Gentile 2010 https://adsabs.harvard.edu/abs/2010arXiv1006.3263G).

        Parameters
        ----------
        eped : PDFParameter
            Distance of the zeroth peak (electronic pedestal) from the origin.
        eped_sigma : PDFParameter
            Sigma of the zeroth peak, represents spread of electronic noise.
        pe : PDFParameter
            Distance of the first peak (1 photoelectron post opct) from the origin.
        pe_sigma : PDFParameter
            Sigma of the 1 photoelectron peak.
        opct : PDFParameter
            Optical crosstalk probability.
        lambda_ : PDFParameter
            Poisson mean (average illumination in p.e.).
        """
        parameters = [eped, eped_sigma, pe, pe_sigma, opct, lambda_]
        super().__init__(parameters)

    def __call__(
        self,
        x: npt.NDArray[float],
        parameters: npt.NDArray[float],
        _: int = 0,
    ) -> npt.NDArray[float]:
        return sipm_gentile(x, *parameters, disable_pedestal=False)


class SiPMGentileMultiIllumination(PDFSimultaneous):
    def __init__(
        self,
        eped=DEFAULT_PARAMETERS["eped"],
        eped_sigma=DEFAULT_PARAMETERS["eped_sigma"],
        pe=DEFAULT_PARAMETERS["pe"],
        pe_sigma=DEFAULT_PARAMETERS["pe_sigma"],
        opct=DEFAULT_PARAMETERS["opct"],
        lambda_: Optional[List[PDFParameter]] = None,
    ):
        """SPE PDF for a SiPM. Optical crosstalk is included by considering all
        the possible combinations that could result in N p.e. (as described in
        Gentile 2010 https://adsabs.harvard.edu/abs/2010arXiv1006.3263G).

        Supports fitting of multiple illuminations simultaneously.

        Parameters
        ----------
        eped : PDFParameter
            Distance of the zeroth peak (electronic pedestal) from the origin.
        eped_sigma : PDFParameter
            Sigma of the zeroth peak, represents spread of electronic noise.
        pe : PDFParameter
            Distance of the first peak (1 photoelectron post opct) from the origin.
        pe_sigma : PDFParameter
            Sigma of the 1 photoelectron peak.
        opct : PDFParameter
            Optical crosstalk probability.
        lambda_ : List[PDFParameter]
            A list of PDFParameters for the poisson mean (average illumination in p.e.).
            Length of the list defines the number of illuminations for the
            simultaneous fit. Default: 3 illuminations.
        """
        lambda_ = lambda_ or [
            replace(DEFAULT_PARAMETERS["lambda_"], name=f"lambda_{i}") for i in range(3)
        ]
        pdfs = []
        for illumination in lambda_:
            parameters = [eped, eped_sigma, pe, pe_sigma, opct, illumination]
            pdfs.append(SiPMGentile(*parameters))
        super().__init__(pdfs)


@njit(fastmath=True)
def sipm_gentile(
    x: npt.NDArray[float],
    eped,
    eped_sigma,
    pe,
    pe_sigma,
    opct,
    lambda_,
    disable_pedestal,
) -> npt.NDArray[float]:
    """PDF for the SPE spectrum of a SiPM as defined in Gentile 2010
    https://adsabs.harvard.edu/abs/2010arXiv1006.3263G
    (Afterpulsing is assumed to be negligible).

    Parameters
    ----------
    x : ndarray
        The x values to evaluate at.
    eped : float
        Distance of the zeroth peak (electronic pedestal) from the origin.
    eped_sigma : float
        Sigma of the zeroth peak, represents spread of electronic noise.
    pe : float
        Distance of the first peak (1 photoelectron post opct) from the origin.
    pe_sigma : float
        Sigma of the 1 photoelectron peak.
    opct : float
        Optical crosstalk probability.
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

    pk_max = 0  # Track when the peak probabilities start to become insignificant

    # Loop over the possible total number of cells fired
    for k in range(1, 100):
        pk = 0
        for j in range(1, k + 1):
            pj = poisson(j, lambda_)  # Probability for j initial fired cells

            # Skip insignificant probabilities
            if pj < 1e-4:
                continue

            # Sum the probability from the possible combinations which result
            # in a total of k fired cells to get the total probability of k
            # fired cells
            pk += pj * pow(1 - opct, j) * pow(opct, k - j) * binom(k - 1, j - 1)

        # Skip insignificant probabilities
        if pk > pk_max:
            pk_max = pk
        elif pk < 1e-4:
            break

        # Combine spread of pedestal and pe peaks
        total_sigma = sqrt(k * pe_sigma**2 + eped_sigma**2)

        # Evaluate probability at each value of x
        spectrum += pk * normal_pdf(x, eped + k * pe, total_sigma)

    return spectrum
