from . import BaseTest
from click.testing import CliRunner
from virl.cli.main import virl
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class Tests(BaseTest):

    @patch("virl.cli.uwm.commands.subprocess.Popen", auto_spec=False)
    def test_virl_uwm(self, call_mock):
        runner = CliRunner()
        runner.invoke(virl, ["uwm"])
        url = 'http://guest:guest@localhost/simulation/guest/TEST_ENV'
        call_mock.assert_called_with(['open', url])
