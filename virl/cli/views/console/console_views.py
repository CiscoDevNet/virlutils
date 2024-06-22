import click
import tabulate


def console_table(consoles):
    click.secho("Here is a list of all the running consoles")
    headers = ["Node", "Console Path"]
    table = list()
    for console in consoles:
        tr = list()
        tr.append(console["node"])
        tr.append(console["console"])
        table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
