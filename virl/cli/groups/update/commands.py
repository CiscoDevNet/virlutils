import sys

import click

from virl.api import VIRLServer
from virl.helpers import get_cml_client, get_group_associations, get_group_member_ids


@click.command()
@click.option("--member", help="Assign one or more users to the groups (e.g., --member user1 --member user2)", multiple=True)
@click.option("--add-all-users", help="Assign all users to the groups", is_flag=True)
@click.option(
    "--lab",
    type=(str, click.Choice(["read_only", "read_write"])),
    help="Labs to assign the groups",
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
def update_groups(groupnames, member, add_all_users, lab, add_all_labs):
    """
    Update one or more groups (e.g., group1 group2)
    """

    server = VIRLServer()
    client = get_cml_client(server)

    all_users = client.user_management.users()
    members_ids = get_group_member_ids(all_users, member, add_all_users)
    associations = get_group_associations(client, lab, add_all_labs)

    groups = client.group_management.groups()
    group_mapping = {group["name"]: group["id"] for group in groups}
    for name in groupnames:
        group_id = group_mapping[name]
        kwargs = {
            "group_id": group_id,
            "members": members_ids,
            "associations": associations,
        }
        try:
            client.group_management.update_group(**kwargs)
            click.secho(f"Group {name} successfully updated", fg="green")
        except Exception as e:
            click.secho(f"Failed to update group: {e}", fg="red")
            sys.exit(1)
