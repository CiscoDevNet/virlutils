import click
import tabulate


def image_list_table(image_list):

    headers = ["ID", "Node Definition ID", "Label", "Description", "RAM", "CPUs", "Boot Disk Size"]
    table = list()

    for f in list(image_list):
        tr = list()
        tr.append(str(f["id"]))
        tr.append(str(f["node_definition_id"]))
        tr.append(str(f["label"]))
        tr.append(str(f["description"]))
        tr.append(str(f["ram"]))
        tr.append(str(f["cpus"]))
        tr.append(str(f["boot_disk_size"]))

        table.append(tr)

    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
