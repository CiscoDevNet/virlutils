import click

from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.argument("node", nargs=1)
@click.option("-f", "--filename", required=False, metavar="<filename>", help="filename to save to")
def export(node, filename):
    """
    export a node definition
    """

    server = VIRLServer()
    client = get_cml_client(server)

    if not filename:
        filename = node + ".yaml"

    defs = client.definitions

    try:
        ndef = defs.download_node_definition(node)
    except Exception as e:
        click.secho("Failed to download node definition for {}: {}".format(node, e), fg="red")
        exit(1)
    else:
        with open(filename, "w") as fd:
            fd.write(ndef)
