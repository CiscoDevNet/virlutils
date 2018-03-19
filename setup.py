# coding: utf-8
from setuptools import setup, find_packages  # noqa: H301

NAME = "virlutils"
VERSION = "0.4"
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
    "docopt",
    "tabulate",
    "pyyaml",
    "jinja2",
    "lxml"
]

test_requirements = [
    "requests_mock",
]

setup(
    name=NAME,
    version=VERSION,
    description="A collection of utilities for interacting with Cisco VIRL",
    author="Kevin Corbin",
    author_email="kecorbin@cisco.com",
    url="https://github.com/kecorbin/virlutils",
    install_requires=REQUIRES,
    entry_points={"console_scripts": [
        "virl=virl.cli.main:virl",
    ]},
    packages=find_packages(),
    package_data={'virl': ['templates/**/*.j2']},
    include_package_data=True,
    long_description="VIRL Command Line Utilities",
    test_suite='tests',
    tests_require=test_requirements,
)
