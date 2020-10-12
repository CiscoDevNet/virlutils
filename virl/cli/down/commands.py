import click
from virl.api import VIRLServer
from virl.helpers import (
    check_sim_running,
    remove_sim_info,
    get_cml_client,
    safe_join_existing_lab_by_title,
    safe_join_existing_lab,
    get_current_lab,
)


@click.command()
@click.option("--id", required=False, help="An existing lab ID to stop (lab-name is ignored)")
@click.option("--lab-name", "-n", "--sim-name", required=False, help="An existing lab name to stop")
def down(id=None, lab_name=None):
    """
    stop a lab
    """
    server = VIRLServer()
    client = get_cml_client(server)

    lab = None

    if id:
        lab = safe_join_existing_lab(id, client)

    if not lab and lab_name:
        lab = safe_join_existing_lab_by_title(lab_name, client)

    if not lab:
        lab_id = get_current_lab()
        if lab_id:
            lab = safe_join_existing_lab(lab_id, client)

    if lab:
        if lab.is_active():
            click.secho("Shutting down lab {} (ID: {}).....".format(lab.title, lab.id))
            lab.stop()
            click.echo(click.style("SUCCESS", fg="green"))
        else:
            click.secho("Lab with ID {} and title {} is already stopped".format(lab.id, lab.title))

    else:
        click.secho("Failed to find lab on server", fg="red")
        exit(1)


@click.command()
@click.argument("env", default="default")
@click.option("--sim-name", required=False)
def down1(sim_name=None, env="default", **kwargs):
    """
    stop a virl simulation
    """
    # by env name
    running = check_sim_running(env)
    if running:
        sim_name = running
    # by sim name
    elif sim_name:
        sim_name = sim_name
    else:
        click.secho("Could not find sim for environment {}".format(env))
        exit(1)
    server = VIRLServer()
    resp = server.stop_simulation(sim_name)
    remove_sim_info(env=env)
    if not resp.ok:
        cause = resp.json()["cause"]
        result = click.style(cause, fg="red")
    else:
        result = click.style(resp.text, fg="green")
    click.secho("Shutting Down Simulation {}.....".format(sim_name)),
    click.echo(result)
