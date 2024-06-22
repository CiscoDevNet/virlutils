import click

from virl.api import NoPluginError, ViewerPlugin, VIRLServer
from virl.cli.views import user_list_table
from virl.helpers import get_cml_client


@click.command()
@click.option("-v", "--verbose", is_flag=True, help="Include user IDs in the output")
def list_users(verbose):
    """
    List all users on the server
    """
    server = VIRLServer()
    client = get_cml_client(server)

    users = client.user_management.users()

    labs_mapping = {lab.id: lab.title for lab in client.all_labs()}
    group_mapping = {g["id"]: g["name"] for g in client.group_management.groups()}

    for user in users:
        user["groups"] = "\n".join(group_mapping[group_id] for group_id in user["groups"])
        user["labs"] = "\n".join(str(labs_mapping[lab_id]) for lab_id in user["labs"])

    try:
        pl = ViewerPlugin(viewer="user")
        pl.visualize(users=users)
    except NoPluginError:
        user_list_table(users, verbose)
