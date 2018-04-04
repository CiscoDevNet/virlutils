import click
from virl.api.github import get_repos
from virl.cli.views.search import repo_table


@click.command()
@click.argument('query', required=False)
def search(query=None, **kwargs):
    """
    lists running simulations in the current project
    """

    repos = get_repos(query=query)
    click.secho("Displaying {} Results For {}".format(len(repos), query))
    repo_table(repos)
