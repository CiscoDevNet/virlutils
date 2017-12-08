import click

from virl.api import VIRLServer
from virl.helpers import generate_sim_id
import os, os.path
import errno

# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')

def store_sim_info(name, env='default'):
    with safe_open_w('./.virl/{}/id'.format(env)) as f:
        f.write(name)



@click.command()
@click.option('--env', '-e', default='default', help='environment name')
def up(**kwargs):
    """
    start a virl simulation
    """
    if os.path.exists('topology.virl'):
        print kwargs
        click.secho('Launching Simulation from topology.virl', fg='green')
        with open('topology.virl') as fh:
            data = fh.read()
        server = VIRLServer()
        dirpath = os.getcwd()
        foldername = os.path.basename(dirpath)
        sim_name = "{}_{}_{}".format(foldername, kwargs['env'], generate_sim_id())
        resp = server.launch_simulation(sim_name, data)
        store_sim_info(resp.text, env=kwargs['env']) # 'topology-2lkx2'
    else:
        print('Could not find virl file')
