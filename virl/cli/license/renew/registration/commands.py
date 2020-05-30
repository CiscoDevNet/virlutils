import click
from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
def registration():
    """
    renew Smart License registration
    """
    server = VIRLServer()
    client = get_cml_client(server)

    # As of 2.0.0b5 of virl2-client, there is no Python API for licensing.  So we use
    # the library as much as we can, and use requests for the rest.

    try:
        response = client.session.put(client._base_url + "licensing/registration/renew")
        response.raise_for_status()
    except Exception as e:
        click.secho("Failed to renew registration: {}".format(e), fg="red")
        exit(1)
