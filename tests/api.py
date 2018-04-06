from . import BaseTest
from virl.api import VIRLServer


class Tests(BaseTest):

    def test_create_virl_server(self):
        server = VIRLServer()
        self.assertIsInstance(server, VIRLServer)

    def test_user(self):
        server = VIRLServer()
        server.user = 'foo'
        self.assertEqual(server.user, 'foo')

    def test_host(self):
        server = VIRLServer()
        server.host = 'notreal'
        self.assertEqual(server.host, 'notreal')

    def test_paaswd(self):
        server = VIRLServer()
        server.passwd = 'notreal'
        self.assertEqual(server.passwd, 'notreal')
