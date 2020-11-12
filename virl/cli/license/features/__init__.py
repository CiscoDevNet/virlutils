import click
from virl.cli.license.features.show.commands import show as showc
from virl.cli.license.features.update.commands import update as updatec


@click.group()
def features():
    """
    work with licensed features
    """
    pass


features.add_command(showc, name="show")
features.add_command(updatec, name="update")
