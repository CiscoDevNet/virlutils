import click
from virl.cli.generate.ansible.commands import ansible, ansible1
from virl.cli.generate.pyats.commands import pyats, pyats1
from virl.cli.generate.nso.commands import nso, nso1

@click.group()
def generate():
    """
    unimplemented
    """
    pass

@click.group()
def generate1():
    """
    generate inv file for various tools
    """
    pass


generate1.add_command(ansible1)
generate1.add_command(pyats1)
generate1.add_command(nso1)
