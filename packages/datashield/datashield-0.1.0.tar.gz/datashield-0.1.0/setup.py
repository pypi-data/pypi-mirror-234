# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datashield']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'datashield',
    'version': '0.1.0',
    'description': 'DataSHIELD Client Interface in Python.',
    'long_description': '# DataSHIELD Interface Python\n\nThis DataSHIELD Client Interface is a Python port of the original DataSHIELD Client Interface written in R ([DSI](https://github.com/datashield/DSI)). The provided interface can be implemented for accessing a data repository supporting the DataSHIELD infrastructure: controlled R commands to be executed on the server side are garanteeing that non disclosive information is returned to client side.\n',
    'author': 'Yannick Marcon',
    'author_email': 'yannick.marcon@obiba.org',
    'maintainer': 'Yannick Marcon',
    'maintainer_email': 'yannick.marcon@obiba.org',
    'url': 'https://www.datashield.org',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
