import click
from subprocess import call
from virl.api import VIRLServer, CachedLab
from virl.helpers import (
    generate_sim_id,
    check_sim_running,
    store_sim_info,
    get_cml_client,
    safe_join_existing_lab,
    safe_join_existing_lab_by_title,
    check_lab_cache,
    cache_lab,
    set_current_lab,
    get_current_lab,
    clear_current_lab,
    get_command,
)
import os
import time


def get_lab_title(fname):
    """
    Try and obtain a sensible title for the lab based on the filename
    and/or its contents.
    """
    # We need to do this to preserve any .virl extension to to tell CML this
    # is an older file.
    title = os.path.basename(fname)
    if not fname.lower().endswith(".virl"):
        title = os.path.splitext(fname)[0]
        # Load the lab YAML to try and extract its title property
        try:
            lab_stub = CachedLab("bogusid", fname)
        except Exception:
            # Someone may be trying to load a 1.x file without the .virl extension.
            click.secho(
                "File {} does not appear to be a YAML-formatted CML topology file."
                "If this is a CML/VIRL 1.x file, it must end with '.virl'".format(fname),
                fg="red",
            )
            exit(1)
        else:
            title = lab_stub.title

    return title


def start_lab(lab, provision=False):
    click.secho("Starting lab {} (ID: {})".format(lab.title, lab.id))
    lab.wait_for_convergence = False
    lab.start()
    cache_lab(lab)
    set_current_lab(lab.id)
    if provision:
        # Technically we need to block until all nodes are "reachable".
        # In the CML 2+ case, this means BOOTED.
        click.secho("Waiting for all nodes to be online...")
        ready = False
        while not ready:
            for n in lab.nodes():
                if not n.is_booted():
                    ready = False
                    break
                ready = True
            time.sleep(1)


@click.command()
@click.argument("repo", default="default")
@click.option(
    "-f",
    help="Lab file to launch, defaults to topology.yaml (or topology.virl if topology.yaml is not found)",
    required=False,
)
@click.option(
    "--provision/--noprovision",
    show_default=False,
    default=False,
    help="Blocks execution until all nodes are reachable (default: do not wait)",
    required=False,
)
@click.option(
    "--start/--no-start",
    show_default=False,
    default=True,
    help="Whether or not to start the lab after importing (default: start the lab)",
    required=False,
)
@click.option("--id", required=False, help="An existing lab ID to start (topology file is ignored, lab-name is ignored)")
@click.option("--lab-name", "-n", "--sim-name", required=False, help="An existing lab name to start (topology file is ignored)")
def up(repo=None, provision=False, start=True, **kwargs):
    """
    start a lab
    """
    def_fname = kwargs["f"]
    alt_fname = "topology.virl"
    fname = def_fname
    lid = kwargs["id"]
    lab_name = kwargs["lab_name"]
    lab = None
    clab = None

    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        clab = safe_join_existing_lab(current_lab, client)
        if not clab:
            click.secho("Current lab is already set to {}, but that lab is not on server; clearing it.".format(current_lab), fg="yellow")
            clear_current_lab()

    if not clab or fname or lid or lab_name:
        if clab:
            click.secho("WARNING: Current lab is set to {} (ID: {}); clearing it".format(clab.title, current_lab), fg="yellow")
            clear_current_lab()

        if not def_fname:
            def_fname = "topology.yaml"
            fname = def_fname

        if not os.path.isfile(def_fname) and os.path.isfile(alt_fname):
            fname = alt_fname

        if lid:
            lab = safe_join_existing_lab(lid, client)
            if not lab:
                # Check the cache
                existing = check_lab_cache(lid)
                if existing:
                    fname = existing

        if not lab and lab_name:
            lab = safe_join_existing_lab_by_title(lab_name, client)

        if not lab and os.path.isfile(fname):
            lname = get_lab_title(fname)
            click.secho("Importing lab {} from file {}".format(lname, fname))
            lab = client.import_lab_from_path(fname, title=lname)
        elif not lab:
            # try to pull from virlfiles
            if repo and (os.path.basename(fname) == "topology.yaml" or os.path.basename(fname) == "topology.virl"):
                rc = call([get_command(), "pull", repo])
                if rc == 0:
                    exit(call([get_command(), "up"]))

        if lab:
            if lab.is_active():
                cache_lab(lab)
                set_current_lab(lab.id)
                click.secho("Lab is already running (ID: {}, Title: {})".format(lab.id, lab.title))
            elif start:
                start_lab(lab, provision)

        else:
            click.secho("Could not find a lab to start.  Maybe try -f", fg="red")
            exit(1)
    elif clab:
        click.secho("Lab {} (ID: {}) is already set as the current lab".format(clab.title, current_lab))
        if not clab.is_active() and start:
            start_lab(clab, provision)


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
            call([get_command(), "pull", repo])
            call([get_command(), "up"])
        else:
            click.secho("Could not find topology.virl. Maybe try -f", fg="red")
