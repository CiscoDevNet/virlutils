import click

from virl.api import VIRLServer
from virl.generators import ansible_inventory_generator
from virl.helpers import (get_cml_client, get_current_lab,
                          safe_join_existing_lab)


@click.command()
@click.option("--output", "-o", help="output File name ")
@click.option("--style", help="output format (default is yaml)", type=click.Choice(["ini", "yaml"]))
def ansible(**kwargs):
    """
    generate ansible inventory
    """
    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            if kwargs.get("output"):
                file_name = kwargs.get("output")
            elif kwargs.get("style") == "ini":
                file_name = "{}_inventory.ini".format(lab.id)
            else:
                file_name = "{}_inventory.yaml".format(lab.id)

            inv = None

            if kwargs.get("style") == "ini":
                inv = ansible_inventory_generator(lab, server, style="ini")
            else:
                inv = ansible_inventory_generator(lab, server)

            if inv:
                click.secho("Writing {}".format(file_name))
                with open(file_name, "w") as fd:
                    fd.write(inv)
            else:
                click.secho("Failed to get inventory data", fg="red")
                exit(1)
        else:
            click.secho("Failed to find running lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("Current lab is not set", fg="red")
        exit(1)
