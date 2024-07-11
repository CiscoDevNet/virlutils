# -*- coding: utf-8 -*-
import textwrap

import click
import tabulate


def group_list_table(groups, verbose=False):
    click.secho("Groups on Server", fg="green")
    table = []

    headers = ["ID"] if verbose else []
    headers.extend(["Name", "Description", "Users", "Labs"])
    for group in groups:
        tr = []
        if verbose:
            tr.append(group["id"])
        tr.append(group["name"])
        wrapped_description = textwrap.fill(group["description"], width=20)
        tr.append(wrapped_description)

        tr.append("\n".join(group["members"]))
        tr.append("\n".join(f"{lab['title']} ({lab['permission']})" for lab in group["labs"]))
        table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
