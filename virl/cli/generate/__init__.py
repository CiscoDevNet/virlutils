import click
from virl.cli.generate.ansible.commands import ansible, ansible1
from virl.cli.generate.pyats.commands import pyats, pyats1
from virl.cli.generate.nso.commands import nso, nso1


@click.group()
def generate():
    """
    generate inv file for various tools
    """
    pass


@click.group()
def generate1():
    """
    generate inv file for various tools
    """
    pass


generate1.add_command(ansible1, name="ansible")
generate1.add_command(pyats1, name="pyats")
generate1.add_command(nso1, name="nso")

generate.add_command(ansible)
generate.add_command(pyats)
generate.add_command(nso)
