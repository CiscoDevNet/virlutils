import click
from virl.api import ViewerPlugin, NoPluginError
from virl.api.github import get_repos
from virl.cli.views.search import repo_table


@click.command()
@click.argument("query", required=False)
@click.option("--org", default="virlfiles", required=False, help="GitHub organization to search (default: virlfiles)")
def search(query=None, **kwargs):
    """
    list topologies available via github
    """

    repos = get_repos(org=kwargs["org"], query=query)
    if query is not None:
        click.secho("Displaying {} Results For {}".format(len(repos), query))
    else:
        click.secho("Displaying {} Results".format(len(repos)))
    try:
        pl = ViewerPlugin(viewer="search")
        pl.visualize(repos=repos)
    except NoPluginError:
        repo_table(repos)
