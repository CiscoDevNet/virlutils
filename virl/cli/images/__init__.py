import click
from virl.cli.images.ls.commands import ls
from virl.cli.images.add.commands import add
from virl.cli.images.delete.commands import delete
from virl.cli.images.update.commands import update

@click.group()
def images():
    """
    Manage VIRL Flavors Attributes
    """
    pass


images.add_command(ls)
images.add_command(add)
images.add_command(delete)
images.add_command(update)
