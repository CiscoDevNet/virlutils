import click
from virl.api import VIRLServer
from virl.helpers import get_cml_client


@click.command()
@click.option(
    "--token", "-t", required=True, help="Smart License token for registration",
)
@click.option(
    "--reregister/--no-reregister",
    "--force/--no-force",
    required=False,
    default=False,
    help="force registration even if already registered",
)
@click.option("--smart-license-server", "-s", required=False, help="URL for the Smart License server or satellite")
@click.option("--proxy-host", "-p", required=False, help="Hostname or IP address of proxy to use for registration (if required)")
@click.option("--proxy-port", "-o", required=False, default=80, help="Port number to use for proxy host (default: 80)")
def register(token, **kwargs):
    """
    register with a Smart License account
    """
    ssms = kwargs["smart_license_server"]
    proxy = kwargs["proxy_host"]
    port = kwargs["proxy_port"]
    force = kwargs["reregister"]
    server = VIRLServer()
    client = get_cml_client(server)

    # As of 2.0.0b5 of virl2-client, there is no Python API for licensing.  So we use
    # the library as much as we can, and use requests for the rest.

    # Offer the config for SL gateway and proxy.  This is kind of a layer violation, but it may be okay for those that
    # would want to use this interface.
    if ssms or proxy:
        try:
            payload = {}
            if ssms:
                payload["ssms"] = ssms

            if proxy:
                payload["proxy"] = {"server": proxy, "port": port}
            response = client.session.put(click._base_url + "licensing/transport", json=payload)
            response.raise_for_status()
        except Exception as e:
            click.secho("Failed to configure Smart License server and proxy: {}".format(e), fg="red")
            exit(1)

    payload = {"token": token}
    if force:
        payload["reregister"] = True

    try:
        response = client.session.post(client._base_url + "licensing/registration", json=payload)
        response.raise_for_status()
    except Exception as e:
        click.secho("Failed to register with Smart Licensing: {}".format(e), fg="red")
        exit(1)
