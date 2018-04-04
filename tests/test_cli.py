import os
import unittest
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl


class VirlCLITest(unittest.TestCase):

    def setUp(self):
        # Only doing this because we don't have a better way of controlling
        # injection of VIRL_HOST
        os.environ['VIRL_HOST'] = 'localhost'

    def test_virl_help(self):
        runner = CliRunner()
        result = runner.invoke(virl, ["--help"])
        self.assertEqual(0, result.exit_code)
        for command in ["console", "generate", "down", "nodes", "logs",
                        "ls", "pull", "search", "ssh", "start", "stop",
                        "telnet", "up", "use"]:
            self.assertIn(command, result.output)

    def test_virl_ls(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/simengine/rest/list', json={
                'simulations': {
                    'virl_cli_default_1dNVCr': {
                        'status': 'ACTIVE',
                        'expires': None,
                        'launched': '2017-12-08T23:39:07.721310',
                    },
                    'topology-fpyHFs': {
                        'status': 'ACTIVE',
                        'expires': None,
                        'launched': '2017-12-08T18:48:34.174486',
                    },
                }
            })
            runner = CliRunner()
            result = runner.invoke(virl, ["ls"])
            print(result.output)
            self.assertEqual(0, result.exit_code)
