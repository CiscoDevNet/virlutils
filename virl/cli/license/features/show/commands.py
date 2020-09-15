import click
from virl.api import VIRLServer
from virl.cli.views import license_features_table
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
        license = licensing.features()
    except Exception as e:
        click.secho("Failed to get license features: {}".format(e), fg="red")
        exit(1)
    else:
        license_features_table(license)
