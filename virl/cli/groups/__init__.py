import click

from virl.cli.groups.create.commands import create_groups
from virl.cli.groups.delete.commands import delete_groups
from virl.cli.groups.ls.commands import list_groups
from virl.cli.groups.update.commands import update_groups


@click.group()
def groups():
    """
    manage groups
    """
    pass


groups.add_command(list_groups, name="ls")
groups.add_command(create_groups, name="create")
groups.add_command(update_groups, name="update")
groups.add_command(delete_groups, name="delete")
