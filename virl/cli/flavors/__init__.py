import click
from virl.cli.flavors.ls.commands import ls
from virl.cli.flavors.add.commands import add
from virl.cli.flavors.delete.commands import delete
from virl.cli.flavors.update.commands import update


@click.group()
def flavors1():
    """
    Manage VIRL Flavors Attributes
    """
    pass


flavors1.add_command(ls)
flavors1.add_command(add)
flavors1.add_command(delete)
flavors1.add_command(update)
