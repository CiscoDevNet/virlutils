import click
from subprocess import call
from virl.api import VIRLServer
from virl.helpers import generate_sim_id, check_sim_running, store_sim_info
import os


@click.command()
@click.argument('repo', default='default')
@click.option('-e', default='default', help="environment name", required=False)
@click.option('-f', default='topology.virl', help='filename', required=False)
def up(repo=None, **kwargs):
    """
    start a virl simulation
    """
    fname = kwargs['f']
    env = kwargs['e']

    if os.path.exists(fname):
        running = check_sim_running(env)
        if not running:
            click.secho('Creating {} environment from {}'.format(env, fname))
            with open(fname) as fh:
                data = fh.read()
            server = VIRLServer()

            # we can expose fairly aribtary substitutions here...
            # anything that may differ usually related to networking....
            # <dirty hack>
            subs = {
                "{{ gateway }}": server.get_gateway_for_network('flat'),
                "{{ flat1_gateway}}": server.get_gateway_for_network('flat1'),
                "{{ dns_server }}": server.get_dns_server_for_network('flat'),
            }

            # also can change some VIRL/ANK defaults
            subs["rsa modulus 768"] = "rsa modulus 1024"

            for tag, value in subs.items():
                if tag in data:
                    if value:
                        # split off the braces
                        humanize = tag
                        click.secho("Localizing {} with: {}".format(humanize,
                                                                    value))
                        data = data.replace(tag, value)

            # </dirty hack>

            dirpath = os.getcwd()
            foldername = os.path.basename(dirpath)
            sim_name = "{}_{}_{}".format(foldername, env, generate_sim_id())
            resp = server.launch_simulation(sim_name, data)
            store_sim_info(resp.text, env=env)  # 'topology-2lkx2'
        else:
            click.secho('Sim {} already running'.format(running))
    else:
        # try to pull from virlfiles
        if repo:
            call(['virl', 'pull', repo])
            call(['virl', 'up'])
        else:
            click.secho('Could not find topology.virl. Maybe try -f', fg="red")
