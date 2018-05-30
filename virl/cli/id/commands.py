import os
import click
from virl.api import VIRLServer


@click.command()
def id():
    """
    gets sim id for local environment
    """

    server = VIRLServer()

    sim_dict = server.list_simulations()
    dirpath = os.getcwd()
    foldername = os.path.basename(dirpath)
    for k in list(sim_dict):
        if not k.startswith(foldername):
            sim_dict.pop(k)
    # can only accurately determine sim id if there is
    # only one sim running with our project name
    if len(sim_dict) == 1:
        click.echo(list(sim_dict)[0])
