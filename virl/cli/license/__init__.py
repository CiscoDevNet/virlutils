import click

from virl.cli.license.deregister.commands import deregister as deregisterc
from virl.cli.license.features import features as featuresc
from virl.cli.license.register.commands import register as registerc
from virl.cli.license.renew import renew as renewc
from virl.cli.license.show.commands import show as showc


@click.group()
def license():
    """
    work with product licensing
    """
    pass


license.add_command(showc, name="show")
license.add_command(registerc, name="register")
license.add_command(renewc, name="renew")
license.add_command(deregisterc, name="deregister")
license.add_command(featuresc, name="features")
