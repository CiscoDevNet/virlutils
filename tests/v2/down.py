from . import BaseCMLTest
from click.testing import CliRunner
import requests_mock
import os


class CMLTestDown(BaseCMLTest):
    def setup_mocks(self, m):
        super().setup_mocks(m)
        m.put(self.get_api_path("labs/{}/stop".format(self.get_test_id())), json="STOPPED")
        m.get(self.get_api_path("labs/{}/check_if_converged".format(self.get_test_id())), json=True)

    def test_cml_down(self):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["down"])
            self.assertEqual(0, result.exit_code)

    def test_cml_down_by_name(self):

        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["down", "--lab-name", self.get_test_title()])
            self.assertEqual(0, result.exit_code)

    def test_cml_down_by_id(self):

        try:
            os.remove(".virl/current_cml_lab")
        except OSError:
            pass

        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["down", "--id", self.get_test_id()])
            self.assertEqual(0, result.exit_code)
