import time

import click
from virl2_client import NodeNotFound

from virl.api import VIRLServer
from virl.helpers import (get_cml_client, get_current_lab,
                          safe_join_existing_lab)


@click.command()
@click.option("--force/--no-force", "-f", default=False, required=False, help="Stop a node (if it's started) then wipe it (default: False)")
@click.option(
    "--confirm/--no-confirm",
    show_default=False,
    default=True,
    help="Do not prompt for confirmation (default: prompt)",
    required=False,
)
@click.argument("node", nargs=1)
def node(node, force, confirm):
    """
    wipe a node
    """
    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            try:
                node_obj = lab.get_node_by_label(node)
            except NodeNotFound:
                click.secho("Node {} was not found in lab {}".format(node, current_lab), fg="red")
                exit(1)

            if node_obj.is_active() and force:
                node_obj.stop()
                while node_obj.is_active():
                    time.sleep(1)

            if not node_obj.is_active():
                ret = "y"
                if confirm:
                    ret = input("Are you sure you want to wipe node {} [y/N]? ".format(node_obj.label))
                if ret.lower().startswith("y"):
                    node_obj.wipe(wait=True)
                    click.secho("Node {} wiped".format(node_obj.label))
                else:
                    click.secho("Not wiping node {}".format(node_obj.label))
            else:
                click.secho("Node {} is active; either stop it or use --force".format(node_obj.label), fg="red")
                exit(1)
        else:
            click.secho("Unable to find lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("No current lab set", fg="red")
        exit(1)
