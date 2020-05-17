import click
from virl.cli.definitions.ls.commands import ls
from virl.cli.definitions.add.commands import add
from virl.cli.definitions.delete.commands import delete
from virl.cli.definitions.update.commands import update


@click.group()
def definitions():
    """
    unimplemented
    """
    pass


definitions.add_command(ls)
definitions.add_command(add)
definitions.add_command(delete)
definitions.add_command(update)
