import click

from virl.api import VIRLServer
from virl.cli.views import log_table

@click.command()
@click.argument('sim_name')
def logs(sim_name, **kwargs):
    """
    Retrieves log information for the provided simulation
    """
    server = VIRLServer()
    resp = server.get_logs(sim_name)
    log_table(resp.json()['events'])
