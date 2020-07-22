import click
from virl.api import VIRLServer
from virl.helpers import get_env_sim_name, get_cml_client, safe_join_existing_lab, get_current_lab, extract_configurations


@click.command()
@click.option("--extract/--no-extract", default=True, help="extract the configurations from devices before export (default: True)")
@click.option(
    "-f", "--filename", required=False, default="topology.yaml", metavar="<filename>", help="filename to save to, defaults to topology.yaml"
)
def save(extract, filename, **kwargs):
    """
    save lab to a local yaml file
    """
    server = VIRLServer()
    client = get_cml_client(server)

    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            if extract:
                click.secho("Extracting configurations...")
                extract_configurations(lab)

            lab_export = lab.download()

            click.secho("Writing {}".format(filename))
            with open(filename, "w") as fd:
                fd.write(lab_export)
        else:
            click.secho("Failed to find running lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("Current lab is not set", fg="red")
        exit(1)


@click.command()
@click.argument("env", default="default")
@click.option("--ip/--no-ip", default=False, help="include dynamically assigned addresses")
@click.option(
    "-f", "--filename", required=False, default="topology.virl", metavar="<filename>", help="filename to save to, defaults to topology.virl"
)
def save1(env, ip, filename, **kwargs):
    """
    save simulation to local virl file
    """
    with open(filename, "w") as fh:
        sim_name = get_env_sim_name(env)
        server = VIRLServer()
        resp = server.export(sim_name, ip=ip)
        click.secho("Saving {} to {}".format(sim_name, filename))
        fh.write(resp.text)
