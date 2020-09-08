import click
from virl.api import VIRLServer
from subprocess import call
from virl import helpers
from virl.helpers import get_cml_client, safe_join_existing_lab, get_current_lab, get_command
from virl2_client.exceptions import NodeNotFound


@click.command()
@click.argument("node", nargs=1)
def start(node):
    """
    start a node
    """
    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            try:
                node_obj = lab.get_node_by_label(node)

                if not node_obj.is_active():
                    node_obj.start(wait=True)
                    click.secho("Started node {}".format(node_obj.label))
                else:
                    click.secho("Node {} is already active".format(node_obj.label), fg="yellow")
            except NodeNotFound:
                click.secho("Node {} was not found in lab {}".format(node, current_lab), fg="red")
                exit(1)
        else:
            click.secho("Unable to find lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("No current lab set", fg="red")
        exit(1)


@click.command()
@click.argument("node", nargs=-1)
def start1(node):
    """
    start a node
    """
    if len(node) == 2:
        # we received env and node name
        env = node[0]
        running = helpers.check_sim_running(env)
        node = node[1]
    elif len(node) == 1:
        # assume default env
        env = "default"
        running = helpers.check_sim_running(env)
        node = node[0]
    else:
        exit(call([get_command(), "start", "--help"]))

    if running:
        sim_name = running
        server = VIRLServer()
        resp = server.start_node(sim_name, node)
        if resp.ok:
            click.secho("Started node {}".format(node))
        else:
            click.secho("Error starting Node {}: {}".format(node, resp), fg="red")
