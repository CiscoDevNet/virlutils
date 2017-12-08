import click

from virl.api import VIRLServer
from virl.cli.views import node_list_table
from virl import helpers

@click.command()
@click.argument('env', default='default')
def nodes(env, **kwargs):
    """
    get nodes for sim_name
    """
    running = helpers.check_sim_running(env)
    if running:
        sim_name = running
        server = VIRLServer()
        resp = server.get_nodes(sim_name)
        node_list_table(resp)
    else:
        click.secho("Environment {} is not running".format(env), fg='red')
