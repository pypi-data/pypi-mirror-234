# spefit 

[![pipeline status](https://gitlab.cta-observatory.org/cta-consortium/aswg/tools/spefit/badges/master/pipeline.svg)](https://gitlab.cta-observatory.org/cta-consortium/aswg/tools/spefit/-/commits/master) [![coverage report](https://gitlab.cta-observatory.org/cta-consortium/aswg/tools/spefit/badges/master/coverage.svg)](https://gitlab.cta-observatory.org/cta-consortium/aswg/tools/spefit/-/commits/master) <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a> [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.cta-observatory.org%2Fcta-consortium%2Faswg%2Ftools%2Fspefit/master?filepath=tutorials)

Optimised framework for the fitting of [Single Photoelectron Spectra](https://github.com/watsonjj/spefit/wiki/Single-Photoelectron-spectra) (SPE) in order to characterize the properties of photomultipliers which influence the measured illumination response.

* Supported Python versions: 3.9+
* Supported platforms: Linux, OSX
* Source: <https://gitlab.cta-observatory.org/cta-consortium/aswg/tools/spefit>
* License: [BSD-3-Clause](LICENSE)
* Citation: _pending_

## Package Features

* Basic [numpy](https://numpy.org/) API
* Runtime-selectable Probability Density Functions (PDFs), optimised using [numba](http://numba.pydata.org/)
* PDFs for the SPE spectra of both Photomultiplier Tubes and Silicon Photomultipliers
* Configuration of PDFs for the case where no pedestal peak exists (e.g. dark counting)
* Estimation of SPE parameters for improved initial fit values
* Runtime-selectable minimization cost definitions, optimised using numba
* Simultaneous fitting of multiple datasets (e.g. containing different average illuminations) for better parameter constraining
* Minimization provided by [iminuit](https://github.com/scikit-hep/iminuit) - Python frontend to the MINUIT2 C++ library
* Calculation of parameter errors and resulting p-value
* Extendable to allow the inclusion of any additional SPE description and minimization cost definitions
* Compatible with other minimization routines
* Convenience class provided for the parallel processing of cameras containing multiple photomultiplier pixels

## Currently Implemented:
### SPE formula:

- PMT Single Gaussian
- SiPM Gentile
- SiPM Modified Poisson

### Minimization Cost functions:

- Unbinned Negative Log-likelihood
- Binned Negative Log-likelihood
- Least Squares

## Installation

The package is available via pypi:
```
pip install spefit
```

Alternatively, this package is installable via pip directly from this repository (via https or ssh), e.g.:
```
pip install 'git+https://gitlab.cta-observatory.org/cta-consortium/aswg/tools/spefit.git#egg=spefit'
```
Also see the [Makefile](Makefile) for development commands.

## Optional Dependencies

Utilisation of Intel's short vector math library (SVML) for improved performance provided by numba:
```
conda install -c numba icc_rt
```

## Usage

With a numpy array of size (n_events) called `charge_array`, containing the measured charges from the low illumination of a photomultiplier, the parameters of the SPE spectra can be extracted with:

```python
from spefit.dataset import Dataset
from spefit.pdf import PMTSingleGaussian
from spefit.cost import BinnedNLL
from spefit.fitter import minimize_with_iminuit

charges = [Dataset(charge_array, n_bins=100, range_=(-3, 6))]
pdf = PMTSingleGaussian()
cost = BinnedNLL(pdf, charges)
values, errors = minimize_with_iminuit(cost)
```

Jupyter notebook demonstrations are provided in [tutorials](tutorials).
