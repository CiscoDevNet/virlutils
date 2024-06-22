import click

from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.argument("image", nargs=1)
@click.option("-f", "--filename", required=False, metavar="<filename>", help="filename to save to")
def export(image, filename):
    """
    export an image definition
    """

    server = VIRLServer()
    client = get_cml_client(server)

    if not filename:
        filename = image + ".yaml"

    defs = client.definitions

    try:
        idef = defs.download_image_definition(image)
    except Exception as e:
        click.secho("Failed to download image definition for {}: {}".format(image, e), fg="red")
        exit(1)
    else:
        with open(filename, "w") as fd:
            fd.write(idef)
