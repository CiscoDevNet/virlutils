import os

import click

from virl.api import CachedLab, NoPluginError, ViewerPlugin, VIRLServer
from virl.cli.views import lab_list_table
from virl.helpers import get_cache_root, get_cml_client


@click.command()
@click.option(
    "--all/--server",
    default=False,
    show_default=False,
    required=False,
    help="Display cached labs in addition to those on the server (default: server labs only)",
)
@click.option(
    "--all-users/--only-me",
    default=False,
    show_default=False,
    required=False,
    help="Display labs for all users (only if current user is an admin) (default: only show labs owned by me)",
)
def ls(all, all_users):
    """
    lists running labs and optionally those in the cache
    """
    server = VIRLServer()
    client = get_cml_client(server)
    labs = []
    cached_labs = None
    users = client.user_management.users()
    ownerids_usernames = {u["id"]: u["username"] for u in users}

    lab_ids = client.get_lab_list(all_users)
    for id in lab_ids:
        labs.append(client.join_existing_lab(id))

    if all:
        cached_labs = []
        cache_root = get_cache_root()
        if os.path.isdir(cache_root):
            for f in os.listdir(cache_root):
                lab_id = f
                cached_labs.append(CachedLab(lab_id, cache_root + "/" + f))

    try:
        pl = ViewerPlugin(viewer="lab")
        pl.visualize(labs=labs, ownerids_usernames=ownerids_usernames, cached_labs=cached_labs)
    except NoPluginError:
        lab_list_table(labs, ownerids_usernames, cached_labs=cached_labs)
