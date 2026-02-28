import webbrowser

import click

from virl.api import VIRLServer


@click.command()
def cockpit():
    """
    opens the Cockpit UI
    """
    server = VIRLServer()
    url = "https://{}:9090".format(server.host)
    webbrowser.open(url)
