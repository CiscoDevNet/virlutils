import click

from virl.api import VIRLServer
from virl.api.nso import NSO
from virl.cli.views import sync_table
from virl.generators import nso_payload_generator
from virl.helpers import (get_cml_client, get_current_lab,
                          safe_join_existing_lab)


@click.command()
@click.option("--output", "-o", help="just dump the payload to file without sending")
@click.option("--syncfrom/--no-syncfrom", default=False, help="Perform sync-from after updating devices")
def nso(syncfrom, **kwargs):
    """
    generate nso inventory
    """

    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            if kwargs.get("output"):
                file_name = kwargs.get("output")
            else:
                file_name = None

            inv = nso_payload_generator(lab, server)

            if inv:
                if file_name:
                    click.secho("Writing {}".format(file_name))
                    with open(file_name, "w") as fd:
                        fd.write(inv)
                else:
                    click.secho("Updating NSO....")
                    nso_obj = NSO()
                    nso_response = nso_obj.update_devices(inv)
                    if nso_response.ok:
                        click.secho("Successfully added CML devices to NSO")
                    else:
                        click.secho("Error updating NSO: ", fg="red")
                        click.secho(nso_response.text)
                    if syncfrom:
                        resp = nso_obj.perform_sync_from()
                        sync_table(resp.json())
            else:
                click.secho("Failed to get inventory data", fg="red")
                exit(1)
        else:
            click.secho("Failed to find running lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("Current lab is not set", fg="red")
        exit(1)
