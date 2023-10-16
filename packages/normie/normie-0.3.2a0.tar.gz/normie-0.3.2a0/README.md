# normie - Python package for normal distribution functions

## Examples of use

```
>>> from normie import cdf, invcdf
>>> cdf(2.0)
0.9772498607635498
>>> invcdf(0.5)
0.0

```

## How it works.
The package uses C code, to be found in src/normie_impl.c

The code uses a built-in function for the cumulative distribution function, and a polynomial approximation for the inverse.

## Repository
normie/ Python code
src/ C code
tests/ Test code
tools/ Used by poetry for build/test scripts
build.py Defines how the package including C code is built
LICENSE MIT License
pyproject.toml Poetry is used for building, testing, dev environment...
README.md This documentation

## Compatibility functions
To make it easier to port code to Python or to make interoperable code, there are functions which are designed to be compatible with Excel functions for quantiles of the normal distribution.

```
>>> from normie.compat.excel import NORM_INV
>>> NORM_INV(0.23, 1, 0.5)
0.6305765807628632

```

Note that we don't make any effort to reproduce the exact value given by Excel. In particular, we are not trying to match any bugs (if there are any). We simply define the function NORM_INV to mean exactly what NORM.INV does in Excel, then provide our best possible evaluation.
