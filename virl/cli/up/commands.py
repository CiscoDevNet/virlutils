import click

from virl.api import VIRLServer
from virl.helpers import generate_sim_id, check_sim_running, store_sim_info
import os, os.path
import errno


@click.command()
@click.argument('env', default='default')
@click.option('-f', help='filename', required=False)
def up(env, **kwargs):
    """
    start a virl simulation
    """
    if kwargs['f']:
        fname = kwargs['f']
    else:
        fname = 'topology.virl'
    if os.path.exists(fname):
        running = check_sim_running(env)
        if not running:
            click.secho('Creating {} environment from {}'.format(env, fname))
            with open(fname) as fh:
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
        click.secho('Could not find topology.virl. Maybe try -f', fg="red")
