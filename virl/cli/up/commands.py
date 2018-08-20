import click
from subprocess import call
from virl.api import VIRLServer
from virl.helpers import generate_sim_id, check_sim_running, store_sim_info
import os
import time


@click.command()
@click.argument('repo', default='default')
@click.option('-e', default='default', help="environment name", required=False)
@click.option('-f', default='topology.virl', help=' \
VIRL file to launch, defaults to topology.virl', required=False)
@click.option('--provision/--noprovision', show_default=False, default=False,
              help=" \
Blocks execution until all nodes are reachable.", required=False)
@click.option('--wait-time', default=10,
              help="max time (in minutes) to wait for nodes to come online",
              show_default=True)
def up(repo=None, provision=False, **kwargs):
    """
    start a virl simulation
    """
    fname = kwargs['f']
    env = kwargs['e']
    wait_time = kwargs['wait_time']

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
                "{{ flat1_gateway }}": server.get_gateway_for_network('flat1'),
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

            if provision:
                nodes = server.get_node_list(sim_name)
                msg = "Waiting {} minutes for nodes to come online...."
                msg = msg.format(wait_time)
                click.secho(msg)
                maxtime = time.time() + 60 * int(wait_time)
                with click.progressbar(nodes) as all_nodes:
                    for node in all_nodes:
                        if time.time() > maxtime:
                            click.secho("")
                            click.secho("Max time expired", fg="red")
                            click.secho("All nodes may not be online",
                                        fg="red")
                            break
                        node_online = False
                        while not node_online:
                            if time.time() > maxtime:
                                break
                            time.sleep(20)
                            node_online = server.check_node_reachable(sim_name,
                                                                      node)
        else:
            click.secho('Sim {} already running'.format(running))
    else:
        # try to pull from virlfiles
        if repo:
            call(['virl', 'pull', repo])
            call(['virl', 'up'])
        else:
            click.secho('Could not find topology.virl. Maybe try -f', fg="red")
