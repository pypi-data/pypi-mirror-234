# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_oidc']

package_data = \
{'': ['*']}

install_requires = \
['authlib>=1.2.0,<2.0.0', 'flask>=2.0.0,<3.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'flask-oidc',
    'version': '2.1.0',
    'description': 'OpenID Connect extension for Flask',
    'long_description': 'flask-oidc\n==========\n\n`OpenID Connect <https://openid.net/connect/>`_ support for `Flask <http://flask.pocoo.org/>`_.\n\n.. image:: https://img.shields.io/pypi/v/flask-oidc.svg?style=flat\n   :target: https://pypi.python.org/pypi/flask-oidc\n   :alt: PyPI version\n\n.. image:: https://img.shields.io/pypi/dm/flask-oidc.svg?style=flat\n   :target: https://pypi.python.org/pypi/flask-oidc\n   :alt: Downloads per month\n\n.. image:: https://readthedocs.org/projects/flask-oidc/badge/?version=latest\n   :target: http://flask-oidc.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://github.com/fedora-infra/flask-oidc/actions/workflows/ci.yml/badge.svg?branch=develop\n   :target: https://github.com/fedora-infra/flask-oidc/actions/workflows/ci.yml?query=branch%3Adevelop\n   :alt: Tests Status\n\n\nThis library should work with any standards compliant OpenID Connect provider.\n\nIt has been tested with:\n\n* `Ipsilon <https://ipsilon-project.org/>`_\n\n\nProject status\n==============\n\nThis project is in active development (again).\n',
    'author': 'Erica Ehrhardt',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fedora-infra/flask-oidc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
