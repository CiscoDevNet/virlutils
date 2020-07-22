import click
from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.option(
    "--confirm/--no-confirm", show_default=False, default=True, help="Do not prompt for confirmation (default: prompt)", required=False,
)
def deregister(confirm):
    """
    deregister the Smart License
    """
    server = VIRLServer()
    client = get_cml_client(server)

    # As of 2.0.0b5 of virl2-client, there is no Python API for licensing.  So we use
    # the library as much as we can, and use requests for the rest.

    ret = "y"
    if confirm:
        ret = input("Are you sure you want to deregister [y/N]? ")
        if not ret.lower().startswith("y"):
            click.secho("Not deregistering")
            exit(0)

    try:
        response = client.session.delete(client._base_url + "licensing/deregistration")
        response.raise_for_status()
    except Exception as e:
        click.secho("Failed to deregister the Smart License: {}".format(e), fg="red")
        exit(1)
