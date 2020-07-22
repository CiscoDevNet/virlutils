import click
from virl.cli.definitions.nodes.ls.commands import ls
from virl.cli.definitions.nodes.nimport.commands import nimport
from virl.cli.definitions.nodes.export.commands import export


@click.group()
def nodes():
    """
    manage node definitions
    """
    pass


nodes.add_command(ls)
nodes.add_command(export)
nodes.add_command(nimport, name="import")
