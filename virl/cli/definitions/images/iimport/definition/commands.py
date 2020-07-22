import click
import os
from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.argument("image", nargs=1)
@click.option("-f", "--filename", required=True, metavar="<filename>", help="path to the local image definition file")
def definition(image, filename):
    """
    import an image definition
    """

    server = VIRLServer()
    client = get_cml_client(server)

    if not os.path.isfile(filename):
        click.secho("Image definition file {} does not exist or is not a file", fg="red")
        exit(1)
    else:
        defs = client.definitions
        contents = None

        with open(filename, "r") as fd:
            contents = fd.read()

        try:
            defs.upload_image_definition(image, contents)
        except Exception as e:
            click.secho("Failed to import image definition for {}: {}".format(image, e), fg="red")
            exit(1)
