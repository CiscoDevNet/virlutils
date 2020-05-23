import click
from virl.cli.definitions.images.ls.commands import ls
from virl.cli.definitions.images.iimport import iimport
from virl.cli.definitions.images.export.commands import export


@click.group()
def images():
    """
    manage image definitions
    """
    pass


images.add_command(ls)
images.add_command(export)
images.add_command(iimport, name="import")
