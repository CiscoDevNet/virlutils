import click
import os
from virl.api import VIRLServer
from virl.helpers import get_cml_client
from virl2_client.models.licensing import DEFAULT_SSMS


@click.command()
@click.option(
    "--token",
    "-t",
    required=True,
    help="Smart License token for registration",
)
@click.option(
    "--reregister/--no-reregister",
    "--force/--no-force",
    required=False,
    default=False,
    help="Force registration even if already registered",
)
@click.option("--smart-license-server", "-s", required=False, help="URL for the Smart License server or satellite")
@click.option("--proxy-host", "-p", required=False, help="Hostname or IP address of proxy to use for registration (if required)")
@click.option("--proxy-port", "-o", required=False, default=80, help="Port number to use for proxy host (default: 80)")
@click.option("--certificate", "-c", required=False, help="Path to a PEM-encoded certificate for the Smart License SSMS")
def register(token, **kwargs):
    """
    register with a Smart License account
    """
    ssms = kwargs["smart_license_server"]
    proxy = kwargs["proxy_host"]
    port = None
    cert = kwargs["certificate"]
    reregister = kwargs["reregister"]
    server = VIRLServer()
    client = get_cml_client(server)
    licensing = client.licensing

    if ssms or proxy:
        if not ssms:
            ssms = DEFAULT_SSMS
        if proxy:
            port = kwargs["proxy_port"]

        try:
            licensing.set_transport(ssms, proxy, port)
        except Exception as e:
            click.secho("Failed to configure Smart License server and proxy: {}".format(e), fg="red")
            exit(1)
    else:
        try:
            licensing.delete_certificate()
        except Exception:
            pass

        licensing.set_default_transport()

    if cert:
        if not os.path.isfile(cert):
            click.secho("Certificate {} is not a valid file!".format(cert), fg="red")
            exit(1)

        with open(cert, "r") as fd:
            contents = fd.read()
            try:
                licensing.upload_certificate(contents)
            except Exception as e:
                click.secho("Failed to upload certificate {}: {}".format(cert, e), fg="red")
                exit(1)

    try:
        licensing.register(token, reregister)
    except Exception as e:
        click.secho("Failed to register with Smart Licensing: {}".format(e), fg="red")
        exit(1)
