import click
from virl.api.github import get_repos
from virl.cli.views.search import repo_table


@click.command()
@click.argument('query', required=False)
def search(query=None, **kwargs):
    """
    lists virl topologies available via github
    """

    repos = get_repos(query=query)
    if query is not None:
        click.secho("Displaying {} Results For {}".format(len(repos), query))
    else:
        click.secho("Displaying {} Results".format(len(repos)))
    repo_table(repos)
