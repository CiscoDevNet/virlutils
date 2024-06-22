import click

from virl import __version__
from virl.api import VIRLServer
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
        server_version = client.system_info()["version"]
    except Exception:
        pass
    virlutils_version = __version__
    click.secho("cmlutils Version: {}".format(virlutils_version))
    click.secho("CML Controller Version: {}".format(server_version))
