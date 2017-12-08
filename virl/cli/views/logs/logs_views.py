import tabulate
import click

def log_table(log_entries):
    print("""
    Here is a list of all the running nodes
    """)
    # sort by date
    log_entries = newlist = sorted(log_entries, key=lambda k: k['id'])
    headers = ["Timestamp", "Severity", "Message"]
    table = list()

    for log in log_entries:
        tr = list()
        tr.append(log['time'])
        tr.append(log['level'])
        tr.append(log['message'])
        table.append(tr)
    click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
