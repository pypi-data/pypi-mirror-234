# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dfv', 'dfv.templatetags']

package_data = \
{'': ['*'], 'dfv': ['static/*', 'templates/dfv/tests/*']}

install_requires = \
['django-htmx>=1.14.0,<2.0.0',
 'django>=4.0.0,<5.0.0',
 'lxml>=4.9.2,<5.0.0',
 'pytest-django>=4.5.2,<5.0.0',
 'pytest-watcher>=0.3.4,<0.4.0',
 'pytest-xdist>=3.3.1,<4.0.0',
 'pytest>=7.4.0,<8.0.0',
 'typeguard',
 'wrapt>=1.15.0,<2.0.0']

extras_require = \
{':extra == "docs"': ['toml>=0.10.2,<0.11.0'],
 'docs': ['Sphinx>=4.3.2,<5.0.0',
          'linkify-it-py>=1.0.3,<2.0.0',
          'myst-parser>=0.16.1,<0.17.0',
          'furo>=2021.11.23,<2022.0.0',
          'sphinx-copybutton>=0.4.0,<0.5.0',
          'sphinx-autobuild>=2021.3.14,<2022.0.0']}

setup_kwargs = {
    'name': 'dfv',
    'version': '0.28.0',
    'description': 'Django Function Views',
    'long_description': '# Django Function Views\n',
    'author': 'Roman Roelofsen',
    'author_email': 'romanroe@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/romanroe/dfv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
