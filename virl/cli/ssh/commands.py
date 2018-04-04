import click
from virl.api import VIRLServer
from subprocess import call
from virl import helpers

@click.command()
@click.argument('node', nargs=-1)
def ssh(node):
    """
    ssh to a node
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
        exit(call(['virl', 'ssh', '--help']))

    if running:
        sim_name = running
        server = VIRLServer()
        details = server.get_sim_roster(sim_name)
        #resp = server.get_node_console(sim_name, node=node)
        if node:
            try:
                for k,v in details.items():
                    if k.endswith(node):
                        ip = details[k]['managementIP']
                        for node_dict in details.values():
                            node_name = node_dict.get("NodeName")
                            if node_name == node:
                                click.secho("Attemping ssh connection to {} at {}".format(node_name, ip))

                        exit(call(['ssh', 'cisco@{}'.format(ip)]))

            except AttributeError:
                click.secho("Could not find management info for {}:{}".format(env,node), fg="red")

            except KeyError:
                click.secho("Unknown node {}:{}".format(env,node), fg="red")
        else:
            return details.json()
