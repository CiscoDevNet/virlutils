import click
from virl.api import VIRLServer
from requests.exceptions import HTTPError


@click.command()
@click.argument('image')
def delete(**kwargs):
    """
    delete a specific flavor
    """

    flavor = kwargs.get('image')
    server = VIRLServer(port=80)

    # Attempt to delete the flavor
    try:
        r = server.delete_flavor(flavor)
        print("Flavor '{}' deleted.".format(r['name']))
    except IndexError as ierr:
        print(ierr)
    except HTTPError as herr:
        print("\nFailed to delete flavor '{}':".format(flavor))
        print("\n\t{}".format(herr.response.reason))
