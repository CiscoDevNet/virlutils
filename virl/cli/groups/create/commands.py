import sys

import click

from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.option("--member", help="Assign one or more users to the groups (e.g., --member user1 --member user2)", multiple=True)
@click.option("--add-all-users", help="Assign all users to the groups", is_flag=True)
@click.option(
    "--lab",
    type=(str, click.Choice(["read_only", "read_write"])),
    help="Labs to assign the groups (e.g, --labs lab_id1 read_only --labs lab_id2 read_write)",
    default=[],
    multiple=True,
    metavar="lab_id [read_only|read_write]",
)
@click.option(
    "--add-all-labs",
    type=click.Choice(["read_only", "read_write"]),
    help="Assign all labs to the groups with either read_only or read_write permissions",
)
@click.argument("groupnames", nargs=-1, required=True)
def create_groups(groupnames, member, add_all_users, lab, add_all_labs):
    """
    Create one or more groups (e.g., group1 group2)
    """

    server = VIRLServer()
    client = get_cml_client(server)

    all_users = client.user_management.users()
    all_users_ids = [u["id"] for u in all_users]
    members_ids = all_users_ids if add_all_users else [u["id"] for u in all_users if u["username"] in member]

    lab_ids = [{"id": lab_id, "permission": permission} for lab_id, permission in lab]
    lab_ids = None if add_all_labs is None else [{"id": lid, "permission": add_all_labs} for lid in client.get_lab_list()]

    for name in groupnames:
        kwargs = {
            "name": name,
            "members": members_ids,
            "labs": lab_ids,
        }
        try:
            client.group_management.create_group(**kwargs)
            click.secho(f"Group {name} successfully created", fg="green")
        except Exception as e:
            click.secho(f"Failed to create group: {e}", fg="red")
            sys.exit(1)
