import click
from click.testing import CliRunner
print('boo')
from virl.cli.main import virl

def test_virl():
    print('foo')
    runner = CliRunner()
    result = runner.invoke(virl, ['--help'])
    print result
    assert result.exit_code == 0
    assert 'Debug mode is on' in result.output
    assert 'Syncing' in result.output
