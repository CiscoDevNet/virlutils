import click
from virl.api import VIRLServer
from virl import helpers
import subprocess


@click.command()
@click.argument('env', default='default')
def uwm1(env):
    """
    opens UWM for the sim
    """
    server = VIRLServer()
    running = helpers.check_sim_running(env)

    if running:
        sim_name = running
        # luanches uwm
        url = "http://{}:{}@{}/simulation/{}/{}"
        url = url.format(server.user, server.passwd,
                         server.host, server.user, sim_name)
        subprocess.Popen(['open', url])
