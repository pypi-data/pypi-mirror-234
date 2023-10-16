# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clarite',
 'clarite.cli',
 'clarite.cli.commands',
 'clarite.internal',
 'clarite.modules',
 'clarite.modules.analyze',
 'clarite.modules.analyze.regression',
 'clarite.modules.analyze.regression.r_code',
 'clarite.modules.plot',
 'clarite.modules.survey']

package_data = \
{'': ['*']}

install_requires = \
['click>7',
 'importlib-metadata>=5.2.0,<6.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.24,<2.0',
 'pandas-genomics>=0.12,<0.13',
 'pandas>=1.3,<2.0',
 'rpy2>=3.4.5,<4.0.0',
 'scipy>=1.9,<2.0',
 'seaborn>0.9',
 'statsmodels>=0.13,<0.14',
 'tzlocal>=2.1,<3.0']

extras_require = \
{'docs': ['sphinx>=3.2.1,<4.0.0',
          'numpydoc>=1.1.0,<2.0.0',
          'sphinx_rtd_theme>=0.5.0,<0.6.0',
          'sphinx-copybutton>=0.3.0,<0.4.0',
          'ipython>=7.18.1,<8.0.0',
          'sphinx-click>=4,<5']}

entry_points = \
{'console_scripts': ['clarite-cli = clarite.cli:entry_point']}

setup_kwargs = {
    'name': 'clarite',
    'version': '2.3.5',
    'description': 'CLeaning to Analysis: Reproducibility-based Interface for Traits and Exposures',
    'long_description': '.. image:: https://raw.githubusercontent.com/HallLab/clarite-python/master/docs/source/_static/clarite_logo.png\n   :target: https://clarite-python.readthedocs.io/en/stable/\n   :align: center\n   :alt: CLARITE Logo\n\n------------\n\n.. image:: https://img.shields.io/badge/python-3.7+-blue.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/clarite\n   :alt: Python version\n\n.. image:: https://img.shields.io/pypi/v/clarite.svg?style=flat-square\n   :target: https://pypi.org/project/clarite/\n   :alt: PyPI\n\n.. image:: https://img.shields.io/github/workflow/status/HallLab/clarite-python/CI?style=flat-square\n   :target: https://github.com/HallLab/clarite-python/actions?query=workflow%3ACI\n   :alt: Build status\n\n.. image:: https://img.shields.io/readthedocs/clarite-python?style=flat-square\n   :target: https://clarite-python.readthedocs.io/en/latest/\n   :alt: Docs\n\n.. image:: https://img.shields.io/codecov/c/gh/HallLab/clarite-python.svg?style=flat-square\n   :target: https://codecov.io/gh/HallLab/clarite-python/\n   :alt: Test coverage\n\n.. image:: https://img.shields.io/pypi/l/clarite?style=flat-square\n   :target: https://opensource.org/licenses/BSD-3-Clause\n   :alt: License\n\n.. image:: https://img.shields.io/badge/code%20style-Black-black?style=flat-square\n   :target: https://github.com/psf/black\n   :alt: Black\n\n------------\n\nCLeaning to Analysis: Reproducibility-based Interface for Traits and Exposures\n==============================================================================\n\n* Free software: 3-clause BSD license\n* Documentation: https://www.hall-lab.org/clarite-python/.\n\nExamples\n--------\n\n**Run an EWAS in a few lines of code**\n\n.. image:: docs/source/_static/code/quick_ewas.png\n\n|\n\n**More realistically, perform some QC first:**\n\n.. image:: docs/source/_static/code/filters.png\n\n|\n\n**Genotype data is supported via Pandas-Genomics**\n\n.. image:: docs/source/_static/code/gwas.png\n\nInstallation\n------------\n\nIn order to use the *r_survey* regression_kind in the *ewas* function, R must be installed along with the *survey* library.\n\n1. Install R and ensure it is accessible from the command line.  You may need to add its location to the PATH environmental variable.\n2. Use *install.packages* in R to install the *survey* library.\n\nQuestions\n---------\nIf you have any questions not answered by the `documentation <https://clarite-python.readthedocs.io/en/latest/>`_,\nfeel free to open an `Issue <https://github.com/HallLab/clarite-python/issues>`_.\n\nCiting CLARITE\n--------------\n\n1.\nLucas AM, et al (2019)\n`CLARITE facilitates the quality control and analysis process for EWAS of metabolic-related traits. <https://www.frontiersin.org/article/10.3389/fgene.2019.01240>`_\n*Frontiers in Genetics*: 10, 1240\n\n2.\nPassero K, et al (2020)\n`Phenome-wide association studies on cardiovascular health and fatty acids considering phenotype quality control practices for epidemiological data. <https://www.worldscientific.com/doi/abs/10.1142/9789811215636_0058>`_\n*Pacific Symposium on Biocomputing*: 25, 659\n',
    'author': 'Andre Rico',
    'author_email': 'alr6366@psu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/HallLab/clarite-python/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.11.0',
}


setup(**setup_kwargs)
