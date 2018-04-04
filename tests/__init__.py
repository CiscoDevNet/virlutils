import os
import unittest
from click.testing import CliRunner
from virl.cli.main import virl


class BaseTest(unittest.TestCase):

    def setUp(self):
        # Only doing this because we don't have a better way of controlling
        # injection of VIRL_HOST
        os.environ['VIRL_HOST'] = 'localhost'
        os.environ['VIRL_USERNAME'] = 'guest'
        os.environ['VIRL_PASSWORD'] = 'guest'
        runner = CliRunner()
        runner.invoke(virl, ["use", "TEST_ENV"])
