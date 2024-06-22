import click

from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
def authorization():
    """
    renew Smart License authorization
    """
    server = VIRLServer()
    client = get_cml_client(server)
    licensing = client.licensing

    try:
        licensing.renew_authorization()
    except Exception as e:
        click.secho("Failed to renew authorization: {}".format(e), fg="red")
        exit(1)
