import os
from . import BaseTest
from click.testing import CliRunner
from virl.cli.main import virl
from virl.swagger.app import app

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class Tests(BaseTest):

    @patch("virl.cli.swagger.commands.subprocess.Popen", auto_spec=False)
    def test_virl_swagger_start(self, call_mock):
        runner = CliRunner()
        runner.invoke(virl, ["swagger", "start"])
        url = 'http://localhost:5000'
        call_mock.assert_called_with(['open', url])

    def test_virl_swagger_status(self):
        with open('/tmp/virl_swagger.port', 'w') as fh:
            fh.write('1234')
        with open('/tmp/virl_swagger.pid', 'w') as fh:
            fh.write('1234')
        runner = CliRunner()
        result = runner.invoke(virl, ["swagger", "status"])
        expected_output = 'VIRL swagger UI is running at http://localhost:1234'
        self.assertIn(expected_output, result.output)

    @patch("virl.cli.swagger.commands.subprocess.Popen", auto_spec=False)
    def test_virl_swagger_stop(self, call_mock):
        runner = CliRunner()
        result = runner.invoke(virl, ["swagger", "stop"])
        print(result.output)
        call_mock.assert_called_with('kill $(cat /tmp/virl_swagger.pid)',
                                     shell=True)


class SwaggerFlaskApp(BaseTest):
    def setUp(self):
        os.environ['VIRL_SWAGGER_HOST'] = 'localhost'
        os.environ['VIRL_SWAGGER_USERNAME'] = 'guest'
        os.environ['VIRL_SWAGGER_PASSWORD'] = 'guest'
        os.environ['VIRL_SWAGGER_PORT'] = '1234'
        self.app = app
        app.testing = True
        self.app = app.test_client()

    def test_swagger_ui(self):
        resp = self.app.get('/')
        expected_data = b'ui.preauthorizeBasic("basicAuth", "guest", "guest")'
        self.assertEqual(resp.status_code, 200)
        self.assertIn(expected_data, resp.data)

    def test_swagger_spec(self):
        resp = self.app.get('/swagger.json')
        expected_data = b'"host": "localhost:1234",'
        self.assertEqual(resp.status_code, 200)
        self.assertIn(expected_data, resp.data)

    def tearDown(self):
        pass
        # os.close(self.db_fd)
        # os.unlink(flaskr.app.config['DATABASE'])
