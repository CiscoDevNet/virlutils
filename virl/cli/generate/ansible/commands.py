import click
from virl.api import VIRLServer
from virl import helpers
from virl.generators import ansible_inventory_generator


@click.command()
@click.argument('env', default='default')
@click.option('--output', '-o', help="output File name ")
@click.option('--style',
              help="output format (default is yaml)",
              type=click.Choice(['ini', 'yaml']))
def ansible(env, **kwargs):
    """
    generate ansible inventory
    """

    if kwargs.get("output"):
        # user specified output filename
        file_name = kwargs.get("output")
    elif kwargs.get("style") == "ini":
        file_name = '{}_inventory.ini'.format(env)
    else:
        # writes to <env>_testbed.yaml by default
        file_name = '{}_inventory.yaml'.format(env)

    running = helpers.check_sim_running(env)
    if running:
        sim_name = running
        server = VIRLServer()
        roster = server.get_sim_roster(sim_name)
        # sim_name = "topology-fpyHFs"
        virl_data = server.export(sim_name, ip=True).content
        interfaces = server.get_interfaces(sim_name).json()
        if kwargs.get("style") == "ini":
            inventory_ini = ansible_inventory_generator(sim_name,
                                                        virl_data,
                                                        roster=roster,
                                                        interfaces=interfaces,
                                                        style="ini")

            click.secho("Writing {}".format(file_name))
            with open(file_name, 'w') as ini_file:
                ini_file.write(inventory_ini)
        else:
            inventory_yaml = ansible_inventory_generator(sim_name,
                                                         virl_data,
                                                         roster=roster,
                                                         interfaces=interfaces)

            click.secho("Writing {}".format(file_name))
            with open(file_name, 'w') as yaml_file:
                yaml_file.write(inventory_yaml)

    else:
        click.secho("couldnt generate testbed for for env: {}".format(env),
                    fg='red')
