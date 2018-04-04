import os
from . import BaseTest
from click.testing import CliRunner
from virl.cli.main import virl


class SearchTests(BaseTest):

    def test_virl_search(self):
        runner = CliRunner()
        result = runner.invoke(virl, ["search"])
        print(result.output)
        self.assertEqual(0, result.exit_code)

    def test_virl_search_with_query_name(self):
        runner = CliRunner()
        result = runner.invoke(virl, ["search", "ios"])
        print(result.output)
        self.assertEqual(0, result.exit_code)

    def test_virl_search_with_query_descr(self):
        runner = CliRunner()
        result = runner.invoke(virl, ["search", "hello"])
        print(result.output)
        self.assertEqual(0, result.exit_code)
