import click
import tabulate


def license_details_table(license):
    click.secho("Registration Details")
    print_registration(license["registration"])
    click.secho("Authorization Details")
    print_authorization(license["authorization"])
    click.secho("Features")
    print_features(license["features"])


def license_features_table(license):
    table = list()
    headers = ["ID", "Name", "In Use"]
    for feature in license:
        tr = list()
        tr.append(feature["id"])
        tr.append(feature["name"])
        tr.append(feature["in_use"])

        table.append(tr)

    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))


def print_registration(reg_obj):
    table = list()
    headers = ["Status", "Expires", "Smart Account", "Virtual Account", "Registration Time", "Registration Status", "Next Renewal Time"]
    tr = list()
    stat_color = None
    if reg_obj["status"] == "COMPLETED":
        stat_color = "green"
    elif reg_obj["status"] == "IN_PROGRESS":
        stat_color = "yellow"
    else:
        stat_color = "red"
    tr.append(click.style(reg_obj["status"], fg=stat_color))
    tr.append(reg_obj["expires"])
    tr.append(reg_obj["smart_account"])
    tr.append(reg_obj["virtual_account"])
    if reg_obj["register_time"]["attempted"]:
        reg_color = None
        tr.append(reg_obj["register_time"]["attempted"])
        if reg_obj["register_time"]["success"] == "SUCCESS":
            reg_color = "green"
        else:
            reg_color = "red"
        tr.append(click.style(reg_obj["register_time"]["success"], fg=reg_color))
    else:
        tr.append("N/A")
        tr.append("N/A")
    if reg_obj["renew_time"]["scheduled"]:
        tr.append(reg_obj["renew_time"]["scheduled"])
    else:
        tr.append("N/A")

    table.append(tr)

    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))


def print_authorization(auth_obj):
    table = list()
    headers = ["Status", "Expires", "Renewal Time", "Renewal Status", "Next Renewal Time"]
    tr = list()
    auth_color = None
    if auth_obj["status"] == "IN_COMPLIANCE":
        auth_color = "green"
    else:
        auth_color = "red"
    tr.append(click.style(auth_obj["status"], fg=auth_color))
    tr.append(auth_obj["expires"])
    if auth_obj["renew_time"]["attempted"]:
        renew_color = None
        if auth_obj["renew_time"]["status"] == "SUCCEEDED":
            renew_color = "green"
        elif auth_obj["renew_time"]["status"] == "NOT STARTED":
            renew_color = "yellow"
        else:
            renew_color = "red"
        tr.append(auth_obj["renew_time"]["attempted"])
        tr.append(click.style(auth_obj["renew_time"]["status"], fg=renew_color))
    else:
        tr.append("N/A")
        tr.append("N/A")
    if auth_obj["renew_time"]["scheduled"]:
        tr.append(auth_obj["renew_time"]["scheduled"])
    else:
        tr.append("N/A")

    table.append(tr)

    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))


def print_features(feature_obj):
    table = list()
    headers = ["Name", "Description", "In Use", "Status", "Version"]
    for feature in feature_obj:
        tr = list()
        tr.append(feature["name"])
        tr.append(feature["description"])
        tr.append(feature["in_use"])
        color = None
        if feature["status"] == "IN_COMPLIANCE":
            color = "green"
        elif feature["status"] != "INIT":
            color = "red"
        tr.append(click.style(feature["status"], fg=color))
        tr.append(feature["version"])

        table.append(tr)

    # wrap the output in this try/except block as some terminals
    # may have problem with the 'fancy_grid'
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
