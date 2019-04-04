import os
import click
from virl.api import VIRLServer
from virl.cli.views import sim_list_table
from virl.helpers import find_virl


@click.command()
@click.option('--all/--local', default=False, help=" \
Display all simulations or only ones from the current project (default)")
def ls(all, **kwargs):
    """
    lists running simulations in the current project
    """

    server = VIRLServer()

    sim_dict = server.list_simulations()
    if not all:
        # only sims for this project
        dirpath = find_virl()
        foldername = os.path.basename(dirpath)
        for k in list(sim_dict):
            if not k.startswith(foldername):
                sim_dict.pop(k)

    sim_list_table(sim_dict)
