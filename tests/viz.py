from . import BaseTest
from click.testing import CliRunner
from virl.cli.main import virl
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class Tests(BaseTest):

    @patch("virl.cli.viz.commands.subprocess.Popen", auto_spec=False)
    def test_virl_uwm(self, call_mock):
        runner = CliRunner()
        runner.invoke(virl, ["viz"])
        url = 'http://localhost:19402/?sim_id=TEST_ENV#/layer/phy'
        call_mock.assert_called_with(['open', url])
