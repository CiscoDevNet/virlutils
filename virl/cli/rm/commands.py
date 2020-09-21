import click
import os
from virl.api import VIRLServer
from virl.helpers import get_cml_client, safe_join_existing_lab, get_current_lab, check_lab_cache, clear_current_lab


@click.command()
@click.option(
    "--force/--no-force",
    "-f",
    default=False,
    required=False,
    help="Stop and/or wipe a lab (if it's started) then remove it (default: False)",
)
@click.option(
    "--confirm/--no-confirm",
    show_default=False,
    default=True,
    help="Do not prompt for confirmation (default: prompt)",
    required=False,
)
@click.option(
    "--from-cache/--no-from-cache",
    default=False,
    required=False,
    show_default=False,
    help="Remove the lab from the cache (default: do not remove from cache)",
)
def rm(force, confirm, from_cache):
    """
    remove a lab
    """
    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            if lab.is_active() and force:
                lab.stop(wait=True)

            if lab.state() != "DEFINED_ON_CORE" and force:
                lab.wipe(wait=True)

            # Check again just to be sure.
            if lab.state() == "DEFINED_ON_CORE":
                ret = "y"
                if confirm:
                    ret = input("Are you sure you want to remove lab {} (ID: {}) [y/N]? ".format(lab.title, current_lab))
                if ret.lower().startswith("y"):
                    # We need to save the lab's title before we remove it.
                    title = lab.title
                    lab.remove()
                    click.secho("Lab {} (ID: {}) removed".format(title, current_lab))
                    if from_cache:
                        try:
                            os.remove(check_lab_cache(current_lab))
                        except OSError:
                            # File doesn't exist.
                            pass

                        click.secho("Removed lab {} from cache".format(current_lab))
                    clear_current_lab()
                else:
                    click.secho("Not removing lab {} (ID: {})".format(lab.title, current_lab))

            else:
                click.secho(
                    "Lab {} (ID: {}) is either active or not wiped; either down and wipe it or use --force".format(lab.title, current_lab),
                    fg="red",
                )
                exit(1)
        else:
            click.secho("Unable to find lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("Current lab is not set", fg="red")
        exit(1)
