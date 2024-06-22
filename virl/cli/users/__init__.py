import click

from virl.cli.users.create.commands import create_users
from virl.cli.users.delete.commands import delete_users
from virl.cli.users.ls.commands import list_users
from virl.cli.users.update.commands import update_users


@click.group()
def users():
    """
    manage users
    """
    pass


users.add_command(list_users, name="ls")
users.add_command(create_users, name="create")
users.add_command(update_users, name="update")
users.add_command(delete_users, name="delete")
