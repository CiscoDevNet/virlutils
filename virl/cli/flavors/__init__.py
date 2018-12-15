import click
from virl.cli.flavors.ls.commands import ls
from virl.cli.flavors.add.commands import add
from virl.cli.flavors.delete.commands import delete
from virl.cli.flavors.update.commands import update


@click.group()
def flavors():
    """
    Manage VIRL Flavors Attributes
    """
    pass


flavors.add_command(ls)
flavors.add_command(add)
flavors.add_command(delete)
flavors.add_command(update)
