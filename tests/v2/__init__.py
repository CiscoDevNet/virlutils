import os
import unittest
from click.testing import CliRunner
from .mocks import MockCMLServer
import functools
import sys
import traceback
import pdb
import requests_mock


def setup_cml_environ():
    os.environ["VIRL_HOST"] = "localhost"
    os.environ["VIRL_USERNAME"] = "admin"
    os.environ["VIRL_PASSWORD"] = "admin"
    os.environ["CML2_PLUS"] = "true"
    os.environ["CML_VERIFY_CERT"] = "false"
    os.environ["NSO_HOST"] = "localhost"
    os.environ["NSO_USERNAME"] = "admin"
    os.environ["NSO_PASSWORD"] = "admin"


def debug_on(*exceptions):
    if not exceptions:
        exceptions = (AssertionError,)

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except exceptions:
                info = sys.exc_info()
                traceback.print_exception(*info)
                pdb.post_mortem(info[2])

        return wrapper

    return decorator


class BaseCMLTest(unittest.TestCase):
    def setUp(self):
        try:
            os.makedirs(".virl")
        except OSError:
            pass
        # Only doing this because we don't have a better way of controlling
        # injection of VIRL_HOST
        virl = self.get_virl()
        runner = CliRunner()
        with requests_mock.Mocker() as m:
            self.setup_mocks(m)
            runner.invoke(virl, ["use", self.get_test_title()])

    def get_virl(self):
        # This bit of hackery is done since coverage loads all modules into the same
        # namespace.  We need to reload our virl module to get this to recognize
        # the new environment.
        try:
            del sys.modules["virl.cli.main"]
        except KeyError:
            pass

        setup_cml_environ()
        from virl.cli.main import virl

        return virl

    def get_api_path(self, path):
        return "https://localhost/api/v0/{}".format(path)

    def get_test_id(self):
        return "5f0d96"

    def get_test_title(self):
        return "Mock Test"

    def get_alt_id(self):
        return "5eaea5"

    def get_alt_title(self):
        return "Other Lab"

    def setup_mocks(self, m):
        m.get(self.get_api_path("labs"), json=MockCMLServer.get_labs)
        m.get(self.get_api_path("populate_lab_tiles"), json=MockCMLServer.get_lab_tiles)
        m.get(self.get_api_path("labs/{}/download".format(self.get_test_id())), text=MockCMLServer.download_lab)
        m.get(
            self.get_api_path("labs/{}/topology?exclude_configurations=False".format(self.get_test_id())), json=MockCMLServer.get_topology
        )
        m.get(
            self.get_api_path("labs/{}/topology?exclude_configurations=False".format(self.get_alt_id())),
            json=MockCMLServer.get_alt_topology,
        )
        m.get(self.get_api_path("labs/{}/topology?exclude_configurations=True".format(self.get_test_id())), json=MockCMLServer.get_topology)
        m.get(
            self.get_api_path("labs/{}/topology?exclude_configurations=True".format(self.get_alt_id())),
            json=MockCMLServer.get_alt_topology,
        )
        m.get(self.get_api_path("labs/{}/download".format(self.get_alt_id())), text=MockCMLServer.download_alt_lab)
        m.get(self.get_api_path("labs/{}/lab_element_state".format(self.get_test_id())), json=MockCMLServer.get_lab_element_state)
        m.get(self.get_api_path("system_information"), json=MockCMLServer.get_sys_info)
        m.get(self.get_api_path("authok"), text=MockCMLServer.auth_ok)
        m.post(self.get_api_path("authenticate"), text=MockCMLServer.authenticate)
        m.get(self.get_api_path("labs/{}/state".format(self.get_test_id())), json="STARTED")
        m.get(self.get_api_path("labs/{}/state".format(self.get_alt_id())), json="STOPPED")
        m.get(self.get_api_path("labs/{}/check_if_converged".format(self.get_test_id())), json=True)

    def add_debug_mock(self, m):
        m.register_uri(requests_mock.ANY, requests_mock.ANY, text=MockCMLServer.print_req)
