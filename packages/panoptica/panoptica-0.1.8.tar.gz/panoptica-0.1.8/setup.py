# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panoptica']

package_data = \
{'': ['*']}

install_requires = \
['connected-components-3d>=3.12.3,<4.0.0',
 'numpy>=1.20.0,<2.0.0',
 'scipy>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'panoptica',
    'version': '0.1.8',
    'description': 'Panoptic Quality (PQ) computation for binary masks.',
    'long_description': None,
    'author': 'Florian Kofler',
    'author_email': 'florian.kofler@tum.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
