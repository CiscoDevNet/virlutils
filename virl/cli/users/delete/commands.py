import sys

import click

from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.argument("usernames", nargs=-1, required=True)
def delete_users(usernames):
    """
    Delete one or more users (e.g., user1 user2)
    """

    server = VIRLServer()
    client = get_cml_client(server)
    user_mapping = {u["username"]: u["id"] for u in client.user_management.users()}

    for username in usernames:
        try:
            user_id = user_mapping[username]
            client.user_management.delete_user(user_id)
            click.secho(f"User {username} successfully deleted", fg="green")
        except Exception as e:
            click.secho(f"Failed to delete user: {e}", fg="red")
            sys.exit(1)
