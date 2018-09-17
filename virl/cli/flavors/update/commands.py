import click
from virl.api import VIRLServer
from requests.exceptions import HTTPError


@click.command()
@click.argument('flavor')
@click.option('--memory', default=None)
@click.option('--vcpus', default=None)
@click.option('--name', default=None)
def update(**kwargs):
    """
    update a specific flavor
    """

    flavor = kwargs.get('flavor')
    memory = kwargs.get('memory')
    vcpus = kwargs.get('vcpus')
    name = kwargs.get('name')
    server = VIRLServer(port=80)

    # Does the flavor exist?
    try:
        id = server.get_flavor_id(flavor)
        r = server.get_flavors(id)
    except HTTPError as err:
        print("\nFailed to locate flavor '{}':".format(flavor))
        print("\n\t{}".format(err.response.reason))
        return

    f = r

    if not memory:
        memory = f['ram']

    if not vcpus:
        vcpus = f['vcpus']

    if not name:
        name = f['name']

    r = server.delete_flavor(flavor)
    r = server.add_flavor(flavor=name,
                          memory=memory,
                          vcpus=vcpus)

    print("Original Flavor")
    print("\t   ID: {}".format(f['id']))
    print("\t Name: {}".format(f['name']))
    print("\t  RAM: {}".format(f['ram']))
    print("\tVCPUS: {}".format(f['vcpus']))

    print("New Flavor")
    print("\t   ID: {}".format(r['id']))
    print("\t Name: {}".format(r['name']))
    print("\t  RAM: {}".format(r['ram']))
    print("\tVCPUS: {}".format(r['vcpus']))
