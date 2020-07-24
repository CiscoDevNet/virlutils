import os
import click
from virl.api import VIRLServer, CachedLab
from virl.helpers import get_current_lab, get_cml_client, safe_join_existing_lab, get_current_lab_link


@click.command()
def lid():
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
            try:
                lab = CachedLab(current_lab, get_current_lab_link())
            except Exception:
                pass

        if lab:
            click.echo("{} (ID: {})".format(lab.title, current_lab))
        else:
            click.secho("Current lab is set to {}, but is not on server or in cache!".format(current_lab), fg="red")


@click.command()
def sid():
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
