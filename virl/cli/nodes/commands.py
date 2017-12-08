import click

from virl.api import VIRLServer
from virl.cli.views import node_list_table

@click.command()
@click.argument('sim_name')
def nodes(sim_name, **kwargs):
    """
    get nodes for sim_name
    """
    server = VIRLServer()
    resp = server.get_nodes(sim_name)
    node_list_table(resp)
