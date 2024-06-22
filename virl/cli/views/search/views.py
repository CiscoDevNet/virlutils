import click
import tabulate


def repo_table(repo_entries):
    # sort by date
    headers = ["Name", "Stars", "Description"]
    table = list()

    for repo in repo_entries:
        tr = list()
        tr.append(repo["full_name"])
        tr.append(repo["stargazers_count"])
        tr.append(repo["description"])
        table.append(tr)
    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
