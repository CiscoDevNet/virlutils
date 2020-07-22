import click
import tabulate


def node_def_list_table(image_list):

    headers = ["ID", "Label", "Description", "Max No. Interfaces", "RAM", "CPUs", "Boot Disk Size"]
    table = list()

    for f in list(image_list):
        tr = list()
        tr.append(str(f["id"]))
        tr.append(str(f["data"]["ui"].get("label", "N/A")))
        tr.append(str(f["data"]["general"]["description"]))
        tr.append(str(len(f["data"]["device"]["interfaces"]["physical"])))
        linux_native = f["data"]["sim"].get("linux_native", None)
        if linux_native:
            ram = int(linux_native.get("ram", 0))
            unit = "GB"
            if ram > 1024:
                ram /= 1024
            else:
                unit = "MB"
            tr.append(str(ram) + " " + unit)
            tr.append(str(linux_native.get("cpus", "N/A")))
            if "boot_disk_size" in linux_native:
                tr.append(str(linux_native["boot_disk_size"]) + " GB")
            else:
                tr.append("N/A")
        else:
            tr.append("N/A")  # RAM
            tr.append("N/A")  # CPU
            tr.append("N/A")  # Boot Disk Size

        table.append(tr)

    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
