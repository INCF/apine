# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "apine"
VERSION = "0.0.1"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion", "jsonschema", "flask"]

setup(
    name=NAME,
    version=VERSION,
    description="API for Neurostuff",
    author_email="gkiar07@gmail.com",
    url="https://github.com/INCF/Apine",
    keywords=["API for Neurostuff"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['apine=apine.driver:main']},
    long_description="""\
    Extensible querying of arbitrarily organized datasets and schemas
    """
)

