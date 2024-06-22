import platform
from subprocess import call

import click
from virl2_client.exceptions import NodeNotFound

from virl import helpers
from virl.api import NoPluginError, ViewerPlugin, VIRLServer
from virl.cli.views.console import console_table
from virl.helpers import (get_cml_client, get_current_lab,
                          safe_join_existing_lab)


@click.command()
@click.argument("node", nargs=1)
@click.option("--display/--none", default="False", help="Display Console information")
def console(node, display, **kwargs):
    """
    console for node
    """
    server = VIRLServer()
    client = get_cml_client(server)
    skip_types = ["external_connector", "unmanaged_switch"]

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            try:
                node_obj = lab.get_node_by_label(node)
            except NodeNotFound:
                click.secho("Node {} was not found in lab {}".format(node, current_lab), fg="red")
                exit(1)

            if node_obj.node_definition not in skip_types:
                if node_obj.is_active():
                    if len(lab.id) == 6:
                        # Old-style (CML 2.2) lab IDs; console uses lab_id/node_id
                        console = "/{}/{}/0".format(lab.id, node_obj.id)
                    else:
                        # From CML 2.3, console uses lab_title/node_label
                        console = "/{}/{}/0".format(lab.title, node_obj.label)
                    if display:
                        try:
                            pl = ViewerPlugin(viewer="console")
                            pl.visualize(consoles=[{"node": node, "console": console}])
                        except NoPluginError:
                            console_table([{"node": node, "console": console}])
                    else:
                        # use user specified ssh command
                        if "CML_CONSOLE_COMMAND" in server.config:
                            cmd = server.config["CML_CONSOLE_COMMAND"]
                            cmd = cmd.format(host=server.host, user=server.user, console="open " + console)
                            print("Calling user specified command: {}".format(cmd))
                            exit(call(cmd.split()))

                        # someone still uses windows
                        elif platform.system() == "Windows":
                            with helpers.disable_file_system_redirection():
                                cmd = "ssh -t {}@{} open {}".format(server.user, server.host, console)
                                exit(call(cmd.split()))

                        # why is shit so complicated?
                        else:
                            cmd = "ssh -t {}@{} open {}".format(server.user, server.host, console)
                            exit(call(cmd.split()))
                else:
                    click.secho("Node {} is not active".format(node), fg="red")
                    exit(1)
            else:
                click.secho("Node type {} does not support console connectivity".format(node_obj.node_definition), fg="yellow")
        else:
            click.secho("Unable to find lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("No current lab set", fg="red")
        exit(1)
