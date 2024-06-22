import click

from virl.api import VIRLServer
from virl.helpers import (get_cml_client, get_current_lab,
                          safe_join_existing_lab)


@click.command()
@click.option("--force/--no-force", "-f", default=False, required=False, help="Stop a lab (if it's started) then wipe it (default: False)")
@click.option(
    "--confirm/--no-confirm",
    show_default=False,
    default=True,
    help="Do not prompt for confirmation (default: prompt)",
    required=False,
)
def lab(force, confirm):
    """
    wipe a lab
    """
    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            active = lab.is_active()
            if active and force:
                lab.stop(wait=True)

            # Check again just to be sure.
            if not lab.is_active():
                ret = "y"
                if confirm:
                    ret = input("Are you sure you want to wipe lab {} (ID: {}) [y/N]? ".format(lab.title, current_lab))
                if ret.lower().startswith("y"):
                    lab.wipe(wait=True)
                    click.secho("Lab {} (ID: {}) wiped".format(lab.title, current_lab))
                else:
                    click.secho("Not wiping lab {} (ID: {})".format(lab.title, current_lab))

            else:
                click.secho("Lab {} (ID: {}) is active; either down it or use --force".format(lab.title, current_lab), fg="red")
                exit(1)
        else:
            click.secho("Unable to find lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("Current lab is not set", fg="red")
        exit(1)
