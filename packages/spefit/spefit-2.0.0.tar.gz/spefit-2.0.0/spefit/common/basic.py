"""Vectorized math formulae"""
from numba import vectorize, int64, float64
from math import lgamma, exp, isnan, log

__all__ = [
    "binom",
    "xlogy",
]


@vectorize([float64(int64, int64)], fastmath=True)
def binom(n, k):
    """Obtain the binomial coefficient, using a definition that is mathematically
    equivalent but numerically stable to avoid arithmetic overflow.

    The result of this method is "n choose k", the number of ways choose an
    (unordered) subset of k elements from a fixed set of n elements.

    Source: https://en.wikipedia.org/wiki/Binomial_coefficient
    """
    return exp(lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1))


@vectorize([float64(float64, float64)])
def xlogy(x, y):
    """Compute ``x*log(y)`` so that the result is 0 if ``x = 0``,
    even if y is negative

    Source: ``scipy.special.xlogy``
    """
    if x == 0 and not isnan(y):
        return 0
    else:
        return x * log(y)
