# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['feynamp', 'feynamp.form', 'feynamp.sympy']

package_data = \
{'': ['*']}

install_requires = \
['feynml>=0.2.13', 'feynmodel>=0.0.4', 'python-form', 'sympy']

setup_kwargs = {
    'name': 'feynamp',
    'version': '0.0.3',
    'description': 'Compute Feynman diagrams',
    'long_description': '# FeynAmp\n',
    'author': 'Alexander Puck Neuwirth',
    'author_email': 'alexander@neuwirth-informatik.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/APN-Pucky/feynamp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
