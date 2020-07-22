import click
import os
from virl.api import VIRLServer

# from virl.swagger.app import app
import subprocess

PIDFILE = "/tmp/virl_swagger.pid"


@click.group()
def swagger1():
    """
    manage local swagger ui server
    """
    pass


@click.command()
@click.argument("port", default=5000)
def start1(port):
    """
    starts swagger ui for virl (mac only)
    """
    server = VIRLServer()
    os.environ["VIRL_SWAGGER_HOST"] = server.host
    os.environ["VIRL_SWAGGER_PORT"] = str(server.port)
    os.environ["VIRL_SWAGGER_USERNAME"] = server.user
    os.environ["VIRL_SWAGGER_PASSWORD"] = server.passwd
    os.environ["VIRL_SWAGGER_UI_PORT"] = str(port)

    with open("/tmp/virl_swagger.port", "w") as fh:
        fh.write(str(port))
    subprocess.Popen(["gunicorn", "-D", "virl.swagger.app:app", "-p", "/tmp/virl_swagger.pid", "-b", "127.0.0.1:{}".format(port)])

    subprocess.Popen(["open", "http://localhost:{}".format(port)])


@click.command()
@click.argument("port", default=5000)
def stop1(port):
    """
    stops swagger ui for virl (mac only)
    """
    subprocess.Popen("kill $(cat /tmp/virl_swagger.pid)", shell=True)
    portfile = "/tmp/virl_swagger.port"
    try:
        os.remove(portfile)
    except IOError:
        pass
    except OSError:
        pass


@click.command()
@click.argument("port", default=5000)
def status1(port):
    """
    show status of swagger ui for virl
    """
    pidfile = "/tmp/virl_swagger.pid"
    portfile = "/tmp/virl_swagger.port"

    if os.path.isfile(pidfile):
        with open(pidfile, "r") as fh:
            pid = fh.read()
    if os.path.isfile(portfile):
        with open(portfile, "r") as fh:
            port = fh.read()
        print("pid: {}".format(pid))
        print("VIRL swagger UI is running at http://localhost:{}".format(port))

    else:
        print("not running")


swagger1.add_command(start1, name="start")
swagger1.add_command(stop1, name="stop")
swagger1.add_command(status1, name="status")
