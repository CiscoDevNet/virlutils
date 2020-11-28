import click
from virl.api import VIRLServer, ViewerPlugin, NoPluginError
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
    pl = None

    # Regardless of the argument, we have to get all the flavors
    # In the case of no arg, we print them all.
    # In the case of an arg, we have to go back and get details.
    defs = client.definitions.image_definitions()

    try:
        pl = ViewerPlugin(viewer="image_def")
    except NoPluginError:
        pass

    if image:
        for f in list(defs):
            if f["name"] == image:
                if pl:
                    pl.visualize(image_defs=[f])
                else:
                    image_list_table([f])
                break
    else:
        if pl:
            pl.visualize(image_defs=defs)
        else:
            image_list_table(defs)
