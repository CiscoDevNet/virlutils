from . import BaseCMLTest
from click.testing import CliRunner
import requests_mock


class CMLIdTest(BaseCMLTest):
    def test_cml_id(self):
        virl = self.get_virl()
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_basic_mocks(m)
            runner = CliRunner()
            result = runner.invoke(virl, ["id"])
            self.assertEqual("Mock Test (ID: 5f0d96)\n", result.output)
