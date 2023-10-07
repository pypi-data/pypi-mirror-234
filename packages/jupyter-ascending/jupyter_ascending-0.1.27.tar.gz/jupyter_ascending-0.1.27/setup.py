# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupyter_ascending',
 'jupyter_ascending.handlers',
 'jupyter_ascending.nbextension',
 'jupyter_ascending.notebook',
 'jupyter_ascending.requests',
 'jupyter_ascending.scripts',
 'jupyter_ascending.tests']

package_data = \
{'': ['*'],
 'jupyter_ascending': ['labextension/*'],
 'jupyter_ascending.nbextension': ['static/*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0',
 'editdistance>=0.6.2,<0.7.0',
 'jsonrpcclient>=4.0.3,<5.0.0',
 'jsonrpcserver>=5.0.9,<6.0.0',
 'jupytext>=1.14.4,<2.0.0',
 'loguru>=0.4.1',
 'notebook>=6.5.1,<7.0.0',
 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'jupyter-ascending',
    'version': '0.1.27',
    'description': '',
    'long_description': 'None',
    'author': 'Josh Albrecht',
    'author_email': 'joshalbrecht@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
