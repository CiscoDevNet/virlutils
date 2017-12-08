import click

from virl.api import VIRLServer
from virl.helpers import generate_sim_id, check_sim_running, store_sim_info
import os, os.path
import errno


@click.command()
@click.argument('env', default='default')
def up(env, **kwargs):
    """
    start a virl simulation
    """

    if os.path.exists('topology.virl'):
        running = check_sim_running(env)
        if not running:
            click.secho('Creating {} environment from topology.virl'.format(env))
            with open('topology.virl') as fh:
                data = fh.read()
            server = VIRLServer()
            dirpath = os.getcwd()
            foldername = os.path.basename(dirpath)
            sim_name = "{}_{}_{}".format(foldername, env, generate_sim_id())
            resp = server.launch_simulation(sim_name, data)
            store_sim_info(resp.text, env=env) # 'topology-2lkx2'
        else:
            click.secho('Sim {} already running'.format(running))
    else:
        print('Could not find virl file')
