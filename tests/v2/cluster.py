from . import BaseCMLTest
from .mocks.github import MockGitHub  # noqa
from click.testing import CliRunner
import requests_mock

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # noqa


class TestCMLCluster(BaseCMLTest):
    def setup_mocks(self, m):
        super().setup_mocks(m)
        m.get(self.get_api_path("system_health"), json=TestCMLCluster.get_system_health)

    @staticmethod
    def get_system_health(req, ctx):
        response = {
            "valid": True,
            "computes": {
                "17e91b4e-865a-4627-a6bb-50e3dfa988ab": {
                    "kvm_vmx_enabled": True,
                    "enough_cpus": True,
                    "refplat_images_available": True,
                    "lld_connected": True,
                    "valid": True,
                    "is_controller": True,
                    "hostname": "cml-controller",
                }
            },
            "is_licensed": True,
            "is_enterprise": True,
        }
        return response

    def test_cml_cluster_info(self):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["cluster", "info"])
            self.assertEqual(0, result.exit_code)
            self.assertIn("17e91b4e-865a-4627-a6bb-50e3dfa988ab", result.output)
