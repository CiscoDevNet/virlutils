import click
from virl.api import VIRLServer
from virl import helpers
import subprocess


@click.command()
@click.argument("env", default="default")
def viz1(env):
    """
    opens live visualization for the sim
    """
    server = VIRLServer()
    running = helpers.check_sim_running(env)

    if running:
        sim_name = running
        url = "http://{}:19402/?sim_id={}#/layer/phy".format(server.host, sim_name)
        subprocess.Popen(["open", url])
    else:
        click.secho("No Running simulation to visualize", fg="red")
