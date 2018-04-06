import click
from virl.api import VIRLServer
from virl.cli.views import sync_table
from virl import helpers
from virl.generators import nso_payload_generator
from virl.api.nso import update_devices, perform_sync_from


@click.command()
@click.argument('env', default='default')
@click.option('--output', '-o',
              help="just dump the payload to file without sending")
@click.option('--syncfrom/--no-syncfrom', default=False,
              help="Perform sync-from after updating devices")
# @click.option('--syncto/--no-syncto', default=False,
#               help="Perform sync-to afgter updating devices")
def nso(env, syncfrom, **kwargs):
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

        payload = nso_payload_generator(sim_name,
                                        virl_data,
                                        roster=roster,
                                        interfaces=interfaces)

        if file_name:  # pragma: no cover
            click.secho("Writing payload to {}".format(file_name))
            with open(file_name, 'w') as payload_file:

                payload_file.write(payload)
        else:
            click.secho("Updating NSO....")
            nso_response = update_devices(payload)
            if nso_response.ok:
                click.secho("Successfully added VIRL devices to NSO")
            else:
                click.secho("Error updating NSO: ", fg='red')
                click.secho(nso_response.text)
            if syncfrom:
                resp = perform_sync_from()
                sync_table(resp.json())

    else:
        click.secho("couldnt generate testbed for for env: {}".format(env),
                    fg='red')
