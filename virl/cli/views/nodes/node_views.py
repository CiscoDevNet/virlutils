import tabulate
import click

def node_list_table(node_dict):
    click.secho("Here is a list of all the running nodes")
    table = list()
    headers = ["Node", "Type", "State", "Reachable", "Protocol", "Management Address", "External Address"]
    skip_subtypes = ["LXC FLAT"]
    for key, props in node_dict.items():
        tr = list()
        # make sure we have minimally useful data otherwise we won't display it..
        if all(k in props for k in ["NodeName", "NodeSubtype"]):
            node = props.get("NodeName", "unknown")
            tr.append(node)

            subtype = props.get('NodeSubtype')

            if subtype in skip_subtypes:
                continue
            tr.append(subtype)

            state = props.get('Status', None)

            if state:
                if state in ['ACTIVE']:
                    color = 'green'
                elif state in ['BUILDING']:
                    color = 'yellow'
                else:
                    color = 'red'
            else:
                state = 'UNKNOWN'
                color = 'red'
            tr.append(click.style(state, fg=color))
            tr.append(props.get('Annotation', "N/A"))
            tr.append(props.get('managementProtocol', "N/A"))
            tr.append(props.get('managementIP', "N/A"))
            tr.append(props.get("externalAddr", "N/A"))

            table.append(tr)

    click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
