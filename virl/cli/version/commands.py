import click
from virl.api import VIRLServer
from virl import __version__


@click.command()
def version():
    """
    version information
    """
    server = VIRLServer()
    virlutils_version = __version__
    server_version = server.get_version().get('virl-version')
    click.secho("virlutils Version: {}".format(virlutils_version))
    click.echo("VIRL Core Version: {}".format(server_version))
