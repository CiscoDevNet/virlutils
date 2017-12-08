import tabulate
import click

def node_list_table(node_dict):
    print("""
    Here is a list of all the running nodes
    """)
    table = list()
    headers = ["Node", "Type", "State", "Reachable", "management-protocol"]
    for node, props in node_dict.items():
        tr = list()
        tr.append(node)
        tr.append(props['subtype'])
        tr.append(props['state'])
        tr.append(props['reachable'])
        tr.append(props['management-protocol'])

        table.append(tr)

    # print type(table)
    click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
