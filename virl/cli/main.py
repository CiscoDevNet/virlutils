import click
import os
from subprocess import call
from virl.api import VIRLServer

from .console.commands import console
from .nodes.commands import nodes
from .logs.commands import logs
from .up.commands import up
from .down.commands import down
from .ls.commands import ls
from .save.commands import save
from .telnet.commands import telnet
from .ssh.commands import ssh
from .generate import generate

@click.group()
def virl():
    pass

virl.add_command(console)
virl.add_command(nodes)
virl.add_command(logs)
virl.add_command(up)
virl.add_command(down)
virl.add_command(ls)
virl.add_command(save)
virl.add_command(telnet)
virl.add_command(ssh)
virl.add_command(generate)


if __name__ == '__main__':
    simengine_host = os.getenv("VIRL_HOST")
    virl_user = os.getenv("VIRL_USER")
    virl_password = os.getenv("VIRL_PASSWORD")

    if not all([simengine_host, virl_user, virl_password]):
        simengine_host = raw_input("Enter VIRL hostname/IP: ")

    cli()
