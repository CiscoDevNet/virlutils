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
    licensing = client.licensing

    try:
        licensing.register_renew()
    except Exception as e:
        click.secho("Failed to renew registration: {}".format(e), fg="red")
        exit(1)
