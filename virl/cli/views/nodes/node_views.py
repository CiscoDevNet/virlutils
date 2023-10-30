import tabulate
import click


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

        tr.append(click.style(node.state, fg=color))
        tr.append(node.state == "DEFINED_ON_CORE")
        intfs = []
        if booted:
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
