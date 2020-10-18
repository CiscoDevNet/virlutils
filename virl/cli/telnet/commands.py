import click
from virl.api import VIRLServer
from subprocess import call
from virl import helpers
from virl.helpers import (
    get_mgmt_lxc_ip,
    get_node_from_roster,
    get_cml_client,
    get_current_lab,
    safe_join_existing_lab,
    get_node_mgmt_ip,
    get_command,
)
from virl2_client.exceptions import NodeNotFound


@click.command()
@click.argument("node", nargs=1)
def telnet(node):
    """
    telnet to a node
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

            if node_obj.is_active():
                mgmtip = get_node_mgmt_ip(node_obj)
                if mgmtip:
                    if "VIRL_TELNET_COMMAND" in server.config:
                        cmd = server.config["VIRL_TELNET_COMMAND"]
                        cmd = cmd.format(host=mgmtip)
                        print("Calling user specified command: {}".format(cmd))
                        exit(call(cmd.split()))
                    else:
                        click.secho("Attemping telnet connection to {} at {}".format(node_obj.label, mgmtip))

                        exit(call(["telnet", mgmtip]))
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


@click.command()
@click.argument("node", nargs=-1)
def telnet1(node):
    """
    telnet to a node
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
        exit(call([get_command(), "telnet", "--help"]))

    if running:
        sim_name = running
        server = VIRLServer()
        details = server.get_sim_roster(sim_name)

        if node:
            try:
                node_dict = get_node_from_roster(node, details)
                node_name = node_dict.get("NodeName")
                ip = node_dict["managementIP"]
                proxy = node_dict.get("managementProxy")

                # use user specified telnet command
                if "VIRL_TELNET_COMMAND" in server.config:
                    cmd = server.config["VIRL_TELNET_COMMAND"]
                    cmd = cmd.format(host=ip)
                    print("Calling user specified command: {}".format(cmd))
                    exit(call(cmd.split()))

                if proxy == "lxc":
                    lxc = get_mgmt_lxc_ip(details)
                    click.secho("Attemping telnet connection" " to {} at {} via ssh {}".format(node_name, ip, lxc))
                    cmd = 'ssh -t {}@{} "telnet {}"'
                    cmd = cmd.format(server.user, lxc, ip)

                    exit(call(cmd, shell=True))
                else:
                    # handle the "flat" networking case
                    click.secho("Attemping telnet connection" " to {} at {}".format(node_name, ip))
                    exit(call(["telnet", ip]))

            except AttributeError:
                click.secho("Could not find management info " "for {}:{}".format(env, node), fg="red")

            except KeyError:
                click.secho("Unknown node {}:{}".format(env, node), fg="red")
        else:
            return details.json()
