import click
from virl.api import VIRLServer
from virl.swagger.app import app
import subprocess


@click.argument('port', default=5000)
@click.command()
def swagger(port):
    """
    starts swagger ui for virl (mac only)
    """
    server = VIRLServer()

    app.config['VIRL_HOST'] = server.host
    app.config['VIRL_PORT'] = server.port
    app.config['VIRL_USERNAME'] = server.user
    app.config['VIRL_PASSWORD'] = server.passwd
    subprocess.Popen(['open', 'http://localhost:{}'.format(port)])
    try:
        app.run(port=int(port))
    except KeyboardInterrupt:
        exit(0)
