# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "0.1.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="API for NEurostuff (Apine)",
    author_email="",
    url="",
    keywords=["Swagger", "API for NEurostuff (Apine)"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    This is the API for NEurostuff (Apine) server.  You can find  out more about Apine on Github\\: [https://github.com/INCF/apine](https://github.com/INCF/apine). 
    """
)

