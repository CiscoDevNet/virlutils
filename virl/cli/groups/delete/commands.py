import sys

import click

from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.argument("groupnames", nargs=-1, required=True)
def delete_groups(groupnames):
    """
    Delete one or more groups (e.g., group1 group2)
    """

    server = VIRLServer()
    client = get_cml_client(server)
    group_mapping = {g["name"]: g["id"] for g in client.group_management.groups()}

    for groupname in groupnames:
        try:
            group_id = group_mapping[groupname]
            client.group_management.delete_group(group_id)
            click.secho(f"Group {groupname} successfully deleted", fg="green")
        except KeyError:
            click.secho(f"Group {groupname} not found", fg="red")
            sys.exit(1)
        except Exception as e:
            click.secho(f"Failed to delete group: {e}", fg="red")
            sys.exit(1)
