from . import BaseCMLTest
from click.testing import CliRunner
import requests_mock
import os


class CMLDefinitionsTest(BaseCMLTest):
    def test_cml_image_definitions_import(self):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            m.post(self.get_api_path("image_definitions/"), json=True)  # virl2_client 2.2.1 uses URI that ends in slashes
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(
                virl,
                [
                    "definitions",
                    "images",
                    "import",
                    "definition",
                    "-f",
                    os.path.join(os.path.dirname(__file__), "static/fake_image_definitions.yaml"),
                ],
            )
            self.assertEqual(0, result.exit_code, result.stdout)
