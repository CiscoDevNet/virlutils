import click

from virl.cli.wipe.lab.commands import lab as labc
from virl.cli.wipe.node.commands import node as nodec


@click.group()
def wipe():
    """
    wipe a lab or nodes within a lab
    """
    pass


wipe.add_command(labc, name="lab")
wipe.add_command(nodec, name="node")
