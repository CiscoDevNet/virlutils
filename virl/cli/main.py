import click
import os
from subprocess import call
from virl.api import VIRLServer
from views import sim_list_table
import random
import string

from .console.commands import console
from .nodes.commands import nodes

SERVER = VIRLServer()

def id():
    return '-' + ''.join(random.choice(string.letters + string.digits) for _ in range(6))

@click.group()
def virl():
    pass

virl.add_command(console)
virl.add_command(nodes)

@virl.command()
def up(**kwargs):
    """
    start a virl simulation
    """
    if os.path.exists('topology.virl'):
        print ('Launching Simulation from topology.virl')
        with open('topology.virl') as fh:
            data = fh.read()
        server = VIRLServer()
        dirpath = os.getcwd()
        foldername = os.path.basename(dirpath)
        sim_name = foldername + id()
        resp = server.launch_simulation(sim_name, data)
        print(resp.text)
    else:
        print('Could not find virl file')

@virl.command()
def ls(**kwargs):
    """
    lists running simulations
    """
    server = VIRLServer()
    sim_dict = server.list_simulations()
    sim_list_table(sim_dict)

@click.argument('sim_name')
@virl.command()
def down(sim_name, **kwargs):
    """
    stop a virl simulation
    """
    server = VIRLServer()
    resp = server.stop_simulation(sim_name)
    print("Shutting Down Simulation {}.....".format(sim_name)),
    click.echo(resp.text)



if __name__ == '__main__':
    simengine_host = os.getenv("VIRL_HOST")
    virl_user = os.getenv("VIRL_USER")
    virl_password = os.getenv("VIRL_PASSWORD")

    if not all([simengine_host, virl_user, virl_password]):
        simengine_host = raw_input("Enter VIRL hostname/IP: ")

    cli()
