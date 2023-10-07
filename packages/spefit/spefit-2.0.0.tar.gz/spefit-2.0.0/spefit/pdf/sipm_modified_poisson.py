from spefit.pdf.base import PDF, PDFParameter
from spefit.common.stats import normal_pdf
from numba import njit, vectorize, float64, int64
from math import exp, sqrt, lgamma, log
from functools import partial

__all__ = ["SiPMModifiedPoisson", "modified_poisson", "sipm_mpoisson"]


class SiPMModifiedPoisson(PDF):
    def __init__(self, n_illuminations: int, disable_pedestal=False):
        """SPE PDF for a SiPM utilising a modified Poisson to include the
        optical crosstalk

        Parameters
        ----------
        n_illuminations : int
            Number of illuminations to simultaneously fit
        disable_pedestal : bool
            Set to True if no pedestal peak exists in the charge spectrum
            (e.g. when triggering on a threshold or "dark counting")
        """
        function = partial(sipm_mpoisson, disable_pedestal=disable_pedestal)
        parameters = dict(
            eped=PDFParameter(initial=0, limits=(-2, 2)),
            eped_sigma=PDFParameter(initial=0.1, limits=(0, 2)),
            pe=PDFParameter(initial=1, limits=(0, 3)),
            pe_sigma=PDFParameter(initial=0.1, limits=(0, 2)),
            opct=PDFParameter(initial=0.2, limits=(0, 1)),
            lambda_=PDFParameter(initial=0.7, limits=(0, 5), multi=True),
        )
        super().__init__(n_illuminations, function, parameters)


@vectorize([float64(int64, float64, float64)], fastmath=True)
def modified_poisson(k, mu, opct):
    """Modified Poisson probabilities for a given mean number per event
    and per opct event.

    Parameters
    ----------
    k : int
        Photoelectron peak number
    mu : float
        The mean number per event
    opct : float
        The mean number per opct event

    Returns
    -------
    probability : float
    """
    mu_dash = mu + k * opct
    # TODO: Use xlogy?
    return mu * exp((k - 1) * log(mu_dash) - mu_dash - lgamma(k + 1))


@njit(fastmath=True)
def sipm_mpoisson(x, eped, eped_sigma, pe, pe_sigma, opct, lambda_, disable_pedestal):
    """SPE spectrum PDF for a SiPM using Gaussian peaks with amplitudes given by
    a modified Poisson formula

    TODO: Explanation/derivation

    Parameters
    ----------
    x : ndarray
        The x values to evaluate at
    eped : float
        Distance of the zeroth peak (electronic pedestal) from the origin
    eped_sigma : float
        Sigma of the zeroth peak, represents spread of electronic noise
    pe : float
        Distance of the first peak (1 photoelectron post opct) from the origin
    pe_sigma : float
        Sigma of the 1 photoelectron peak
    opct : float
        Optical crosstalk probability
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

    # Loop over the possible total number of cells fired
    for k in range(1, 100):
        p = modified_poisson(k, lambda_, opct)

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
