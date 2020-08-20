import os
from . import BaseTest
from click.testing import CliRunner
from virl.cli.main import virl


class UseTest(BaseTest):
    def test_virl_use(self):
        runner = CliRunner()
        result = runner.invoke(virl, ["use", "TEST_ENV"])
        path = './.virl/default/id'
        file_exists = os.path.isfile(path)
        self.assertTrue(file_exists)
        self.assertEqual(0, result.exit_code)
        with open(path, 'r') as fh:
            data = fh.read()
        contents_correct = 'TEST_ENV' in data
        self.assertTrue(contents_correct)
