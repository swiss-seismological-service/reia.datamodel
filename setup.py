# Copyright 2018, ETH Zurich - Swiss Seismological Service SED
'''
setup.py for reia.datamodel
'''

import sys

from setuptools import setup

if sys.version_info[:2] < (3, 8):
    raise RuntimeError('Python version >= 3.8 required.')


_authors = ['Nicolas Schmid']

_authors_email = ['nicolas.schmid@sed.ethz.ch']

_install_requires = [
    'sqlalchemy>=1.4.31']

_extras_require = {'dev': [
    'flake8>=4.0.1',
    'autopep8>=1.6.0',
    'typer==0.7.0',
    'psycopg2==2.9.5'
]}

_name = 'reia.datamodel'
_version = 0.1
_description = ('Datamodel for Event Specific Loss calculations.')

_packages = ['reia.datamodel']

_entry_points = {
    'console_scripts': [
        'reia=reia.cli:app'
    ],
}

# ----------------------------------------------------------------------------
setup(
    name=_name,
    version=_version,
    author=' (SED, ETHZ),'.join(_authors),
    author_email=', '.join(_authors_email),
    description=_description,
    license='AGPL',
    packages=_packages,
    entry_points=_entry_points,
    install_requires=_install_requires,
    extras_require=_extras_require,
    include_package_data=True,
    zip_safe=False,
)
