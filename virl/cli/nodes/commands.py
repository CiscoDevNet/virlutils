import click
from virl.api import VIRLServer, ViewerPlugin, NoPluginError
from virl.cli.views import node_list_table1, node_list_table
from virl.helpers import get_cml_client, get_current_lab, safe_join_existing_lab
from virl import helpers


@click.command()
def nodes():
    """
    get node list for the current lab
    """
    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            try:
                pl = ViewerPlugin(viewer="node")
                pl.visualize(nodes=lab.nodes())
            except NoPluginError:
                node_list_table(lab.nodes())
        else:
            click.secho("Lab {} is not running".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("No current lab selected", fg="red")
        exit(1)


@click.command()
@click.argument("env", default="default")
def nodes1(env, **kwargs):
    """
    get nodes for sim_name
    """
    running = helpers.check_sim_running(env)
    if running:
        sim_name = running
        server = VIRLServer()
        details = server.get_sim_roster(sim_name)
        node_list_table1(details)
    else:
        click.secho("Environment {} is not running".format(env), fg="red")
