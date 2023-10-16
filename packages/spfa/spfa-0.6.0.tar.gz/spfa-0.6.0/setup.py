# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spfa', 'spfa.models', 'spfa.plots', 'spfa.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3',
 'matplotlib>=3.5.2',
 'muon>=0.1.3',
 'numba>=0.55.2',
 'numpy>=1.22.4',
 'pandas>=1.4.2',
 'pyro-ppl<1.8.4',
 'pytest',
 'scikit-learn>=1.1.1',
 'scipy>=1.8.1',
 'sphinxcontrib-bibtex>=2.5.0,<3.0.0',
 'torch>=1.13.1,<2.0.0']

extras_require = \
{'docs': ['Sphinx==4.2.0',
          'sphinx-rtd-theme==1.0.0',
          'sphinxcontrib-napoleon==0.7',
          'nbsphinx==0.8.9'],
 'notebook': ['jupyter']}

setup_kwargs = {
    'name': 'spfa',
    'version': '0.6.0',
    'description': 'Probabilistic factor analysis model with covariate guided factors',
    'long_description': '# spFA\n\n# Introduction\n\nHere we present semi-supervised probabilistic Factor Analysis (spFA), a multi-omics integration method, which infers a set of low dimensional latent factors that represent the main sources of variability. spFA enables the discovery of primary sources of variation while adjusting for known covariates and simultaneously disentangling variation that is shared between multiple omics modalities and specific to single modalities. The spFA method is implemented in python using the pyro framework for probabilistic programming.\n\n\n# Installation\n\nTo install `spfa` first create `Python 3.8` environment e.g. by\n\n```\nconda create --name spfa-env python=3.8\nconda activate spfa-env\n```\n\nand install the package using \n\n```\npip install spfa\n```\n\n\n\n# How to use `spfa` for multi-omics analyses\n\nA detailed manual with examples and how to use `spfa` can be found here https://tcapraz.github.io/spFA/index.html.\n\n\n',
    'author': 'capraz',
    'author_email': 'tuemayc@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.1,<3.11.6',
}


setup(**setup_kwargs)
