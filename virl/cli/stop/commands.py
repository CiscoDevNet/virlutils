import click
from subprocess import call

from virl2_client.exceptions import NodeNotFound

from virl.api import VIRLServer
from virl.helpers import get_cml_client, get_current_lab, safe_join_existing_lab, get_command


@click.command()
@click.argument("node", required=False)
@click.option("--id", required=False, help="An existing node ID to stop (the node name argument is ignored)")
def stop(node, id):
    """
    stop a node
    """
    if not node and not id:
        exit(call([get_command(), "stop", "--help"]))

    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            try:
                if id:
                    node_obj = lab.get_node_by_id(id)
                else:
                    node_obj = lab.get_node_by_label(node)

                if node_obj.is_active():
                    node_obj.stop(wait=True)
                    click.secho("Stopped node {}".format(node_obj.label))
                else:
                    click.secho("Node {} is already stopped".format(node_obj.label), fg="yellow")
            except NodeNotFound:
                click.secho("Node {} was not found in lab {}".format(id if id else node, current_lab), fg="red")
                exit(1)
        else:
            click.secho("Unable to find lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("No current lab set", fg="red")
        exit(1)
