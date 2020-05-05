import click
from virl.api import VIRLServer
from virl.helpers import (
    check_sim_running,
    remove_sim_info,
    get_cml_client,
    check_lab_active,
    get_lab_id,
    check_lab_server,
    clear_current_lab,
    get_current_lab,
)


@click.command()
@click.option("--id", required=False, help="An existing CML lab ID to stop (lab-name is ignored)")
@click.option("--lab-name", "-n", "--sim-name", required=False, help="An existing CML lab name to stop")
def down(id=None, lab_name=None, **kwargs):
    """
    stop a CML lab
    """
    server = VIRLServer()
    client = get_cml_client(server)

    lab = None

    if id:
        if check_lab_server(id, client):
            lab = client.join_existing_lab(id)

    if not lab and lab_name:
        lab = get_lab_id(lab_name, client)

    if not lab:
        try:
            lab_id = get_current_lab()
            if lab_id:
                if check_lab_server(lab_id, client):
                    lab = client.join_existing_lab(lab_id)
        except Exception as e:
            click.secho("Failed to read current lab: {}".format(e), fg="red")

    if lab:
        if check_lab_active(lab):
            lab.stop()
            msg = clear_current_lab(lab)
            if msg:
                click.secho("Failed to clear current lab: {}".format(msg), fg="yellow")
        else:
            click.secho("Lab with ID {} and title {} is already stopped".format(lab.id, lab.title))

    else:
        click.secho("Failed to find lab on server", fg="red")


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
