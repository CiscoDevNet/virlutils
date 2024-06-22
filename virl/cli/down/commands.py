import click

from virl.api import VIRLServer
from virl.helpers import (get_cml_client, get_current_lab,
                          safe_join_existing_lab,
                          safe_join_existing_lab_by_title)


@click.command()
@click.option("--id", required=False, help="An existing lab ID to stop (lab-name is ignored)")
@click.option("--lab-name", "-n", "--sim-name", required=False, help="An existing lab name to stop")
def down(id=None, lab_name=None):
    """
    stop a lab
    """
    server = VIRLServer()
    client = get_cml_client(server)

    lab = None

    if id:
        lab = safe_join_existing_lab(id, client)

    if not lab and lab_name:
        lab = safe_join_existing_lab_by_title(lab_name, client)

    if not lab:
        lab_id = get_current_lab()
        if lab_id:
            lab = safe_join_existing_lab(lab_id, client)

    if lab:
        if lab.is_active():
            click.secho("Shutting down lab {} (ID: {}).....".format(lab.title, lab.id))
            lab.stop()
            click.echo(click.style("SUCCESS", fg="green"))
        else:
            click.secho("Lab with ID {} and title {} is already stopped".format(lab.id, lab.title))

    else:
        click.secho("Failed to find lab on server", fg="red")
        exit(1)
