from . import BaseTest
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class Test(BaseTest):

    def test_virl_logs(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/simengine/rest/events/TEST_ENV',
                  json=self.mock_request())
            runner = CliRunner()
            result = runner.invoke(virl, ["logs"])
            self.assertEqual(0, result.exit_code)

    @patch('virl.helpers.check_sim_running', return_value=False)
    def test_virl_logs_not_running(self, mock):

        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/simengine/rest/events/TEST_ENV',
                  json=self.mock_request())
            runner = CliRunner()
            result = runner.invoke(virl, ["logs"])
            self.assertEqual(0, result.exit_code)

    def mock_request(self):
        response = {
            u'events': [
                {
                    u'name': u'unspecified',
                    u'level': u'INFO',
                    u'session': u'virlutils_default_WPJ4ES',
                    u'user': u'guest',
                    u'time': u'Apr/04/201814:25:13',
                    u'message': u'some message',
                    u'id': 1457
                }
            ]
        }
        return response
