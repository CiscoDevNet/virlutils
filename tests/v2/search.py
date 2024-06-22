import requests_mock
from click.testing import CliRunner

from . import BaseCMLTest


class SearchTests(BaseCMLTest):
    @requests_mock.mock()
    def test_virl_search(self, m):
        m.get("https://api.github.com/orgs/virlfiles/repos", json=self.mock_response())
        virl = self.get_virl()
        runner = CliRunner()
        result = runner.invoke(virl, ["search"])
        self.assertEqual(0, result.exit_code)

    @requests_mock.mock()
    def test_virl_search_with_query_name(self, m):
        m.get("https://api.github.com/orgs/virlfiles/repos", json=self.mock_response())
        virl = self.get_virl()
        runner = CliRunner()
        result = runner.invoke(virl, ["search", "ios"])
        self.assertEqual(0, result.exit_code)

    @requests_mock.mock()
    def test_virl_search_with_query_descr(self, m):
        # Mock the request to return what we expect from the API.
        m.get("https://api.github.com/orgs/virlfiles/repos", json=self.mock_response())
        virl = self.get_virl()
        runner = CliRunner()
        result = runner.invoke(virl, ["search", "hello"])
        self.assertEqual(0, result.exit_code)

    def mock_response(self):
        response = [
            {"name": "2-ios-router", "full_name": "virlfiles/2-ios-router", "description": "hello world virlfile", "stargazers_count": 344}
        ]
        return response
