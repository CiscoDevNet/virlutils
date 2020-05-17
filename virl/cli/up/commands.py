import click
from subprocess import call
from virl.api import VIRLServer
from virl.helpers import (
    generate_sim_id,
    check_sim_running,
    store_sim_info,
    get_cml_client,
    safe_join_existing_lab,
    safe_join_existing_lab_by_title,
    check_lab_cache,
    cache_lab,
    check_lab_active,
    set_current_lab,
    get_current_lab,
    clear_current_lab,
)
import os
import time
import sys


@click.command()
@click.argument("repo", default="default")
@click.option(
    "-f",
    default="topology.yaml",
    help=" \
CML file to launch, defaults to topology.yaml (or topology.virl if topology.yaml is not found)",
    required=False,
)
@click.option(
    "--provision/--noprovision",
    show_default=False,
    default=False,
    help=" \
Blocks execution until all nodes are reachable.",
    required=False,
)
@click.option("--id", required=False, help="An existing CML lab ID to start (topology file is ignored, lab-name is ignored)")
@click.option("--lab-name", "-n", required=False, help="An existing CML lab name to start (topology file is ignored)")
def up(repo=None, provision=False, **kwargs):
    """
    start a CML lab
    """
    def_fname = kwargs["f"]
    alt_fname = "topology.virl"
    fname = def_fname
    id = kwargs["id"]
    lab_name = kwargs["lab_name"]
    lab = None

    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    clab = None
    if current_lab:
        clab = safe_join_existing_lab(current_lab, client)
        if not clab:
            click.secho("Current lab is already set to {}, but that lab is not on server; clearing it.".format(current_lab), fg="yellow")
            clear_current_lab()

    if not clab:
        if not os.path.exists(def_fname) and os.path.exists(alt_fname):
            fname = alt_fname

        if id:
            lab = safe_join_existing_lab(id, client)
            if not lab:
                # Check the cache
                existing = check_lab_cache(id)
                if existing:
                    fname = existing

        if not lab and lab_name:
            lab = safe_join_existing_lab_by_title(lab_name, client)

        if not lab and os.path.exists(fname):
            lab = client.import_lab_from_path(fname)
        elif not lab:
            # try to pull from virlfiles
            if repo:
                call([sys.argv[0], "pull", repo])
                exit(call([sys.argv[0], "up"]))

        if lab:
            # if lab.is_active():
            if check_lab_active(lab):
                cache_lab(lab)
                set_current_lab(lab.id)
                click.secho("Lab is already running (ID: {}, Title: {})".format(lab.id, lab.title))
            else:
                lab.wait_for_convergence = False
                lab.start()
                cache_lab(lab)
                set_current_lab(lab.id)
                if provision:
                    # Technically we need to block until all nodes are "reachable".
                    # In the CML 2+ case, this means BOOTED.
                    ready = False
                    while not ready:
                        for n in lab.nodes():
                            if not n.is_booted():
                                ready = False
                                break
                            ready = True
                        time.sleep(1)
        else:
            click.secho("Could not find a lab to start.  Maybe try -f", fg="red")
    else:
        click.secho("Lab {} (ID: {}) is already set as the current lab".format(clab.title, current_lab))


@click.command()
@click.argument("repo", default="default")
@click.option("-e", default="default", help="environment name", required=False)
@click.option(
    "-f",
    default="topology.virl",
    help=" \
VIRL file to launch, defaults to topology.virl",
    required=False,
)
@click.option(
    "--provision/--noprovision",
    show_default=False,
    default=False,
    help=" \
Blocks execution until all nodes are reachable.",
    required=False,
)
@click.option("--wait-time", default=10, help="max time (in minutes) to wait for nodes to come online", show_default=True)
def up1(repo=None, provision=False, **kwargs):
    """
    start a virl simulation
    """
    fname = kwargs["f"]
    env = kwargs["e"]
    wait_time = kwargs["wait_time"]

    if os.path.exists(fname):
        running = check_sim_running(env)
        if not running:
            click.secho("Creating {} environment from {}".format(env, fname))
            with open(fname) as fh:
                data = fh.read()
            server = VIRLServer()

            # we can expose fairly aribtary substitutions here...
            # anything that may differ usually related to networking....
            # <dirty hack>
            subs = {
                "{{ gateway }}": server.get_gateway_for_network("flat"),
                "{{ flat1_gateway }}": server.get_gateway_for_network("flat1"),
                "{{ dns_server }}": server.get_dns_server_for_network("flat"),
            }

            # also can change some VIRL/ANK defaults
            subs["rsa modulus 768"] = "rsa modulus 1024"

            for tag, value in subs.items():
                if tag in data:
                    if value:
                        # split off the braces
                        humanize = tag
                        click.secho("Localizing {} with: {}".format(humanize, value))
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
                            click.secho("All nodes may not be online", fg="red")
                            break
                        node_online = False
                        while not node_online:
                            if time.time() > maxtime:
                                break
                            time.sleep(20)
                            node_online = server.check_node_reachable(sim_name, node)
        else:
            click.secho("Sim {} already running".format(running))
    else:
        # try to pull from virlfiles
        if repo:
            call([sys.argv[0], "pull", repo])
            call([sys.argv[0], "up"])
        else:
            click.secho("Could not find topology.virl. Maybe try -f", fg="red")
