import click
import os
from subprocess import call
from virl.api import VIRLServer
from virl.helpers import store_sim_info, get_cml_client, get_lab_by_title, check_lab_server, check_lab_cache, cache_lab, set_current_lab

# This may need to become a helper
def check_lab_server_cache(lab_id, client):
    ret = None

    if not check_lab_cache(lab_id):
        if check_lab_server(lab_id, client):
            lab_obj = client.join_existing_lab(lab_id)
            msg = cache_lab(lab_obj)
            if msg:
                return None

            ret = lab_id
    else:
        ret = lab_id

    return ret


@click.command()
@click.argument("lab", required=False)
@click.option("--id", required=False, help="An existing CML lab ID to start (lab-name is ignored)")
@click.option("--lab-name", "-n", required=False, help="An existing CML lab name to start")
def use(lab, id, lab_name):
    """
    use CML lab launched elsewhere
    """
    server = VIRLServer()
    client = get_cml_client(server)
    lab_id = None

    if not lab and not id and not lab_name:
        call(["virl", "use", "--help"])
        return

    if id:
        lab_id = check_lab_server_cache(id, client)

    # Prefer --lab-name over positional argument
    if lab_name:
        lab = lab_name

    if not id and lab:
        lab_obj = get_lab_by_title(lab, client)
        if lab_obj:
            lab_id = check_lab_server_cache(lab_obj.id, client)

    if lab_id:
        lab_obj = client.join_existing_lab(lab_id)
        msg = set_current_lab(lab_obj)
        if msg:
            click.secho("Failed to use lab {} (ID: {}): {}".format(lab_obj.title, lab_obj.id, msg))
    else:
        click.secho("Unable to find lab on server or in cache", fg="red")


@click.command()
@click.argument("sim")
def use1(sim):
    """
    use virl simulation launched elsewhere
    """
    store_sim_info(sim, env="default")  # 'topology-2lkx2'
    click.secho("Now using VIRL simulation {}".format(sim))
