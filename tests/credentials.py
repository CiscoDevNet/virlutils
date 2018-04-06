import os
from . import BaseTest
from virl.api import VIRLServer
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class Tests(BaseTest):

    def setUp(self):
        del os.environ['VIRL_HOST']
        del os.environ['VIRL_USERNAME']
        del os.environ['VIRL_PASSWORD']

        try:
            os.remove('.virl/default/id')
        except OSError:
            pass

    @patch('virl.api.credentials.get_prop', return_value='fake')
    def test_create_virl_server(self, mock_prop):
        server = VIRLServer()
        self.assertIsInstance(server, VIRLServer)
    #
    # def test_user(self):
    #     server = VIRLServer()
    #     server.user = 'foo'
    #     self.assertEqual(server.user, 'foo')
    #
    # def test_host(self):
    #     server = VIRLServer()
    #     server.host = 'notreal'
    #     self.assertEqual(server.host, 'notreal')
    #
    # def test_paaswd(self):
    #     server = VIRLServer()
    #     server.passwd = 'notreal'
    #     self.assertEqual(server.passwd, 'notreal')
