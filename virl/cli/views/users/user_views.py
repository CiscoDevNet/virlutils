# -*- coding: utf-8 -*-
import textwrap

import click
import tabulate


def user_list_table(users, verbose=False):
    click.secho("Users on Server", fg="green")
    table = []
    headers = ["ID"] if verbose else []
    headers.extend(["Username", "Administrator", "Full Name", "Email", "Groups", "Labs"])
    for user in users:
        tr = []
        if verbose:
            tr.append(user["id"])
        tr.append(user["username"])
        tr.append(user["admin"])
        wrapped_fullname = textwrap.fill(user["fullname"], width=20)
        tr.append(wrapped_fullname)
        tr.append(user["email"])
        tr.append("\n".join(user["groups"]))
        tr.append("\n".join(user["labs"]))
        table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
