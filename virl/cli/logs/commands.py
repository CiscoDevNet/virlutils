import click

from virl.api import VIRLServer
from virl.cli.views import log_table
from virl import helpers


@click.command()
@click.argument('env', default='default')
def logs1(env, **kwargs):
    """
    Retrieves log information for the provided simulation
    """
    running = helpers.check_sim_running(env)
    if running:
        sim_name = running
        server = VIRLServer()
        resp = server.get_logs(sim_name)
        log_table(resp.json()['events'])
    else:
        click.secho("could not find logs for for env: {}".format(env),
                    fg='red')
