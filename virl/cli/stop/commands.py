import click
from virl.api import VIRLServer
from virl2_client.exceptions import NodeNotFound
from virl.helpers import get_cml_client, safe_join_existing_lab, get_current_lab


@click.command()
@click.argument("node", nargs=1)
def stop(node):
    """
    stop a node
    """
    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            try:
                node_obj = lab.get_node_by_label(node)

                if node_obj.is_active():
                    node_obj.stop(wait=True)
                    click.secho("Stopped node {}".format(node_obj.label))
                else:
                    click.secho("Node {} is already stopped".format(node_obj.label), fg="yellow")
            except NodeNotFound:
                click.secho("Node {} was not found in lab {}".format(node, current_lab), fg="red")
                exit(1)
        else:
            click.secho("Unable to find lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("No current lab set", fg="red")
        exit(1)
