import os
from . import BaseTest
from virl.api import VIRLServer
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class Tests(BaseTest):

    def setUp(self):
        if 'VIRL_HOST' in os.environ:
            del os.environ['VIRL_HOST']
        if 'VIRL_USERNAME' in os.environ:
            del os.environ['VIRL_USERNAME']
        if 'VIRL_PASSWORD' in os.environ:
            del os.environ['VIRL_PASSWORD']

        try:
            os.remove('.virl/default/id')
        except OSError:
            pass

    @patch('virl.api.credentials.get_prop', return_value='fake')
    def test_create_virl_server(self, mock_prop):
        server = VIRLServer()
        self.assertIsInstance(server, VIRLServer)

    @patch('virl.api.credentials._get_from_user', return_value='userinput')
    @patch('virl.api.credentials._get_password', return_value='passwordinput')
    def test_prompt_user(self, user_input, password_input):
        server = VIRLServer()
        user = server.user
        self.assertEqual(user, 'userinput')
