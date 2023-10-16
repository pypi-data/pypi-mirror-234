# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['normie', 'normie.compat']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=56.0.0,<57.0.0']

entry_points = \
{'console_scripts': ['doctest = tools.run_tests:run_doctest',
                     'test = tools.run_tests:test']}

setup_kwargs = {
    'name': 'normie',
    'version': '0.3.2a0',
    'description': 'Accurate and efficient normal distribution statistics.',
    'long_description': "# normie - Python package for normal distribution functions\n\n## Examples of use\n\n```\n>>> from normie import cdf, invcdf\n>>> cdf(2.0)\n0.9772498607635498\n>>> invcdf(0.5)\n0.0\n\n```\n\n## How it works.\nThe package uses C code, to be found in src/normie_impl.c\n\nThe code uses a built-in function for the cumulative distribution function, and a polynomial approximation for the inverse.\n\n## Repository\nnormie/ Python code\nsrc/ C code\ntests/ Test code\ntools/ Used by poetry for build/test scripts\nbuild.py Defines how the package including C code is built\nLICENSE MIT License\npyproject.toml Poetry is used for building, testing, dev environment...\nREADME.md This documentation\n\n## Compatibility functions\nTo make it easier to port code to Python or to make interoperable code, there are functions which are designed to be compatible with Excel functions for quantiles of the normal distribution.\n\n```\n>>> from normie.compat.excel import NORM_INV\n>>> NORM_INV(0.23, 1, 0.5)\n0.6305765807628632\n\n```\n\nNote that we don't make any effort to reproduce the exact value given by Excel. In particular, we are not trying to match any bugs (if there are any). We simply define the function NORM_INV to mean exactly what NORM.INV does in Excel, then provide our best possible evaluation.\n",
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': 'Jack Grahl',
    'maintainer_email': 'jack.grahl@gmail.com',
    'url': 'https://github.com/jwg4/normie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
