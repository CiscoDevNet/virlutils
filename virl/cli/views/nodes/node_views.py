import tabulate
import click


def node_list_table(nodes, computes):
    click.secho("Here is a list of nodes in this lab")
    table = list()
    headers = ["ID", "Label", "Type"]
    if len(computes.keys()) > 0:
        headers.append("Compute Node")

    headers += ["State", "Wiped?", "L3 Address(es)"]
    skip_types = []
    for node in nodes:
        # Skip a full operational sync per node.
        node.lab.auto_sync = True
        for sync in (
            "sync_statistics_if_outdated",
            "sync_states_if_outdated",
            "sync_layer3_addresses_if_outdated",
            "sync_topology_if_outdated",
        ):
            meth = getattr(node.lab, sync)
            meth()

        node.lab.auto_sync = False

        tr = list()
        if node.node_definition in skip_types:
            continue

        tr.append(node.id)
        tr.append(node.label)
        tr.append(node.node_definition)
        if len(computes.keys()) > 0 and hasattr(node, "compute_id") and node.compute_id in computes:
            tr.append(computes[node.compute_id]["hostname"])
        elif len(computes.keys()) > 0:
            tr.append("Unknown")

        color = "red"
        if node.is_booted():
            color = "green"
        elif node.is_active():
            color = "yellow"

        tr.append(click.style(node.state, fg=color))
        tr.append(node.state == "DEFINED_ON_CORE")
        intfs = []
        if node.is_booted():
            for i in node.interfaces():
                if i.discovered_ipv4:
                    intfs += i.discovered_ipv4
                if i.discovered_ipv6:
                    intfs += i.discovered_ipv6

        tr.append(",".join(intfs))
        table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))


def node_list_table1(node_dict):
    click.secho("Here is a list of all the running nodes")
    table = list()
    headers = ["Node", "Type", "State", "Reachable", "Protocol", "Management Address", "External Address"]
    skip_subtypes = ["LXC FLAT"]
    for key, props in node_dict.items():
        tr = list()
        # make sure we have minimally useful data otherwise we won't display it
        if all(k in props for k in ["NodeName", "NodeSubtype"]):
            node = props.get("NodeName", "unknown")
            tr.append(node)

            subtype = props.get("NodeSubtype")

            if subtype in skip_subtypes:
                continue
            tr.append(subtype)

            state = props.get("Status", None)

            if state:
                if state in ["ACTIVE"]:
                    color = "green"
                elif state in ["BUILDING"]:
                    color = "yellow"
                else:
                    color = "red"
            else:
                state = "UNKNOWN"
                color = "red"

            reachable = props.get("Annotation", "N/A")
            if reachable:
                if reachable in ["UNREACHABLE"]:
                    r_color = "red"
                elif reachable in ["REACHABLE"]:
                    r_color = "green"
                else:
                    r_color = "red"
            else:
                state = "UNKNOWN"
                r_color = "red"

            tr.append(click.style(state, fg=color))
            tr.append(click.style(reachable, fg=r_color))
            tr.append(props.get("managementProtocol", "N/A"))
            tr.append(props.get("managementIP", "N/A"))
            tr.append(props.get("externalAddr", "N/A"))

            table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
