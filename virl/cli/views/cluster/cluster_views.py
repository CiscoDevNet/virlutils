import click
import tabulate


def cluster_list_table(computes: dict) -> None:
    table = list()
    headers = ["ID", "Hostname", "Is Controller?", "Status"]
    for cid, compute in computes.items():
        tr = list()

        tr.append(cid)
        tr.append(compute["hostname"])
        tr.append(compute["is_controller"])

        healthy = "HEALTHY"
        bad_props = []
        for stat_prop, description in {
            "kvm_vmx_enabled": "KVM",
            "enough_cpus": "CPU",
            "refplat_images_available": "REFPLAT",
            "lld_connected": "LLD",
            "valid": "VALID",
        }.items():
            if not compute[stat_prop]:
                healthy = "UNHEALTHY"
                bad_props.append(description)

        color = "green"
        if len(bad_props) > 0:
            healthy += " ({})".format(",".join(bad_props))
            color = "red"

        tr.append(click.style(healthy, fg=color))
        table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
