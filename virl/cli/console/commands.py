import click
from virl.api import VIRLServer
from subprocess import call
from virl import helpers

@click.command()
@click.argument('node', nargs=-1)
def console(node):
    """
    console for node
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
        resp = server.get_node_console(sim_name, node=node)
        if node:
            print "Attempting to connect to console of {}".format(node)
            try:
                ip, port = resp.json()[node].split(':')
                exit(call(['telnet', ip, port]))
            except AttributeError:
                click.secho("Could not find console info for {}:{}".format(env,node), fg="red")
            except KeyError:
                click.secho("Unknown node {}:{}".format(env,node), fg="red")
        else:
            return resp.json()
