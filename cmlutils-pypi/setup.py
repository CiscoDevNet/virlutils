# coding: utf-8
from setuptools import setup, find_packages  # noqa: H301
import io

NAME = "cmlutils"
VERSION = "0.0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "virlutils"
]

def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name=NAME,
    version=VERSION,
    description="A collection of utilities for interacting with Cisco Modeling Labs",
    author="Hank Preston",
    author_email="hapresto@cisco.com",
    url="https://github.com/CiscoDevNet/virlutils",
    install_requires=REQUIRES,
    packages=find_packages(),
    long_description=readme(),
)
