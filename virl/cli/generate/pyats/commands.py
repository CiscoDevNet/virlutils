import click

from virl.api import VIRLServer
from virl.generators import pyats_testbed_generator
from virl.helpers import (get_cml_client, get_current_lab,
                          safe_join_existing_lab)


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
