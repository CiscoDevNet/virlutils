import click
from virl.api import VIRLServer
from virl import helpers
from virl.generators import pyats_testbed_generator


@click.command()
@click.argument('env', default='default')
@click.option('--output', '-o', help="output File name ")
def pyats(env, **kwargs):
    """
    Generates a pyats testbed config for an environment
    """
    if kwargs.get("output"):
        # user specified output filename
        file_name = kwargs.get("output")
    else:
        # writes to <env>_testbed.yaml by default
        file_name = '{}_testbed.yaml'.format(env)

    running = helpers.check_sim_running(env)
    if running:
        sim_name = running
        server = VIRLServer()
        roster = server.get_sim_roster(sim_name)
        # sim_name = "topology-fpyHFs"
        virl_data = server.export(sim_name, ip=True).content
        interfaces = server.get_interfaces(sim_name).json()
        testbed_yaml = pyats_testbed_generator(sim_name,
                                               virl_data,
                                               roster=roster,
                                               interfaces=interfaces)

        click.secho("Writing {}".format(file_name))
        with open(file_name, 'w') as yaml_file:
            yaml_file.write(testbed_yaml)

    else:
        click.secho("couldnt generate testbed for for env: {}".format(env),
                    fg='red')
