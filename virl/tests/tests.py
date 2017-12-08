import click
from click.testing import CliRunner

from virl.cli.main import virl


def test_virl_help():
    runner = CliRunner()
    result = runner.invoke(virl, ["--help"])
    print result.output
    assert result.exit_code == 0
    commands = ['console','logs']
    assert all(x in result.output for x in commands) == True

def test_virl_ls():
    runner = CliRunner()
    result = runner.invoke(virl, ["ls"])
    print result.output
    assert result.exit_code == 0


if __name__ == '__main__':
    test_virl_help()
    test_virl_ls()
