import click

from virl.api import NoPluginError, ViewerPlugin, VIRLServer
from virl.cli.views import cluster_list_table
from virl.helpers import get_cml_client


@click.command()
def info():
    """
    display cluster configuration details
    """

    server = VIRLServer()
    client = get_cml_client(server)
    pl = None

    system_health = None
    try:
        system_health = client.get_system_health()
    except Exception as e:
        click.secho(f"Failed to get system health data: {e}", fg="red")
        exit(1)

    try:
        pl = ViewerPlugin(viewer="cluster")
    except NoPluginError:
        pass

    if pl:
        pl.visualize(computes=system_health["computes"])
    else:
        cluster_list_table(system_health["computes"])
