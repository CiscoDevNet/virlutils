import click
from virl.api import VIRLServer
from subprocess import call
from virl import helpers


@click.command()
@click.argument('node', nargs=-1)
def stop(node):
    """
    stop a node
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
        exit(call(['virl', 'stop', '--help']))

    if running:
        sim_name = running
        server = VIRLServer()
        resp = server.stop_node(sim_name, node)
        if resp.ok:
            click.secho("Stopped node {}".format(node))
        else:
            click.secho("Error Stopping Node {}: {}".format(node, resp),
                        fg="red")
