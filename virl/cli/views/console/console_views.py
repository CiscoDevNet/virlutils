import tabulate
import click


def console_table(console_entries):
    click.secho("""
    Here is a list of all the running consoles
    """)
    headers = ["Node", "IP", "Port"]
    table = list()
    for node, ip_port in console_entries.items():
        tr = list()
        tr.append(node)
        if ip_port:
            tr.append(ip_port.split(":")[0])
            tr.append(ip_port.split(":")[1])
        table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
