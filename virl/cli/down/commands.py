import click
from virl.api import VIRLServer

@click.command()
@click.argument('sim_name')
def down(sim_name, **kwargs):
    """
    stop a virl simulation
    """
    server = VIRLServer()
    resp = server.stop_simulation(sim_name)
    print("Shutting Down Simulation {}.....".format(sim_name)),
    click.echo(resp.text)
