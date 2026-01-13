import click
from virl2_client.models.cl_pyats import (ClPyats, PyatsDeviceNotFound,
                                          PyatsNotInstalled)

from virl.api import VIRLServer
from virl.helpers import (get_cml_client, get_current_lab,
                          safe_join_existing_lab)


@click.command()
@click.argument("node", nargs=1)
@click.argument("command", nargs=1)
@click.option("--config/--no-config", default=False, show_default=False, help="Command is a configuration command (default: False)")
def command(node, command, config, **kwargs):
    """
    send a command or config to a node (requires pyATS)
    """
    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            pylab = None
            pyats_username = server.config.get("CML_DEVICE_USERNAME")
            pyats_password = server.config.get("CML_DEVICE_PASSWORD")
            pyats_auth_password = server.config.get("CML_DEVICE_ENABLE_PASSWORD")

            try:
                pylab = ClPyats(lab)
                pylab.sync_testbed(server.user, server.passwd)
            except PyatsNotInstalled:
                click.secho("pyATS is not installed, run 'pip install pyats'", fg="red")
                exit(1)

            for device in pylab._testbed.devices.values():
                if device.name != "terminal_server":
                    device.credentials.default.username = pyats_username or "cisco"
                    device.credentials.default.password = pyats_password or "cisco"
                    device.credentials.enable.password = pyats_auth_password or "cisco"

            try:
                result = ""
                if config:
                    result = pylab.run_config_command(node, command)
                else:
                    result = pylab.run_command(node, command)

                click.secho(result)
            except PyatsDeviceNotFound:
                click.secho("Node '{}' is not supported by pyATS".format(node), fg="yellow")
            except Exception as e:
                click.secho("Failed to run '{}' on '{}': {}".format(command, node, e))
                exit(1)
        else:
            click.secho("Unable to find lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("No current lab set", fg="red")
        exit(1)
