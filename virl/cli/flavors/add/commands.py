import click
from virl.api import VIRLServer
from requests.exceptions import HTTPError


@click.command()
@click.argument('flavor')
@click.option('--memory', default='2048')
@click.option('--vcpus', default='1')
def add(**kwargs):
    """
    add a specific flavor
    """

    flavor = kwargs.get('flavor')
    memory = kwargs.get('memory')
    vcpus = kwargs.get('vcpus')
    server = VIRLServer(port=80)

    # Attempt to delete the flavor
    try:
        r = server.add_flavor(flavor=flavor, memory=memory, vcpus=vcpus)
        print("Flavor '{}' ({}) added.".format(flavor, r['id']))

    except HTTPError as err:
        print("\nFailed to create flavor '{}':".format(flavor))
        print("\n\t{}\n".format(err.response.reason))
