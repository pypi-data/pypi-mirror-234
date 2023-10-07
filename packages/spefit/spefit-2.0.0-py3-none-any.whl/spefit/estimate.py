"""
Methods for estimating the SPE parameters for potential use in the
initial values for the minimisation
"""

import numpy as np
from numpy.polynomial.polynomial import polyfit
from numba import njit
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from functools import partial

__all__ = ["find_spe_peaks", "calculate_peak_ratio", "estimate_spe_parameters"]


def find_spe_peaks(x, y, min_n_peaks: int = 2, max_n_peaks: int = 5):
    """
    Find the SPE peaks from a binned spectrum using scipy.signal.find_peaks

    Parameters
    ----------
    x : ndarray
        X coordinates of spectrum
    y : ndarray
        Y coordinates of spectrum
    min_n_peaks : int
        Minimum number of peaks required to be found (by iteratively reducing
        the peak prominence required)
        If this number of peaks is not found, then ValueError is raised
    max_n_peaks : int
        Maximum number of peaks to be found before the iterative algorithm
        stops looking

    Returns
    -------
    peak_x : ndarray
        X coordinate (location) of each found peak
    peak_y : ndarray
        Y coordinate (height) of each found peak
    peak_sigma : ndarray
        Sigma (standard deviation) of each found peak
    """
    dx = x[1] - x[0]
    y_max = np.max(y)

    peaks = None
    p_prop = None
    for i in range(50):
        prominence = y_max * (1 - i / 50)
        height = y_max / 10
        peaks, p_prop = find_peaks(y, prominence=prominence, height=height, width=1)
        if len(peaks) >= max_n_peaks:
            break

    if len(peaks) < min_n_peaks:
        raise ValueError(f"Unable to find {min_n_peaks} peaks in spectrum")

    peak_x = x[peaks]
    peak_y = p_prop["peak_heights"]

    # Obtain peak sigma assuming 0 is the baseline for each peak
    width_sigma_ratio = 2 * np.sqrt(2 * np.log(peak_y / p_prop["width_heights"]))
    peak_sigma = p_prop["widths"] * dx / width_sigma_ratio

    return peak_x, peak_y, peak_sigma


@njit(fastmath=True)
def calculate_peak_ratio(k, lambda_, sigma0, sigma1):
    """
    Relationship between the height ratio of the peaks, the average
    illumination, and the peak widths

    Assumes a Poisson distribution of photoelectron probabilities, and
    Gaussian peak shape

    Parameters
    ----------
    k : ndarray or int
        Peak index (i.e. photoelectron), k > 0
    lambda_ : float
        Average illumination
    sigma0 : float
        Contribution of the baseline fluctuations to the peak width
    sigma1 : float
        Contribution of the charge amplification fluctuations to the peak width

    Returns
    -------
    peak_ratio : ndarray or float
        Ratio of peak heights H(k-1)/H(k) for each k

    """
    r = k / lambda_
    return r * np.sqrt(
        (sigma0 ** 2 + k * sigma1 ** 2) / (sigma0 ** 2 + (k - 1) * sigma1 ** 2)
    )


def estimate_spe_parameters(peak_x, peak_y, peak_sigma, disable_pedestal: bool = False):
    """
    Estimate the parameters of the SPE spectrum from the peak positions.
    Useful for improving initial guess before minimization.

    Uses scipy.signal.find_peaks to extract the peaks from the SPE. This
    approach requires multiple distinctive peaks in the SPE spectrum

    Parameters
    ----------
    peak_x : ndarray
        X coordinate (location) of each SPE peak
    peak_y : ndarray
        Y coordinate (height) of each SPE peak
    peak_sigma : ndarray
        Sigma (standard deviation) of each SPE peak
    disable_pedestal : bool
        Set to True if no pedestal peak exists in the charge spectrum
        (e.g. when triggering on a threshold or "dark counting")

    Returns
    -------
    estimates : dict
        Dict containing the estimated values for the SPE parameters
    """
    first_peak_pe = 1 if disable_pedestal else 0  # p.e. of first peak in spectrum
    peak_pe = np.arange(first_peak_pe, len(peak_x) + first_peak_pe)  # p.e. of each peak

    # Linear regression to estimate photoelectron peak properties
    eped, pe = polyfit(peak_pe, peak_x, 1)
    var = np.array(polyfit(peak_pe, peak_sigma ** 2, 1))
    if (var < 0).any():  # Manually define if trouble in estimating
        var = np.array([(pe * 0.2) ** 2, (pe * 0.1) ** 2])
    eped_sigma, pe_sigma = np.sqrt(var)

    # Least squares to estimate the average illumination from the ratios of peak height
    peak_ratio_k = peak_pe[1:]
    peak_ratio = peak_y[:-1] / peak_y[1:]
    f = partial(calculate_peak_ratio, sigma0=eped_sigma, sigma1=pe_sigma)
    lambda_ = curve_fit(f, peak_ratio_k, peak_ratio, bounds=(0, 5), p0=1)[0][0]

    return dict(
        eped=eped, eped_sigma=eped_sigma, pe=pe, pe_sigma=pe_sigma, lambda_=lambda_
    )
