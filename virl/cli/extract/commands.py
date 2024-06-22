import click

from virl.api import VIRLServer
from virl.helpers import (cache_lab, extract_configurations, get_cml_client,
                          get_current_lab, safe_join_existing_lab)


@click.command()
@click.option("--update-cache/--no-update-cache", default=True, help="update the local cache (default: True)")
def extract(update_cache, **kwargs):
    """
    extract configurations from all nodes in a lab
    """
    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            extract_configurations(lab)

            if update_cache:
                cache_lab(lab, force=True)
        else:
            click.secho("Failed to find running lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("Current lab is not set", fg="red")
        exit(1)
