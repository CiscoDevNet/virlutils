import click
import os
from virl.api import VIRLServer
from virl.helpers import get_env_sim_name

@click.command()
@click.argument('env', default='default')
@click.option('--ip/--no-ip', default=False, help="include dynamically assigned addresses")
def save(env, ip, **kwargs):
    """
    save simulation to local virl file
    """
    if os.path.exists('topology.virl'):
        sim_name = get_env_sim_name(env)
        server = VIRLServer()
        resp = server.export(sim_name, ip=ip)
        print resp.text
        with open('topology.virl', 'w') as fh:
            fh.write(resp.text)

    else:
        click.secho("No local virl file detected", fg='red')
