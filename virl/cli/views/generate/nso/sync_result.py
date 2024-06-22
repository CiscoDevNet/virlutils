import click
import tabulate


def sync_table(sync_result):
    click.secho("""
    NSO Sync Report
    """)
    headers = ["Device", "Result"]
    table = list()

    sync_results = sync_result['tailf-ncs:output']['sync-result']
    for item in sync_results:
        tr = list()
        tr.append(item['device'])

        result = item['result']
        if result is True:
            result = "SUCCESS"
            color = 'green'
        else:
            result = "FAILED"
            color = 'red'

        tr.append(click.style(result, fg=color))
        table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
