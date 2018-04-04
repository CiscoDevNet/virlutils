import click
from virl.api import VIRLServer
from virl.helpers import check_sim_running, remove_sim_info


@click.command()
@click.argument('env', default='default')
@click.option('--sim-name', required=False)
def down(sim_name=None, env='default', **kwargs):
    """
    stop a virl simulation
    """
    # by env name
    running = check_sim_running(env)
    if running:
        sim_name = running
    # by sim name
    elif sim_name:
        sim_name = sim_name
    else:
        click.secho("Could not find sim for environment {}".format(env))
        exit(1)
    server = VIRLServer()
    resp = server.stop_simulation(sim_name)
    remove_sim_info(env=env)
    if not resp.ok:
        cause = resp.json()['cause']
        result = click.style(cause, fg="red")
    else:
        result = click.style(resp.text, fg="green")
    click.secho("Shutting Down Simulation {}.....".format(sim_name)),
    click.echo(result)
