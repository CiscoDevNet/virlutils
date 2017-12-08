import click

from virl.api import VIRLServer
from virl.cli.views import log_table

@click.command()
@click.argument('sim_name')
def logs(sim_name, **kwargs):
    """
    get logs for sim_name
    """
    server = VIRLServer()
    resp = server.get_logs(sim_name)
    log_table(resp.json()['events'])
