import os

import click
import libtmux

from virl.api import VIRLServer
from virl.helpers import (get_cml_client, get_current_lab,
                          safe_join_existing_lab)


def connect_tmux(session_title, node_console_cmd, group):
    tmux_server = libtmux.server.Server()
    session = tmux_server.new_session(session_name=session_title, kill_session=True)
    if group == "panes":
        window = session.windows[0]
        panes_len = len(window.panes)
        for node_obj, cmd in node_console_cmd:
            label = node_obj.label
            if panes_len == 1:
                panes_len += 1
                pane = window.panes[0]
            else:
                pane = window.split_window()
            pane.send_keys("printf '\\033]2;%s\\033\\\\' '{}'".format(label), suppress_history=True)
            pane.send_keys(cmd, suppress_history=True)
            window.select_layout("tiled")

    if group == "windows":
        windows_len = len(session.windows)
        for node_obj, cmd in node_console_cmd:
            label = node_obj.label
            if windows_len == 1:
                windows_len += 1
                window = session.windows[0]
                window.cmd("rename-window", label)
            else:
                window = session.new_window(window_name=label)
            pane = window.panes[0]
            pane.send_keys(cmd, suppress_history=True)

    if "TMUX" in os.environ:
        session.switch_client()
    else:
        session.attach_session()


@click.command(help="console to all nodes using tmux")
@click.option(
    "--group",
    type=click.Choice(("panes", "windows")),
    default="panes",
    show_default=True,
    help="'panes': group all nodes in one window, 'windows': one node per window",
)
def tmux(group):
    """
    console to all devices in the lab with tmux
    """
    server = VIRLServer()
    client = get_cml_client(server)
    skip_types = ["external_connector", "unmanaged_switch"]

    node_console_cmd = []
    current_lab = get_current_lab()
    if current_lab:
        lab = safe_join_existing_lab(current_lab, client)
        if lab:
            for node_obj in lab.nodes():
                if node_obj.node_definition in skip_types or not node_obj.is_active():
                    continue
                if len(lab.id) == 6:
                    # Old-style (CML 2.2) lab IDs; console uses lab_id/node_id
                    console = "/{}/{}/0".format(lab.id, node_obj.id)
                else:
                    # From CML 2.3, console uses lab_title/node_label
                    console = "/{}/{}/0".format(lab.title, node_obj.label)
                # use user specified ssh command
                if "CML_CONSOLE_COMMAND" in server.config:
                    cmd = server.config["CML_CONSOLE_COMMAND"]
                    cmd = cmd.format(host=server.host, user=server.user, console="open " + console)
                    print("Calling user specified command: {}".format(cmd))
                else:
                    cmd = "ssh -t {}@{} open {}".format(server.user, server.host, console)
                node_console_cmd.append((node_obj, cmd))

            if node_console_cmd:
                session_title = "{}-{}".format(str(lab.title).replace(".", "_").replace(":", "_"), lab.id[:4])
                connect_tmux(session_title, node_console_cmd, group)
            else:
                click.secho("Unable to find any valid nodes", fg="red")
                exit(1)
        else:
            click.secho("Unable to find lab {}".format(current_lab), fg="red")
            exit(1)
    else:
        click.secho("No current lab set", fg="red")
        exit(1)
