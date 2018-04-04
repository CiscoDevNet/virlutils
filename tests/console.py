from . import BaseTest
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl


class ConsoleTest(BaseTest):

    def mock_response(self):
        sim_response = {
            u'router2': u'10.94.241.194:17003',
            u'router1': u'10.94.241.194:17000'
        }
        return sim_response

    def test_virl_console(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/simengine/rest/serial_port/TEST_ENV',
                  json=self.mock_response())
            runner = CliRunner()
            result = runner.invoke(virl, ["console", "--display"])
            print(result.output)
            self.assertEqual(0, result.exit_code)
