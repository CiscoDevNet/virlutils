import click

from virl.api import NoPluginError, ViewerPlugin, VIRLServer
from virl.cli.views import group_list_table
from virl.helpers import get_cml_client


@click.command()
@click.option("-v", "--verbose", is_flag=True, help="Include user IDs in the output")
def list_groups(verbose):
    """
    List all groups on the server
    """
    server = VIRLServer()
    client = get_cml_client(server)
    user_mapping = {u["id"]: u["username"] for u in client.user_management.users()}
    labs_mapping = {lab.id: lab.title for lab in client.all_labs(show_all=True)}
    groups = client.group_management.groups()
    for group in groups:
        group["members"] = [user_mapping[uid] for uid in group["members"]]
        group["labs"] = [{"title": labs_mapping[lab["id"]], "permission": lab["permission"]} for lab in group["labs"]]
    try:
        pl = ViewerPlugin(viewer="group")
        pl.visualize(groups=groups)
    except NoPluginError:
        group_list_table(groups, verbose=verbose)
