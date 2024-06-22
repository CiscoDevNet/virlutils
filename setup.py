# coding: utf-8
from setuptools import find_packages, setup  # noqa: H301

from virl import __version__

NAME = "virlutils"
CMLNAME = "cmlutils"
VERSION = __version__
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools


def requirements(f):
    with open(f, "r") as fd:
        return fd.read()


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name=NAME,
    version=VERSION,
    description="A collection of utilities for interacting with Cisco Modeling Labs",
    author="Joe Clarke",  # With a big thanks to its original author, Kevin Corbin
    author_email="jclarke@cisco.com",
    url="https://github.com/CiscoDevNet/virlutils",
    entry_points={"console_scripts": ["virl=virl.cli.main:virl", "cml=virl.cli.main:virl"]},
    packages=find_packages(),
    package_data={"virl": ["templates/**/*.j2", "swagger/templates/*", "swagger/static/*", "examples/plugins/*"]},
    include_package_data=True,
    install_requires=requirements("requirements.txt"),
    long_description_content_type="text/markdown",
    long_description=readme(),
    test_suite="tests",
    tests_require=requirements("test-requirements.txt"),
    zip_safe=False,
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
