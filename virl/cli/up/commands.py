import os
import time
from subprocess import call

import click

from virl.api import CachedLab, VIRLServer
from virl.helpers import (
    cache_lab,
    check_lab_cache,
    clear_current_lab,
    get_cml_client,
    get_command,
    get_current_lab,
    safe_join_existing_lab,
    safe_join_existing_lab_by_title,
    set_current_lab,
)


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


def _build_command(cmd, provision, start, **kwargs):
    if kwargs["f"]:
        cmd += ["-f", kwargs["f"]]
    if provision:
        cmd.append("--provision")
    else:
        cmd.append("--noprovision")
    if start:
        cmd.append("--start")
    else:
        cmd.append("--no-start")
    if kwargs["id"]:
        cmd += ["--id", kwargs["id"]]
    if kwargs["lab_name"]:
        cmd += ["--lab-name", kwargs["lab_name"]]

    return cmd


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
            (lfname, lfext) = os.path.splitext(fname)
            if lfext.lower() == ".unl":
                # This is an EVE-NG lab.  Convert it if we can.
                rc = -1
                try:
                    rc = call(["eve2cml", fname])
                except FileNotFoundError:
                    pass

                if rc != 0:
                    click.secho(
                        "ERROR: Failed to convert {} from EVE-NG to CML.  Is https://pypi.org/project/eve2cml/ installed?".format(fname),
                        fg="red",
                    )
                    exit(rc)

                fname = "{}.yaml".format(lfname)

            lname = get_lab_title(fname)
            click.secho("Importing lab {} from file {}".format(lname, fname))
            lab = client.import_lab_from_path(fname, title=lname)
        elif not lab:
            # try to pull from virlfiles
            if repo:
                cmd = [get_command(), "pull", repo]
                if kwargs["f"]:
                    cmd += ["--file", kwargs["f"]]

                rc = call(cmd)
                if rc == 0:
                    cmd = [get_command(), "up"]
                    cmd = _build_command(cmd, provision, start, **kwargs)

                    exit(call(cmd))

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
