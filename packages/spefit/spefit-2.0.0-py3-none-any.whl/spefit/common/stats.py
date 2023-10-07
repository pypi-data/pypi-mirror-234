"""Vectorized forms of common PDFs and PMFs"""
from spefit.common.basic import xlogy
from numba import vectorize, int64, float64
from math import lgamma, exp, sqrt, pi

__all__ = ["poisson_logpmf", "poisson", "normal_pdf"]

SQRT2PI = sqrt(2.0 * pi)


@vectorize([float64(float64, float64)], fastmath=True)
def poisson_logpmf(k, mu):
    """Poisson log-PMF, using a definition that is mathematically
    equivalent but numerically stable to avoid arithmetic overflow.

    Source: https://en.wikipedia.org/wiki/Poisson_distribution
    """
    return xlogy(k, mu) - lgamma(k + 1) - mu


@vectorize([float64(int64, float64)], fastmath=True)
def poisson(k, mu):
    """Poisson PMF, using a definition that is mathematically
    equivalent but numerically stable to avoid arithmetic overflow.

    The result is the probability of observing k events for an average number
    of events per interval, lambda_.

    Source: https://en.wikipedia.org/wiki/Poisson_distribution
    """
    return exp(poisson_logpmf(k, mu))


@vectorize([float64(float64, float64, float64)], fastmath=True)
def normal_pdf(x, mean, std_deviation):
    """Normal PDF

    The result is the probability of observing a value at a position x, for a
    normal distribution described by a mean m and a standard deviation s.

    Source: https://stackoverflow.com/questions/10847007/using-the-gaussian-probability-density-function-in-c
    """
    u = (x - mean) / std_deviation
    return exp(-0.5 * u**2) / (SQRT2PI * std_deviation)
