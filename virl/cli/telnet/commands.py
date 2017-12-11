import click
from virl.api import VIRLServer
from subprocess import call
from virl import helpers

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
    else:
        # assume default env
        env = 'default'
        running = helpers.check_sim_running(env)
        node = node[0]
    if running:
        sim_name = running
        server = VIRLServer()
        details = server.get_sim_roster(sim_name)
        #resp = server.get_node_console(sim_name, node=node)
        for node_dict in details.values():
            node_name = node_dict.get("NodeName")
            if node_name == node:
                print "will attempt a telnet connection with this info"
                print node_dict
                # TODO WIP


        # if node:
        #     print "Attempting to connect to console of {}".format(node)
        #     try:
        #         ip, port = resp.json()[node].split(':')
        #         exit(call(['telnet', ip, port]))
        #     except AttributeError:
        #         click.secho("Could not find console info for {}:{}".format(env,node), fg="red")
        #     except KeyError:
        #         click.secho("Unknown node {}:{}".format(env,node), fg="red")
        # else:
        #     return resp.json()
