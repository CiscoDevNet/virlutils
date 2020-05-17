import os
import click
from virl.api import VIRLServer
from virl.helpers import get_current_lab, get_cml_client, safe_join_existing_lab, get_current_lab_link


@click.command()
def id():
    """
    get the current lab title and ID
    """
    server = VIRLServer()
    client = get_cml_client(server)
    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        # The lab really should be on the server.
        if not lab:
            lab = CachedLab(current_lab, get_current_lab_link())

        if lab:
            click.echo("{} (ID: {})".format(lab.title, current_lab))


@click.command()
def id1():
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
