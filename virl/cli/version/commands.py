import click
from virl.api import VIRLServer
from virl import __version__
from virl.helpers import get_cml_client


@click.command()
def version():
    """
    version information
    """
    server = VIRLServer()
    client = get_cml_client(server)
    server_version = "Unknown"
    try:
        response = client.session.get(client._base_url + "system_information")
        response.raise_for_status()
        server_version = response.json()["version"]
    except Exception:
        pass
    virlutils_version = __version__
    click.secho("virlutils Version: {}".format(virlutils_version))
    click.secho("CML Controller Version: {}".format(server_version))


@click.command()
def version1():
    """
    version information
    """
    server = VIRLServer()
    virlutils_version = __version__
    server_version = server.get_version().get("virl-version")
    click.secho("virlutils Version: {}".format(virlutils_version))
    click.echo("VIRL Core Version: {}".format(server_version))
