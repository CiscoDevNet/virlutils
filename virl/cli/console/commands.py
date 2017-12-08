import click
from virl.api import VIRLServer
from subprocess import call
from virl import helpers

@click.command()
@click.argument('env', default='default')
@click.argument('node', default=None, required=False)
def console(env, node):
    """
    console for node
    """
    print env, node
    running = helpers.check_sim_running(env)
    if running:

        sim_name = running
        server = VIRLServer()
        resp = server.get_node_console(sim_name, node=node)
        if node:
            print "Attempting to connect to console of {}".format(node)
            ip, port = resp.json()[node].split(':')
            exit(call(['telnet', ip, port]))
        else:
            return resp.json()
