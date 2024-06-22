import click
import tabulate


def node_list_table(nodes, computes):
    click.secho("Here is a list of nodes in this lab")
    table = list()
    headers = ["ID", "Label", "Type"]
    if computes:
        headers.append("Compute Node")

    headers += ["State", "Wiped?", "L3 Address(es)"]
    skip_types = []
    for node in nodes:
        # Skip a full operational sync per node.
        node.lab.auto_sync = True
        for sync in (
            # "sync_statistics_if_outdated",
            "sync_states_if_outdated",
            "sync_l3_addresses_if_outdated",
            "sync_topology_if_outdated",
        ):
            try:
                meth = getattr(node.lab, sync)
            except AttributeError:
                pass
            else:
                meth()

        node.lab.auto_sync = False

        tr = list()
        if node.node_definition in skip_types:
            continue

        tr.append(node.id)
        tr.append(node.label)
        tr.append(node.node_definition)
        try:
            node_compute_id = node.compute_id
        except AttributeError:
            node_compute_id = None

        if node_compute_id and node_compute_id in computes:
            tr.append(computes[node_compute_id]["hostname"])
        elif computes:
            tr.append("Unknown")

        color = "red"
        booted = node.is_booted()
        if booted:
            color = "green"
        elif node.is_active():
            color = "yellow"

        node_state = node.state
        tr.append(click.style(node_state, fg=color))
        tr.append(node_state == "DEFINED_ON_CORE")
        intfs = []
        if booted:
            for i in node.interfaces():
                disc_ipv4 = i.discovered_ipv4
                if disc_ipv4:
                    intfs += disc_ipv4

                disc_ipv6 = i.discovered_ipv6
                if disc_ipv6:
                    intfs += disc_ipv6

        tr.append("\n".join(intfs))
        table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
