import click

from virl.cli.license.renew.authorization.commands import \
    authorization as authorizationc
from virl.cli.license.renew.registration.commands import \
    registration as registrationc


@click.group()
def renew():
    """
    renew registration or authorization
    """
    pass


renew.add_command(registrationc, name="registration")
renew.add_command(authorizationc, name="authorization")
