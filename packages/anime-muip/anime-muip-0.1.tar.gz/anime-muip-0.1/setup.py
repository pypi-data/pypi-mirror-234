# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anime_muip']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'anime-muip',
    'version': '0.1',
    'description': 'Simple module for anime game servers',
    'long_description': None,
    'author': 'MrM0der',
    'author_email': '124781355+MrM0der@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
