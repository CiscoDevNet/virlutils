import click

from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.option(
    "--id",
    "-i",
    required=True,
    help="ID for the Smart License feature to modify",
)
@click.option("--value", "-v", required=True, type=int, help="Number of licenses of this feature to use")
def update(id, value):
    """
    update the number of feature instances
    """
    server = VIRLServer()
    client = get_cml_client(server)
    licensing = client.licensing

    try:
        licensing.update_features({id: value})
    except Exception as e:
        click.secho("Failed to update features: {}".format(e), fg="red")
        exit(1)
