import click

from virl.api import NoPluginError, ViewerPlugin, VIRLServer
from virl.cli.views import license_details_table
from virl.helpers import get_cml_client


@click.command()
def show():
    """
    display license details
    """
    server = VIRLServer()
    client = get_cml_client(server)
    licensing = client.licensing

    try:
        license = licensing.status()
    except Exception as e:
        click.secho("Failed to get license details: {}".format(e), fg="red")
        exit(1)
    else:
        try:
            pl = ViewerPlugin(viewer="license")
            pl.visualize(license=license)
        except NoPluginError:
            license_details_table(license)
