import click
import os
from virl.api import VIRLServer

@click.group()
def cli():
    pass

@cli.command()
def up(**kwargs):
    """
    start a virl simulation
    """
    pass

@cli.command()
def ls(**kwargs):
    """
    lists running simulations
    """
    server = VIRLServer()
    resp = server.list_simulations()

    print resp

@cli.command()
def down(**kwargs):
    """
    stop a virl simulation
    """
    pass

if __name__ == '__main__':
    simengine_host = os.getenv("VIRL_HOST")
    virl_user = os.getenv("VIRL_USER")
    virl_password = os.getenv("VIRL_PASSWORD")

    if not all([simengine_host, virl_user, virl_password]):
        simengine_host = raw_input("Enter VIRL hostname/IP: ")

    cli()
