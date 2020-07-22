import click
from virl.api import VIRLServer
from virl.cli.views import image_list_table
from virl.helpers import get_cml_client


@click.command()
@click.option("--image", default=None)
def ls(**kwargs):
    """
    list all images or the details of a specific image
    """

    image = kwargs.get("image")
    server = VIRLServer()
    client = get_cml_client(server)

    # Regardless of the argument, we have to get all the flavors
    # In the case of no arg, we print them all.
    # In the case of an arg, we have to go back and get details.
    defs = client.definitions.image_definitions()

    if image:
        for f in list(defs):
            if f["name"] == image:
                image_list_table([f])
                break
    else:
        image_list_table(defs)
