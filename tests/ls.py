from . import BaseTest
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl


class LsTest(BaseTest):

    def test_virl_ls(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/simengine/rest/list', json={
                'simulations': {
                    'sim1': {
                        'status': 'ACTIVE',
                        'expires': None,
                        'launched': '2017-12-08T23:39:07.721310',
                    },
                    'sim2': {
                        'status': 'ACTIVE',
                        'expires': None,
                        'launched': '2017-12-08T18:48:34.174486',
                    },
                }
            })
            runner = CliRunner()
            result = runner.invoke(virl, ["ls", "--all"])
            print(result.output)
            self.assertEqual(0, result.exit_code)
