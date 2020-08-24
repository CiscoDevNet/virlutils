from . import BaseTest
from .mocks.github import MockGitHub # noqa
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl
import os
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch # noqa


class Tests(BaseTest):

    def setUp(self):
        os.environ['VIRL_HOST'] = 'localhost'
        os.environ['VIRL_USERNAME'] = 'guest'
        os.environ['VIRL_PASSWORD'] = 'guest'

        try:
            os.remove('.virl/default/id')
            os.system('cp tests/v1/static/fake_repo_topology.virl topology.virl')

        except OSError:
            pass

    def test_01_virl_up(self):

        try:
            os.remove('.virl/default/id')
        except OSError:
            pass

        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            up_url = 'http://localhost:19399/simengine/rest/launch'
            m.post(up_url, json=self.mock_up_response())
            net_url = 'http://localhost:19399/openstack/rest/networks'
            m.get(net_url, json=self.mock_os_net_response())
            runner = CliRunner()
            result = runner.invoke(virl, ["up"])
            self.assertEqual(0, result.exit_code)

    @patch("virl.cli.up.commands.call", auto_spec=False)
    def test_02_virl_up_from_repo(self, call_mock):

        try:
            os.remove('.virl/default/id')
            os.remove('topology.virl')
        except OSError:
            pass

        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            up_url = 'http://localhost:19399/simengine/rest/launch'
            m.post(up_url, json=self.mock_up_response())
            net_url = 'http://localhost:19399/openstack/rest/networks'
            m.get(net_url, json=self.mock_os_net_response())
            topo_url = 'https://raw.githubusercontent.com/'
            topo_url += 'foo/bar/master/topology.virl'
            m.get(topo_url, json=MockGitHub.get_topology())
            runner = CliRunner()
            runner.invoke(virl, ["up", "foo/bar"])

    def mock_up_response(self):
        response = u'TEST_ENV'
        return response

    def mock_os_net_response(self):
        response = [
            {u'Description': u'L3 SNAT External',
             u'ID': u'e565b39a-ee48-4d35-b22f-15ca13cca40d',
             u'DNS': [u'8.8.8.8', u'171.70.168.183'],
             u'CIDR': u'10.10.241.208/28',
             u'Gateway': u'10.10.241.209',
             u'Network Name': u'ext-net'},
            {u'Description': u'L2 FLAT',
             u'ID': u'426a32c0-4964-4288-ba74-7db1f1f0b848',
             u'DNS': [u'8.8.8.8', u'171.70.168.183'],
             u'CIDR': u'10.10.241.224/27',
             u'Gateway': u'10.10.241.225',
             u'Network Name': u'flat'},
            {u'Description': u'L2 FLAT',
             u'ID': u'bfa4c58b-e404-45af-905d-b50aa603df20',
             u'DNS': [u'8.8.8.8', u'171.70.168.183'],
             u'CIDR': u'172.16.1.192/27',
             u'Gateway': u'172.16.1.193',
             u'Network Name': u'flat1'}
        ]
        return response
