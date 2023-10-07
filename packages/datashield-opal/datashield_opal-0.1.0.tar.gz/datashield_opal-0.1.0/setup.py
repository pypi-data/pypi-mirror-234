# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datashield_opal']

package_data = \
{'': ['*']}

install_requires = \
['datashield>=0.1.0,<0.2.0', 'obiba_opal>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'datashield-opal',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Yannick Marcon',
    'author_email': 'yannick.marcon@obiba.org',
    'maintainer': 'Yannick Marcon',
    'maintainer_email': 'yannick.marcon@obiba.org',
    'url': 'https://www.obiba.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
