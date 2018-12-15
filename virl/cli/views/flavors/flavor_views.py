import click
import tabulate


def flavor_list_table(flavors_list):

    headers = ['Name', 'Memory', 'vCPUs']
    table = list()

    for f in list(flavors_list):
        tr = list()
        tr.append(str(f['name']))
        tr.append(str(f['ram']))
        tr.append(str(f['vcpus']))

        table.append(tr)

    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
