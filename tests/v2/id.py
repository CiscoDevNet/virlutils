from . import BaseCMLTest
from click.testing import CliRunner
import requests_mock


class CMLIdTest(BaseCMLTest):
    def test_cml_id(self):
        virl = self.get_virl()
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            runner = CliRunner()
            result = runner.invoke(virl, ["id"])
            self.assertEqual("{} (ID: {})\n".format(self.get_test_title(), self.get_test_id()), result.output)
