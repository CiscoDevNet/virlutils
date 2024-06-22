import click

from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.option(
    "--confirm/--no-confirm",
    show_default=False,
    default=True,
    help="Do not prompt for confirmation (default: prompt)",
    required=False,
)
def deregister(confirm):
    """
    deregister the Smart License
    """
    server = VIRLServer()
    client = get_cml_client(server)
    licensing = client.licensing

    ret = "y"
    if confirm:
        ret = input("Are you sure you want to deregister [y/N]? ")
        if not ret.lower().startswith("y"):
            click.secho("Not deregistering")
            exit(0)

    try:
        licensing.deregister()
    except Exception as e:
        click.secho("Failed to deregister with Smart Licensing: {}".format(e), fg="red")
        exit(1)
