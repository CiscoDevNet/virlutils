# -*- coding: utf-8 -*-
import click
import tabulate


def sim_list_table(node_dict):
    click.secho("Running Simulations", fg="green")
    table = list()
    headers = ["Simulation", "Status", "Launched", "Expires"]
    for node, props in node_dict.items():
        tr = list()
        tr.append(node)
        status = props['status']
        if status == 'ACTIVE':
            color = 'green'
        elif status == 'BUILDING':
            color = 'yellow'
        else:
            color = 'red'
        tr.append(click.style(status, fg=color))
        tr.append(props['launched'])
        tr.append(props.get('expires', 'N/A'))
        table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
