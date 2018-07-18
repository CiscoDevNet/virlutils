import click
from virl.api import VIRLServer
from subprocess import call
from virl import helpers
from virl.helpers import get_mgmt_lxc_ip, get_node_from_roster


@click.command()
@click.argument('node', nargs=-1)
def telnet(node):
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
        env = 'default'
        running = helpers.check_sim_running(env)
        node = node[0]
    else:
        exit(call(['virl', 'telnet', '--help']))

    if running:
        sim_name = running
        server = VIRLServer()
        details = server.get_sim_roster(sim_name)

        if node:
            try:
                node_dict = get_node_from_roster(node, details)
                node_name = node_dict.get("NodeName")
                ip = node_dict['managementIP']
                proxy = node_dict.get("managementProxy")

                # use user specified telnet command
                if 'VIRL_TELNET_COMMAND' in server.config:
                    cmd = server.config['VIRL_TELNET_COMMAND']
                    cmd = cmd.format(host=ip)
                    print("Calling user specified command: {}".format(cmd))
                    exit(call(cmd.split()))

                if proxy == 'lxc':
                    lxc = get_mgmt_lxc_ip(details)
                    click.secho("Attemping telnet connection"
                                " to {} at {} via ssh {}".format(node_name,
                                                                 ip, lxc))
                    cmd = 'ssh -t {}@{} "telnet {}"'
                    cmd = cmd.format(server.user, lxc, ip)

                    exit(call(cmd, shell=True))
                else:
                    # handle the "flat" networking case
                    click.secho("Attemping telnet connection"
                                " to {} at {}".format(node_name,
                                                      ip))
                    exit(call(['telnet', ip]))

            except AttributeError:
                click.secho("Could not find management info "
                            "for {}:{}".format(env, node), fg="red")

            except KeyError:
                click.secho("Unknown node {}:{}".format(env, node), fg="red")
        else:
            return details.json()
