import click
from virl.cli.generate.ansible.commands import ansible
from virl.cli.generate.pyats.commands import pyats
from virl.cli.generate.nso.commands import nso


@click.group()
def generate():
    """
    generate inv file for various tools
    """
    pass


generate.add_command(ansible)
generate.add_command(pyats)
generate.add_command(nso)
