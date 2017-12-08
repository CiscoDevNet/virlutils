# coding: utf-8
from setuptools import setup, find_packages  # noqa: H301

NAME = "virlutils"
VERSION = "0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "click",
    "requests",
    "urllib3 >= 1.15",
    "six >= 1.10",
    "certifi",
    "python-dateutil",
    "docopt"
]

setup(
    name=NAME,
    version=VERSION,
    description="VIRL CLI",
    author_email="",
    url="",
    install_requires=REQUIRES,
    entry_points={"console_scripts": [
        "virl=virl.cli.main:cli",
    ]},
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    VIRL Command Line Utilities  # noqa: E501
    """
)
