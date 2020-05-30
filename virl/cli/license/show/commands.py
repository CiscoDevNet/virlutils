import click
from virl.api import VIRLServer
from virl.cli.views import license_details_table
from virl.helpers import get_cml_client


@click.command()
def show():
    """
    display license details
    """
    server = VIRLServer()
    client = get_cml_client(server)

    # As of 2.0.0b5 of virl2-client, there is no Python API for licensing.  So we use
    # the library as much as we can, and use requests for the rest.
    try:
        response = client.session.get(client._base_url + "licensing")
        response.raise_for_status()
        license = response.json()
    except Exception as e:
        click.secho("Failed to get license details: {}".format(e), fg="red")
        exit(1)
    else:
        license_details_table(license)
