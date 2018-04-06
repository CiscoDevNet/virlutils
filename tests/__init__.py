import os
import unittest
from click.testing import CliRunner
from virl.cli.main import virl
import functools
import sys
import traceback
import pdb


def debug_on(*exceptions):
    if not exceptions:
        exceptions = (AssertionError, )

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except exceptions:
                info = sys.exc_info()
                traceback.print_exception(*info)
                pdb.post_mortem(info[2])
        return wrapper
    return decorator


class BaseTest(unittest.TestCase):

    def setUp(self):
        # Only doing this because we don't have a better way of controlling
        # injection of VIRL_HOST
        os.environ['VIRL_HOST'] = 'localhost'
        os.environ['VIRL_USERNAME'] = 'guest'
        os.environ['VIRL_PASSWORD'] = 'guest'
        runner = CliRunner()
        runner.invoke(virl, ["use", "TEST_ENV"])
