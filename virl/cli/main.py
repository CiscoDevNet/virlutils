import click
import os
from subprocess import call
from virl.api import VIRLServer

from .console.commands import console
from .nodes.commands import nodes
from .logs.commands import logs
from .up.commands import up
from .use.commands import use
from .down.commands import down
from .ls.commands import ls
from .save.commands import save
from .telnet.commands import telnet
from .ssh.commands import ssh
from .generate import generate
from .start.commands import start
from .stop.commands import stop

@click.group()
def virl():
    pass

virl.add_command(console)
virl.add_command(nodes)
virl.add_command(logs)
virl.add_command(up)
virl.add_command(down)
virl.add_command(ls)
virl.add_command(use)
virl.add_command(save)
virl.add_command(telnet)
virl.add_command(ssh)
virl.add_command(generate)
virl.add_command(start)
virl.add_command(stop)

if __name__ == '__main__':
    cli()
