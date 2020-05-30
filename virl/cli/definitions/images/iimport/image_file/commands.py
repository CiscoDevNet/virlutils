import click
import os
from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.option("-f", "--filename", required=True, metavar="<filename>", help="path to local image file")
@click.option("--rename", required=False, metavar="<filename>", help="optional new name to give the file on the server")
def image_file(filename, rename):
    """
    import an image file
    """

    server = VIRLServer()
    client = get_cml_client(server)

    if not os.path.isfile(filename):
        click.secho("Image file {} does not exist or is not a file", fg="red")
        exit(1)
    else:
        defs = client.definitions
        try:
            defs.upload_image_file(filename, rename)
        except Exception as e:
            click.secho("Failed to import image file {}: {}".format(filename, e), fg="red")
            exit(1)
