"""Collection of PDFs which describe single photoelectron spectra"""
from .base import PDFParameter, PDF, PDFSimultaneous
from .pmt_single_gaussian import PMTSingleGaussian, PMTSingleGaussianMultiIllumination
from .sipm_gentile import SiPMGentile, SiPMGentileMultiIllumination
from .sipm_modified_poisson import SiPMModifiedPoisson

__all__ = [
    "PDFParameter",
    "PDF",
    "PDFSimultaneous",
    "PMTSingleGaussian",
    "PMTSingleGaussianMultiIllumination",
    "SiPMGentile",
    "SiPMGentileMultiIllumination",
    "SiPMModifiedPoisson",
]
