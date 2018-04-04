import tabulate
import click


def log_table(log_entries):
    click.secho("Here is a list of recent log entries")
    # sort by date
    log_entries = sorted(log_entries, key=lambda k: k['id'])
    headers = ["Timestamp", "Severity", "Message"]
    table = list()

    for log in log_entries:
        tr = list()
        tr.append(log['time'])
        level = log['level']
        if level == 'INFO':
            color = "green"
        else:
            color = 'yellow'
        tr.append(click.style(level, fg=color))
        tr.append(log['message'])
        table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
