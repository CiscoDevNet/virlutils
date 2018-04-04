import click

from virl.api import VIRLServer
from virl.helpers import generate_sim_id, check_sim_running, store_sim_info
import os, os.path


@click.command()
@click.argument('sim')
def use(sim):
    """
    use virl simulation launched elsewhere
    """
    dirpath = os.getcwd()
    foldername = os.path.basename(dirpath)
    store_sim_info(sim, env='default') # 'topology-2lkx2'
    click.secho('Now using VIRL simulation {}'.format(sim))
