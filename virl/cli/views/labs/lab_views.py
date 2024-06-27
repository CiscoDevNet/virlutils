# -*- coding: utf-8 -*-
import textwrap

import click
import tabulate


def lab_list_table(labs, cached_labs=None):
    click.secho("Labs on Server", fg="green")
    print_labs(labs)
    if cached_labs:
        click.secho("Cached Labs", fg="yellow")
        print_labs(cached_labs)


def print_labs(labs):
    table = []
    headers = ["ID", "Title", "Description", "Owner", "Status", "Nodes", "Links", "Interfaces"]
    for lab in labs:
        lab_details = lab.details()
        tr = []
        tr.append(lab_details["owner_username"])
        tr.append(lab_details["lab_title"])
        wrapped_description = textwrap.fill(lab_details["lab_description"], width=40)
        tr.append(wrapped_description)
        tr.append(lab_details["owner_username"])
        status = lab_details["state"]
        if status in {"BOOTED", "STARTED"}:
            color = "green"
        elif status in {"QUEUED"}:
            color = "yellow"
        else:
            color = "red"
        tr.append(click.style(status, fg=color))
        tr.append(lab_details["node_count"])
        tr.append(lab_details["link_count"])
        stats = lab.statistics
        tr.append(stats["interfaces"])
        table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
