import click

from virl.cli.cluster.info.commands import info


@click.group()
def cluster():
    """
    display and manage CML cluster details
    """
    pass


cluster.add_command(info)
