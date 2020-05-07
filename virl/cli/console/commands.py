import click
from virl.api import VIRLServer
from subprocess import call
from virl import helpers
from virl.helpers import get_cml_client, get_current_lab, safe_join_existing_lab
from virl.cli.views.console import console_table, console_table1
import platform


@click.command()
@click.argument("node", nargs=1)
@click.option("--display/--none", default="False", help="Display Console information")
def console(node, display, **kwargs):
    """
    console for node (XXX: currently broken)
    """
    server = VIRLServer()
    client = get_cml_client(server)

    if not node:
        exit(call(["virl", "console", "--help"]))

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            node_obj = lab.get_node_by_label(node)

            if node_obj.is_active():
                console = "/{}/{}/0".format(lab.id, node_obj.id)
                if display:
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
                            cmd = "ssh {}@{} open {}".format(server.user, server.host, console)
                            exit(call(cmd.split()))

                    # why is shit so complicated?
                    else:
                        cmd = "ssh {}@{} open {}".format(server.user, server.host, console)
                        exit(call(cmd.split()))
            else:
                click.secho("Node {} is not active".format(node), fg="red")
        else:
            click.secho("Unable to find lab {}".format(current_lab), fg="red")
    else:
        click.secho("No current lab set", fg="red")


@click.command()
@click.argument("node", nargs=-1)
@click.option("--display/--none", default="False", help="Display Console information")
def console1(node, display, **kwargs):
    """
    console for node
    """
    server = VIRLServer()

    if len(node) == 2:
        # we received env and node name
        env = node[0]
        running = helpers.check_sim_running(env)
        node = node[1]
    elif display:
        # only displaying output
        env = "default"
        running = helpers.check_sim_running(env)
        node = None

    elif len(node) == 1:
        # assume default env
        env = "default"
        running = helpers.check_sim_running(env)
        node = node[0]
    else:
        # node was not specified, display usage
        exit(call(["virl", "console", "--help"]))

    if running:

        sim_name = running

        resp = server.get_node_console(sim_name, node=node)
        if node:
            click.secho("Attempting to connect to console " "of {}".format(node))
            try:
                ip, port = resp.json()[node].split(":")

                # use user specified telnet command
                if "VIRL_CONSOLE_COMMAND" in server.config:
                    cmd = server.config["VIRL_CONSOLE_COMMAND"]
                    cmd = cmd.format(host=ip, port=port)
                    print("Calling user specified command: {}".format(cmd))
                    exit(call(cmd.split()))

                # someone still uses windows
                elif platform.system() == "Windows":
                    with helpers.disable_file_system_redirection():
                        exit(call(["telnet", ip, port]))

                # why is shit so complicated?
                else:
                    exit(call(["telnet", ip, port]))
            except AttributeError:
                click.secho("Could not find console info for " "{}:{}".format(env, node), fg="red")
            except KeyError:
                click.secho("Unknown node {}:{}".format(env, node), fg="red")
        else:
            # defaults to displaying table
            console_table1(resp.json())
