import click
from virl.api import VIRLServer, ViewerPlugin, NoPluginError
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
    pl = None

    # Regardless of the argument, we have to get all the node definitions
    # In the case of no arg, we print them all.
    # In the case of an arg, we have to go back and get details.
    defs = client.definitions.node_definitions()

    try:
        pl = ViewerPlugin(viewer="node_def")
    except NoPluginError:
        pass

    if node:
        for f in list(defs):
            if f["id"] == node:
                if pl:
                    pl.visualize(node_defs=[f])
                else:
                    node_def_list_table([f])
                break
    else:
        if pl:
            pl.visualize(node_defs=defs)
        else:
            node_def_list_table(defs)
