from spefit.container import ChargeContainer
from spefit.cost import Cost
import iminuit
from scipy.optimize import minimize as scipy_minimize
import numpy as np
from tqdm.autonotebook import trange
import warnings
from multiprocessing import Pool, Manager
from functools import partial
from typing import List, Tuple, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from spefit.pdf.base import PDF

__all__ = ["minimize_with_iminuit", "CameraFitter"]


def minimize_with_iminuit(cost: "Cost") -> (Dict[str, float], Dict[str, float]):
    """Minimize the Cost definition using iminuit"""
    initial = np.array(list(cost.pdf.initial.values()))
    m0 = iminuit.Minuit(cost, initial, name=cost.parameter_names)
    m0.fixed = cost.pdf.fixed.values()
    m0.limits = cost.pdf.limits.values()
    m0.errordef = cost.errordef
    m0.throw_nan = True
    m0.print_level = 0

    # Run Migrad minimization
    m0.migrad()

    # Attempt to run HESSE to compute parabolic errors.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", iminuit.util.HesseFailedWarning)
        m0.hesse()

    values = dict(zip(cost.pdf.parameter_names, m0.values))
    errors = dict(zip(cost.pdf.parameter_names, m0.errors))
    return values, errors


def minimize_with_scipy(cost: "Cost") -> (Dict[str, float], Dict[str, float]):
    """
    Minimize the Cost definition using scipy
    Fixed parameters not currently implemented
    """
    ftol = 2.220446049250313e-09  # Default
    results = scipy_minimize(cost, **cost.scipy_kwargs, tol=ftol)
    values = dict(zip(cost.pdf.parameter_names, results.x))
    error_array = np.sqrt(np.diag(results.hess_inv.todense()) * ftol * results.fun)
    errors = dict(zip(cost.pdf.parameter_names, error_array))
    return values, errors


class CameraFitter:
    def __init__(
        self,
        pdf: "PDF",
        n_bins: int,
        range_: Tuple[float, float],
        cost_name: str = "BinnedNLL",
    ):
        """Convenience class for fitting the charge distributions measured in
        multiple pixels of a camera

        Result of the fit for each pixel can be accessed from the self.pixel_*
        attributes

        Parameters
        ----------
        pdf : PDF
            PDF class assumed to describe the charge distribution
        n_bins : int
            Number of bins for the charge histogram
            (used for binned cost methods and plotting)
        range_ : tuple
            Only charge values between (min, max) are considered in the fit
        cost_name : str
            Name of the Cost subclass to use.
            Must be one of ["UnbinnedNLL", "BinnedNLL", "LeastSquares"]
            Default is "BinnedNLL"
        """
        self._pdf = pdf
        self._cost_name = cost_name
        self._n_bins = n_bins
        self._range = range_

        manager = Manager()
        self.pixel_values = manager.dict()
        self.pixel_errors = manager.dict()
        self.pixel_scores = manager.dict()
        self.pixel_arrays = manager.dict()

    @property
    def n_illuminations(self):
        return self._pdf.n_illuminations

    def _update_initial(self, charges: List["ChargeContainer"]):
        """
        Update the initial parameters of the minimization for each pixel based
        on the measured charge distribution

        Placeholder method for potential overriding by a subclass
        """

    def _apply_pixel(self, charge_arrays: List[np.ndarray], pixel: int):
        """
        Process a single pixel and store result into the
        multiprocessing-managed dicts

        Parameters
        ----------
        charge_arrays : List[ndarray]
            List of size n_illuminations, containing numpy arrays of
            shape (n_events, n_pixels)
        """
        n_illuminations = self._pdf.n_illuminations
        charges = []
        for i in range(n_illuminations):
            c = charge_arrays[i][:, pixel]
            charges.append(ChargeContainer(c, n_bins=self._n_bins, range_=self._range))

        self._update_initial(charges)

        cost = Cost.from_name(self._cost_name, pdf=self._pdf, charges=charges)
        values, errors = minimize_with_iminuit(cost)
        values_array = np.array(list(values.values()))

        # Obtain score of minimization
        try:
            scores = dict(
                chi2=cost.chi2(values_array),
                reduced_chi2=cost.reduced_chi2(values_array),
                p_value=cost.p_value(values_array),
            )
        except ValueError:
            scores = dict(chi2=np.nan, reduced_chi2=np.nan, p_value=np.nan)

        # Obtain resulting arrays for plotting purposes
        fit_x = np.linspace(self._range[0], self._range[1], self._n_bins * 10)
        arrays = []
        for i in range(n_illuminations):
            d = dict(
                charge_hist_x=charges[i].between,
                charge_hist_y=charges[i].hist,
                charge_hist_edges=charges[i].edges,
                fit_x=fit_x,
                fit_y=self._pdf(fit_x, values_array, i),
            )
            arrays.append(d)

        self.pixel_values[pixel] = values
        self.pixel_errors[pixel] = errors
        self.pixel_scores[pixel] = scores
        self.pixel_arrays[pixel] = arrays

    def multiprocess(self, charge_arrays: List[np.ndarray], n_processes: int):
        """
        Fit multiple pixels in parallel using the multiprocessing package

        Parameters
        ----------
        charge_arrays : List[ndarray]
            List of size n_illuminations, containing numpy arrays of
            shape (n_events, n_pixels)
        n_processes : int
            Number of processes to spawn for the parallelization
        """
        print(f"Multiprocessing pixel SPE fit (n_processes = {n_processes})")
        _, n_pixels = charge_arrays[0].shape
        apply = partial(self._apply_pixel, charge_arrays)
        with Pool(n_processes) as pool:
            pool.map(apply, trange(n_pixels))

    def process(self, charge_arrays: List[np.ndarray]):
        """
        Fit multiple pixels in series

        Parameters
        ----------
        charge_arrays : List[ndarray]
            List of size n_illuminations, containing numpy arrays of
            shape (n_events, n_pixels)
        """
        _, n_pixels = charge_arrays[0].shape
        for pixel in trange(n_pixels):
            self._apply_pixel(charge_arrays, pixel)
