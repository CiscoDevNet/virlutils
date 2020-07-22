import click
from virl.cli.license.show.commands import show
from virl.cli.license.register.commands import register
from virl.cli.license.renew import renew
from virl.cli.license.deregister.commands import deregister


@click.group()
def license():
    """
    work with product licensing
    """
    pass


license.add_command(show)
license.add_command(register)
license.add_command(renew)
license.add_command(deregister)
