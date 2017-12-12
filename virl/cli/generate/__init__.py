import click
from virl.cli.generate.ansible.commands import ansible
from virl.cli.generate.pyats.commands import pyats


@click.group()
def generate():
    """
    generate inv file for various tools
    """
    pass

generate.add_command(ansible)
generate.add_command(pyats)
