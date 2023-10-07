from spefit.pdf.base import PDF, PDFParameter
from spefit.common.stats import poisson, normal_pdf
from numba import njit
from math import exp, sqrt
from functools import partial

__all__ = ["PMTSingleGaussian", "pmt_single_gaussian"]


class PMTSingleGaussian(PDF):
    def __init__(self, n_illuminations: int, disable_pedestal=False):
        """SPE PDF for a Photomultiplier Tube consisting of a single gaussian
        per photoelectron

        Parameters
        ----------
        n_illuminations : int
            Number of illuminations to simultaneously fit
        disable_pedestal : bool
            Set to True if no pedestal peak exists in the charge spectrum
            (e.g. when triggering on a threshold or "dark counting")
        """
        function = partial(pmt_single_gaussian, disable_pedestal=disable_pedestal)
        parameters = dict(
            eped=PDFParameter(initial=0, limits=(-2, 2)),
            eped_sigma=PDFParameter(initial=0.1, limits=(0, 2)),
            pe=PDFParameter(initial=1, limits=(0, 3)),
            pe_sigma=PDFParameter(initial=0.1, limits=(0, 2)),
            lambda_=PDFParameter(initial=0.7, limits=(0, 5), multi=True),
        )
        super().__init__(n_illuminations, function, parameters)


@njit(fastmath=True)
def pmt_single_gaussian(x, eped, eped_sigma, pe, pe_sigma, lambda_, disable_pedestal):
    """Simple description of the SPE spectrum PDF for a traditional
    Photomultiplier Tube, with the underlying 1 photoelectron PDF described by
    a single gaussian

    Parameters
    ----------
    x : ndarray
        The x values to evaluate at
    eped : float
        Distance of the zeroth peak (electronic pedestal) from the origin
    eped_sigma : float
        Sigma of the zeroth peak, represents spread of electronic noise
    pe : float
        Distance of the first peak (1 photoelectron) from the origin
    pe_sigma : float
        Sigma of the 1 photoelectron peak
    lambda_ : float
        Poisson mean (average illumination in p.e.)
    disable_pedestal : bool
        Set to True if no pedestal peak exists in the charge spectrum
        (e.g. when triggering on a threshold or "dark counting")

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
        total_sigma = sqrt(k * pe_sigma ** 2 + eped_sigma ** 2)

        # Evaluate probability at each value of x
        spectrum += p * normal_pdf(x, eped + k * pe, total_sigma)

    return spectrum
