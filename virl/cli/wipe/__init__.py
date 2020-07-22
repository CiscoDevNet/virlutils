import click
from virl.cli.wipe.node.commands import node
from virl.cli.wipe.lab.commands import lab


@click.group()
def wipe():
    """
    wipe a lab or nodes within a lab
    """
    pass


wipe.add_command(lab)
wipe.add_command(node)
