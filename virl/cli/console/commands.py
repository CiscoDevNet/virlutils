import click
from virl.api import VIRLServer
from subprocess import call

@click.command()
@click.argument('sim_name')
@click.argument('node', required=False)
def console(sim_name, node):
    """
    console for node
    """
    server = VIRLServer()
    resp = server.get_node_console(sim_name, node=node)
    if node:
        print "Attempting to connect to console of {}".format(node)
        ip, port = resp.json()[node].split(':')
        exit(call(['telnet', ip, port]))
    else:
        return resp.json()
