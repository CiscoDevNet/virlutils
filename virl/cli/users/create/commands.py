import getpass
import sys

import click

from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.option("--admin/--no-admin", is_flag=True, default=False, help="Grant or revoke admin privileges for the users")
@click.option("--group", default=[], multiple=True, help="Assign the users to one or more groups (e.g., --group group1 --group group2)")
@click.argument("usernames", nargs=-1, required=True)
def create_users(usernames, admin, group):
    """
    Create one or more users (e.g., user1 user2)
    """

    server = VIRLServer()
    client = get_cml_client(server)
    group_ids = [client.group_management.group_id(g) for g in group]

    for username in usernames:
        kwargs = {
            "username": username,
            "admin": admin,
            "groups": group_ids,
        }
        try:
            passwd = confirm_password(username)
            kwargs["pwd"] = passwd
            client.user_management.create_user(**kwargs)
            click.secho(f"User {username} successfully created", fg="green")
        except Exception as e:
            click.secho(f"Failed to create user: {e}", fg="red")
            sys.exit(1)


def confirm_password(username):
    """
    Prompts the user for a password and confirms it
    """
    passwd = getpass.getpass(f"Enter {username}'s password: ")
    re_entered_passwd = getpass.getpass(f"Re-Enter {username}'s password: ")
    if passwd != re_entered_passwd:
        click.secho("Passwords do not match", fg="red")
        sys.exit(1)
    return passwd
