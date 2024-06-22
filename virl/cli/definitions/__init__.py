import click

from virl.cli.definitions.images import images
from virl.cli.definitions.nodes import nodes


@click.group()
def definitions():
    """
    manage image and node definitions
    """
    pass


definitions.add_command(nodes)
definitions.add_command(images)
