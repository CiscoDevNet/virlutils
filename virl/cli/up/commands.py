import click

from virl.api import VIRLServer

@click.command()
def up(**kwargs):
    """
    start a virl simulation
    """
    if os.path.exists('topology.virl'):
        click.secho('Launching Simulation from topology.virl', fg='green')
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
