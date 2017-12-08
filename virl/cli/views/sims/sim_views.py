import click
import tabulate

def sim_list_table(node_dict):
    print("""
    Here is a list of all the running nodes
    """)
    table = list()
    headers = ["Simulation", "Status", "Launched", "Expires"]
    for node, props in node_dict.items():
        tr = list()
        tr.append(node)
        tr.append(props['status'])
        tr.append(props['launched'])
        tr.append(props.get('expires', 'N/A'))
        table.append(tr)
    click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
