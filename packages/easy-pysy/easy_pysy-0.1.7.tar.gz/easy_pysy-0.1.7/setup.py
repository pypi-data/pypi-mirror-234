# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easy_pysy',
 'easy_pysy.core',
 'easy_pysy.plugins',
 'easy_pysy.utils',
 'easy_pysy.utils.functional']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.85.0,<0.86.0',
 'loguru>=0.6.0,<0.7.0',
 'pendulum>=2.1.2,<3.0.0',
 'requests>=2.28.0,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.6.1,<0.7.0',
 'uvicorn[standard]>=0.18.3,<0.19.0']

setup_kwargs = {
    'name': 'easy-pysy',
    'version': '0.1.7',
    'description': '',
    'long_description': 'None',
    'author': 'Pierre Merienne',
    'author_email': 'pierre.merienne@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.9.2',
}


setup(**setup_kwargs)
