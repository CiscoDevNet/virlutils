import click
from virl.api import VIRLServer
from virl.cli.views import sim_list_table

@click.command()
def ls(**kwargs):
    """
    lists running simulations
    """
    server = VIRLServer()
    sim_dict = server.list_simulations()
    sim_list_table(sim_dict)
