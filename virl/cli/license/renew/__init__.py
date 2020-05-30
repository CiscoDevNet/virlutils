import click
from virl.cli.license.renew.registration.commands import registration
from virl.cli.license.renew.authorization.commands import authorization


@click.group()
def renew():
    """
    renew registration or authorization
    """
    pass


renew.add_command(registration)
renew.add_command(authorization)
