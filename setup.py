# coding: utf-8
from setuptools import setup, find_packages  # noqa: H301
import io
from virl import __version__

NAME = "virlutils"
VERSION = __version__
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "click",
    "gunicorn",
    "requests>=2.20.0",
    "urllib3>=1.23",
    "six >= 1.10",
    "certifi",
    "flask>=0.12.3",
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


def readme():
    with io.open('README.rst', encoding='utf-8') as f:
        return f.read()


setup(
    name=NAME,
    version=VERSION,
    description="A collection of utilities for interacting with Cisco VIRL",
    author="Kevin Corbin",
    author_email="kecorbin@cisco.com",
    url="https://github.com/CiscoDevNet/virlutils",
    install_requires=REQUIRES,
    entry_points={"console_scripts": [
        "virl=virl.cli.main:virl",
    ]},
    packages=find_packages(),
    package_data={'virl': ['templates/**/*.j2',
                           'swagger/templates/*',
                           'swagger/static/*']},
    include_package_data=True,
    long_description=readme(),
    test_suite='tests',
    tests_require=test_requirements,
    zip_safe=False
)
