import click

from virl.api import NoPluginError, ViewerPlugin, VIRLServer
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
    defs_orig = client.definitions.node_definitions()

    # Create a new list of the *flattened* node definitions.  CML 2.3 removed the
    # extra "data" layer of nesting in the node def JSON format.  To make the rest
    # of the code work no matter which version of CML we're talking to, create a
    # list of node definitions, removing the extra layer of nesting if needed.
    defs = [f["data"] if "data" in f else f for f in defs_orig]

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
