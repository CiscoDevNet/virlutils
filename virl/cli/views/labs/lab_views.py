# -*- coding: utf-8 -*-
import textwrap

import click
import tabulate


def lab_list_table(labs, ownerids_usernames, cached_labs=None):
    click.secho("Labs on Server", fg="green")
    print_labs(labs, ownerids_usernames)
    if cached_labs:
        click.secho("Cached Labs", fg="yellow")
        print_labs(cached_labs, ownerids_usernames)


def print_labs(labs, ownerids_usernames):
    table = list()
    headers = ["ID", "Title", "Description", "Owner", "Status", "Nodes", "Links", "Interfaces"]
    for lab in labs:
        tr = list()
        tr.append(lab.id)
        tr.append(lab.title)
        wrapped_description = textwrap.fill(lab.description, width=40)
        tr.append(wrapped_description)
        owner = ownerids_usernames.get(lab.owner, lab.owner)
        tr.append(owner)
        status = lab.state()
        stats = lab.statistics
        if status in {"BOOTED", "STARTED"}:
            color = "green"
        elif status in {"QUEUED"}:
            color = "yellow"
        else:
            color = "red"
        tr.append(click.style(status, fg=color))
        tr.append(stats["nodes"])
        tr.append(stats["links"])
        tr.append(stats["interfaces"])
        table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
