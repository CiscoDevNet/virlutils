import click
from virl.cli.license.features.show.commands import show
from virl.cli.license.features.update.commands import update


@click.group()
def features():
    """
    work with licensed features
    """
    pass


features.add_command(show)
features.add_command(update)
