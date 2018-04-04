import click
from virl.api import VIRLServer
from virl.helpers import get_env_sim_name


@click.command()
@click.argument('env', default='default')
@click.option('--ip/--no-ip',
              default=False,
              help="include dynamically assigned addresses")
@click.option('-f', '--filename',
              required=False,
              default='topology.virl',
              metavar='<filename>',
              help="filename to save to, defaults to topology.virl")
def save(env, ip, filename, **kwargs):
    """
    save simulation to local virl file
    """
    with open(filename, 'w') as fh:
        sim_name = get_env_sim_name(env)
        server = VIRLServer()
        resp = server.export(sim_name, ip=ip)
        click.secho("Saving {} to {}".format(sim_name, filename))
        fh.write(resp.text)
