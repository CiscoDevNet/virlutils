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
    cached_labs = None
    labs = client.all_labs(show_all=all_users)

    if all:
        cached_labs = []
        cache_root = get_cache_root()
        if os.path.isdir(cache_root):
            for f in os.listdir(cache_root):
                lab_id = f
                cached_labs.append(CachedLab(lab_id, cache_root + "/" + f))

    try:
        pl = ViewerPlugin(viewer="lab")
        pl.visualize(labs=labs, cached_labs=cached_labs)
    except NoPluginError:
        lab_list_table(labs, cached_labs)
