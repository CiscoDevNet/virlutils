import os

import click

from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.option("-f", "--filename", required=True, metavar="<filename>", help="path to the local node definition file")
def nimport(filename):
    """
    import a node definition
    """

    server = VIRLServer()
    client = get_cml_client(server)

    if not os.path.isfile(filename):
        click.secho("Node definition file {} does not exist or is not a file", fg="red")
        exit(1)
    else:
        defs = client.definitions
        contents = None

        with open(filename, "r") as fd:
            contents = fd.read()

        try:
            defs.upload_node_definition(contents)
        except Exception as e:
            click.secho("Failed to import node definition: {}".format(e), fg="red")
            exit(1)
