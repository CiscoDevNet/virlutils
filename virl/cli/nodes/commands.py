import click

from virl.api import NoPluginError, ViewerPlugin, VIRLServer
from virl.cli.views import node_list_table
from virl.helpers import (get_cml_client, get_current_lab,
                          safe_join_existing_lab)


@click.command()
def nodes():
    """
    get node list for the current lab
    """
    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            # Force an operational sync.
            try:
                lab.sync_operational_if_outdated()
            except Exception:
                pass

            computes = {}
            try:
                computes = client.get_system_health()["computes"]
            except Exception:
                pass

            try:
                pl = ViewerPlugin(viewer="node")
                pl.visualize(nodes=lab.nodes(), computes=computes)
            except NoPluginError:
                node_list_table(lab.nodes(), computes)
        else:
            click.secho("Lab {} is not running".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("No current lab selected", fg="red")
        exit(1)
