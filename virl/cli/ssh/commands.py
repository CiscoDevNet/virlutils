from subprocess import call

import click
from virl2_client.exceptions import NodeNotFound

from virl.api import VIRLServer
from virl.helpers import (get_cml_client, get_current_lab, get_node_mgmt_ip,
                          safe_join_existing_lab)


@click.command()
@click.argument("node", nargs=1)
def ssh(node):
    """
    ssh to a node
    """
    server = VIRLServer()
    client = get_cml_client(server)
    username = server.config.get("VIRL_SSH_USERNAME", "cisco")

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            try:
                node_obj = lab.get_node_by_label(node)
            except NodeNotFound:
                click.secho("Node {} was not found in lab {}".format(node, current_lab), fg="red")
                exit(1)

            if node_obj.is_active():
                mgmtip = get_node_mgmt_ip(node_obj)
                if mgmtip:
                    if "VIRL_SSH_COMMAND" in server.config:
                        cmd = server.config["VIRL_SSH_COMMAND"]
                        cmd = cmd.format(host=mgmtip, username=username)
                        print("Calling user specified command: {}".format(cmd))
                        exit(call(cmd.split()))
                    else:
                        click.secho("Attemping ssh connection to {} at {}".format(node_obj.label, mgmtip))

                        exit(call(["ssh", "{}@{}".format(username, mgmtip)]))
                else:
                    click.secho("Node {} does not have an external management IP".format(node_obj.label))
            else:
                click.secho("Node {} is not active".format(node_obj.label), fg="yellow")
        else:
            click.secho("Unable to find lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("No current lab set", fg="red")
        exit(1)
