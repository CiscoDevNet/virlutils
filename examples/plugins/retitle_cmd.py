from virl.api import CommandPlugin
import click
from virl.api import VIRLServer
from virl.helpers import get_cml_client, get_current_lab, safe_join_existing_lab


class RetitleCommand(CommandPlugin, command="retitle"):
    @staticmethod
    @click.command()
    @click.option("--new-title", "-n", required=True, help="New title for the lab")
    def run(new_title):
        """
        re-title the current lab
        """

        server = VIRLServer()
        client = get_cml_client(server)

        clab = get_current_lab()

        if not clab:
            click.secho("Current lab is not set", fg="red")
            exit(1)

        lab = safe_join_existing_lab(clab, client)
        if lab:
            lab.title = new_title
        else:
            click.secho("Current lab {} is not present on the server".format(clab), fg="red")
            exit(1)
