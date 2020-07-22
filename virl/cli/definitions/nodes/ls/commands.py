import click
from virl.api import VIRLServer
from virl.cli.views import node_def_list_table
from virl.helpers import get_cml_client


@click.command()
@click.option("--node", default=None)
def ls(**kwargs):
    """
    list all node definitions or the details of a specific node definition
    """

    node = kwargs.get("node")
    server = VIRLServer()
    client = get_cml_client(server)

    # Regardless of the argument, we have to get all the node definitions
    # In the case of no arg, we print them all.
    # In the case of an arg, we have to go back and get details.
    defs = client.definitions.node_definitions()

    if node:
        for f in list(defs):
            if f["id"] == node:
                node_def_list_table([f])
                break
    else:
        node_def_list_table(defs)
