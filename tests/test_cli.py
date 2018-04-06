from . import BaseTest
from click.testing import CliRunner
from virl.cli.main import virl


class TestHelp(BaseTest):

    def test_virl_help(self):
        runner = CliRunner()
        result = runner.invoke(virl, ["--help"])
        self.assertEqual(0, result.exit_code)
        for command in ["console", "generate", "down", "nodes", "logs",
                        "ls", "pull", "search", "ssh", "start", "stop",
                        "telnet", "up", "use"]:
            self.assertIn(command, result.output)
