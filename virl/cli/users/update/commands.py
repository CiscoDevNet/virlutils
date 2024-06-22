import getpass
import sys

import click

from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.option("--admin/--no-admin", is_flag=True, default=None, help="Grant or revoke admin privileges for the users")
@click.option(
    "--group",
    multiple=True,
    help="Assign the user to one or more groups (e.g., --group group1 --group group2)",
)
@click.option("--remove-from-all-groups", is_flag=True, help="Remove the users from all groups")
@click.option("--change-password", is_flag=True, help="Prompt to change the users' password")
@click.option("--all-users", is_flag=True, help="Apply the changes to all users")
@click.argument("usernames", nargs=-1, required=True)
def update_users(usernames, admin, group, remove_from_all_groups, change_password, all_users):
    """
    Update one or more users (e.g., user1 user2)
    """

    server = VIRLServer()
    client = get_cml_client(server)

    group = group if group else None
    group = [] if remove_from_all_groups else group
    group_ids = [g["id"] for g in client.group_management.groups() if g["name"] in group] if group else group

    users = client.user_management.users()
    user_mapping = {user["username"]: user["id"] for user in users}
    all_usernames = users if all_users else usernames

    for username in all_usernames:
        user_id = user_mapping[username]
        password_dict = get_password_dict(username) if change_password else None
        kwargs = {
            "user_id": user_id,
            "admin": admin,
            "groups": group_ids,
            "password_dict": password_dict,
        }
        # only pass kwargs that are not None
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        try:
            client.user_management.update_user(**kwargs)
            click.secho(f"User {username} successfully updated", fg="green")
        except Exception as e:
            click.secho(f"Failed to create user: {e}", fg="red")
            sys.exit(1)


def get_password_dict(username):
    """
    Prompt the user for old and new password and verify it
    A user with administrative privileges can set a new password by providing an arbitrary or empty old password
    """
    old_passwd = getpass.getpass(f"Enter {username}'s old password (password can be blank if you are an admin): ")
    new_passwd = getpass.getpass(f"Enter {username}'s new password: ")
    return {"old_password": old_passwd, "new_password": new_passwd}
