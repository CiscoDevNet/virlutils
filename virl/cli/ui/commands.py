import subprocess

import click

from virl.api import VIRLServer
from virl.helpers import (get_cml_client, get_current_lab,
                          safe_join_existing_lab)


@click.command()
def ui():
    """
    opens the Workbench for the current lab
    """
    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            url = "https://{}/lab/{}".format(server.host, current_lab)
            subprocess.Popen(["open", url])
