from . import BaseTest
from click.testing import CliRunner
import requests_mock
from virl.cli.main import virl


class FlavorsTest(BaseTest):

    def get_flavors(self):
        response = {
            "flavors": [
                {
                    "OS-FLV-DISABLED:disabled": False,
                    "OS-FLV-EXT-DATA:ephemeral": 0,
                    "disk": 0,
                    "id": "7ca78ccd-4a59-4b0c-802e-2a82de05e7c9",
                    "name": "ASAv",
                    "os-flavor-access:is_public": True,
                    "ram": 2048,
                    "rxtx_factor": 1.0,
                    "swap": "",
                    "vcpus": 1
                },
                {
                    "OS-FLV-DISABLED:disabled": False,
                    "OS-FLV-EXT-DATA:ephemeral": 0,
                    "disk": 0,
                    "id": "99710bf7-b822-4240-9d5e-17bc03393675",
                    "name": "CSR1000v",
                    "os-flavor-access:is_public": True,
                    "ram": 3072,
                    "rxtx_factor": 1.0,
                    "swap": "",
                    "vcpus": 1
                },
                {
                    "OS-FLV-DISABLED:disabled": False,
                    "OS-FLV-EXT-DATA:ephemeral": 0,
                    "disk": 0,
                    "id": "a484b396-c0fd-4949-80fb-7a0ac4e15a2f",
                    "name": "IOS XRv",
                    "os-flavor-access:is_public": True,
                    "ram": 3072,
                    "rxtx_factor": 1.0,
                    "swap": "",
                    "vcpus": 1
                },
                {
                    "OS-FLV-DISABLED:disabled": False,
                    "OS-FLV-EXT-DATA:ephemeral": 0,
                    "disk": 0,
                    "id": "a484b396-c0fd-4949-80fb-7a0ac4efffff",
                    "name": "mockTest",
                    "os-flavor-access:is_public": True,
                    "ram": 2048,
                    "rxtx_factor": 1.0,
                    "swap": "",
                    "vcpus": 1
                },
                {
                    "OS-FLV-DISABLED:disabled": False,
                    "OS-FLV-EXT-DATA:ephemeral": 0,
                    "disk": 0,
                    "id": "a484b396-c0fd-4949-80fb-7a0ac4eeeeee",
                    "name": "mockTest2",
                    "os-flavor-access:is_public": True,
                    "ram": 4096,
                    "rxtx_factor": 1.0,
                    "swap": "",
                    "vcpus": 2
                }
            ]
        }

        return response

    def return_flavor(self, name=None):
        if name is None:
            raise IndexError("No such index {}".format(name))

        r = self.get_flavors()
        if name == 'mockTest':
            return {"flavor": r['flavors'][3]}

        if name == 'mockTest2':
            return {"flavor": r['flavors'][4]}

    def test_virl_flavors_00_ls(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:80/rest/flavors',
                  json=self.get_flavors())

            runner = CliRunner()
            result = runner.invoke(virl, ["flavors", "ls"])
            self.assertEqual(0, result.exit_code)

    def test_virl_flavors_01_add(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.post('http://localhost:80/rest/flavors',
                   json=self.return_flavor('mockTest'))

            runner = CliRunner()
            result = runner.invoke(virl, ["flavors", "add", "mockTest"])
            self.assertEqual(0, result.exit_code)

            args = [
                "flavors", "add", "mockTest2",
                "--vcpus", "2",
                "--memory", "4096"
            ]
            result = runner.invoke(virl, args)
            self.assertEqual(0, result.exit_code)

    def test_virl_flavors_02_update(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:80/rest/flavors',
                  json=self.get_flavors())
            m.post('http://localhost:80/rest/flavors',
                   json=self.return_flavor('mockTest'))

            u = 'http://localhost:80/rest/flavors/{}'
            u = u.format('a484b396-c0fd-4949-80fb-7a0ac4efffff')
            m.get(u, json=self.return_flavor('mockTest'))
            m.delete(u, json=self.return_flavor('mockTest'))

            runner = CliRunner()
            args = [
                "flavors", "update", "mockTest",
                "--vcpus", "2",
            ]
            result = runner.invoke(virl, args)
            self.assertEqual(0, result.exit_code)

    def test_virl_flavors_03_delete(self):
        with requests_mock.mock() as m:
            # Mock the request to return what we expect from the API.
            m.get('http://localhost:80/rest/flavors',
                  json=self.get_flavors())

            u = 'http://localhost:80/rest/flavors/{}'
            u = u.format('a484b396-c0fd-4949-80fb-7a0ac4efffff')
            m.delete(u, json=self.return_flavor('mockTest'))

            u = 'http://localhost:80/rest/flavors/{}'
            u = u.format('a484b396-c0fd-4949-80fb-7a0ac4eeeeee')
            m.delete(u, json=self.return_flavor('mockTest2'))

            runner = CliRunner()
            result = runner.invoke(virl, ["flavors", "delete", "mockTest"])
            self.assertEqual(0, result.exit_code)

            result = runner.invoke(virl, ["flavors", "delete", "mockTest2"])
            self.assertEqual(0, result.exit_code)
