import click
from virl.api import VIRLServer
from virl import helpers
from virl.helpers import get_cml_client, get_current_lab, safe_join_existing_lab
from virl.generators import pyats_testbed_generator1, pyats_testbed_generator


@click.command()
@click.option("--output", "-o", help="output File name")
def pyats(**kwargs):
    """
    generates a pyats testbed config for a lab
    """
    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            if kwargs.get("output"):
                # user specified output filename
                file_name = kwargs.get("output")
            else:
                # writes to <lab.id>_testbed.yaml by default
                file_name = "{}_testbed.yaml".format(lab.id)

            testbed = pyats_testbed_generator(lab)

            if testbed:
                click.secho("Writing {}".format(file_name))
                with open(file_name, "w") as fd:
                    fd.write(testbed)
            else:
                click.secho("Failed to get testbed data", fg="red")
                exit(1)
        else:
            click.secho("Failed to find running lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("Current lab is not set", fg="red")
        exit(1)


@click.command()
@click.argument("env", default="default")
@click.option("--output", "-o", help="output File name ")
def pyats1(env, **kwargs):
    """
    Generates a pyats testbed config for an environment
    """
    if kwargs.get("output"):
        # user specified output filename
        file_name = kwargs.get("output")
    else:
        # writes to <env>_testbed.yaml by default
        file_name = "{}_testbed.yaml".format(env)

    running = helpers.check_sim_running(env)
    if running:
        sim_name = running
        server = VIRLServer()
        roster = server.get_sim_roster(sim_name)
        # sim_name = "topology-fpyHFs"
        virl_data = server.export(sim_name, ip=True).content
        interfaces = server.get_interfaces(sim_name).json()
        testbed_yaml = pyats_testbed_generator1(sim_name, virl_data, roster=roster, interfaces=interfaces)

        click.secho("Writing {}".format(file_name))
        with open(file_name, "w") as yaml_file:
            yaml_file.write(testbed_yaml)

    else:
        click.secho("couldnt generate testbed for for env: {}".format(env), fg="red")
