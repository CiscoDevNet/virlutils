from . import BaseTest
from .mocks.api import MockVIRLServer
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl


class IdTest(BaseTest):

    def test_virl_id_nosim(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:19399/simengine/rest/list',
                  json=MockVIRLServer.list_simulations())
            runner = CliRunner()
            result = runner.invoke(virl, ["id"])
            self.assertEqual("virlutils-id\n", result.output)
