import click
from virl.api import VIRLServer
from virl.cli.views import sync_table
from virl import helpers
from virl.helpers import get_cml_client, safe_join_existing_lab, get_current_lab, cache_lab_data
from virl.generators import export_generator


@click.command()
@click.option("--output", "-o", help="write the exported lab to a YAML file instead of the cache")
@click.option("--extract/--no-extract", default=True, help="extract the configurations from devices before export (default: True)")
def export(extract, **kwargs):
    """
    export the CML lab definition
    """

    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:

            if kwargs.get("output"):
                file_name = kwargs.get("output")
            else:
                file_name = None

            lab_export = export_generator(lab, extract)

            if lab_export:
                if file_name:
                    click.secho("Writing {}".format(file_name))
                    with open(file_name, "w") as fd:
                        fd.write(lab_export)
                else:
                    click.secho("Updating cache....")
                    cache_lab_data(lab.id, lab_export)
            else:
                click.secho("Failed to get lab export", fg="red")
        else:
            click.secho("Failed to find running lab {}".format(current_lab), fg="red")
    else:
        click.secho("Current lab is not set", fg="red")
