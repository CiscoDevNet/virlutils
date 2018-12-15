import click
from virl.api import VIRLServer
from virl.cli.views import flavor_list_table


@click.command()
@click.option('--flavor', default=None)
def ls(**kwargs):
    """
    list all flavors or the details of a specific flavor
    """

    flavor = kwargs.get('flavor')
    server = VIRLServer(port=80)

    # Regardless of the argument, we have to get all the flavors
    # In the case of no arg, we print them all.
    # In the case of an arg, we have to go back and get details.
    r = server.get_flavors()

    if flavor:
        for f in list(r):
            if f['name'] == flavor:
                flavor_list_table([f])
                break
    else:
        flavor_list_table(r)
