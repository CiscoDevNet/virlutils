import click
from virl.api import VIRLServer
from virl.cli.views import sync_table
from virl import helpers
from virl.helpers import get_cml_client, safe_join_existing_lab, get_current_lab
from virl.generators import nso_payload_generator1, nso_payload_generator
from virl.api.nso import NSO


@click.command()
@click.option("--output", "-o", help="just dump the payload to file without sending")
@click.option("--syncfrom/--no-syncfrom", default=False, help="Perform sync-from after updating devices")
def nso(syncfrom, **kwargs):
    """
    generate nso inventory
    """

    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:

            if kwargs.get("output"):
                file_name = kwargs.get("output")
            else:
                file_name = None

            inv = nso_payload_generator(lab, server)

            if inv:
                if file_name:
                    click.secho("Writing {}".format(file_name))
                    with open(file_name, "w") as fd:
                        fd.write(inv)
                else:
                    click.secho("Updating NSO....")
                    nso_obj = NSO()
                    nso_response = nso_obj.update_devices(inv)
                    if nso_response.ok:
                        click.secho("Successfully added CML devices to NSO")
                    else:
                        click.secho("Error updating NSO: ", fg="red")
                        click.secho(nso_response.text)
                    if syncfrom:
                        resp = nso_obj.perform_sync_from()
                        sync_table(resp.json())
            else:
                click.secho("Failed to get inventory data", fg="red")
                exit(1)
        else:
            click.secho("Failed to find running lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("Current lab is not set", fg="red")
        exit(1)


@click.command()
@click.argument("env", default="default")
@click.option("--output", "-o", help="just dump the payload to file without sending")
@click.option("--syncfrom/--no-syncfrom", default=False, help="Perform sync-from after updating devices")
# @click.option('--syncto/--no-syncto', default=False,
#               help="Perform sync-to afgter updating devices")
def nso1(env, syncfrom, **kwargs):
    """
    generate nso inventory
    """

    if kwargs.get("output"):
        # user specified output filename
        file_name = kwargs.get("output")
    else:
        # writes to <env>.json by default
        file_name = None

    running = helpers.check_sim_running(env)
    if running:
        sim_name = running
        server = VIRLServer()
        roster = server.get_sim_roster(sim_name)
        # sim_name = "topology-fpyHFs"
        virl_data = server.export(sim_name, ip=True).content
        interfaces = server.get_interfaces(sim_name).json()

        payload = nso_payload_generator1(sim_name, virl_data, roster=roster, interfaces=interfaces)

        if file_name:  # pragma: no cover
            click.secho("Writing payload to {}".format(file_name))
            with open(file_name, "w") as payload_file:

                payload_file.write(payload)
        else:
            click.secho("Updating NSO....")
            nso_obj = NSO()
            nso_response = nso_obj.update_devices(payload)
            if nso_response.ok:
                click.secho("Successfully added VIRL devices to NSO")
            else:
                click.secho("Error updating NSO: ", fg="red")
                click.secho(nso_response.text)
            if syncfrom:
                resp = nso_obj.perform_sync_from()
                sync_table(resp.json())

    else:
        click.secho("couldnt generate testbed for for env: {}".format(env), fg="red")
