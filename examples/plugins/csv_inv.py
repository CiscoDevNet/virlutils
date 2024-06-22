import csv

import click

from virl.api import GeneratorPlugin, VIRLServer
from virl.helpers import (get_cml_client, get_current_lab, get_node_mgmt_ip,
                          safe_join_existing_lab)


class CSVInventory(GeneratorPlugin, generator="csv"):
    @staticmethod
    def write_inventory(nodes, delimiter, output):
        with open(output, "w") as fd:
            csvwriter = csv.writer(fd, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(["Name", "Type", "Tags", "IP Address"])
            for node in nodes:
                mgmt_ip = get_node_mgmt_ip(node)
                if not mgmt_ip:
                    continue

                row = [node.label]
                row.append(node.node_definition.lower())
                row.append(" ".join(node.tags()))
                row.append(mgmt_ip)
                csvwriter.writerow(row)

    @staticmethod
    @click.command()
    @click.option(
        "--delimiter", "-d", default=",", show_default=False, required=False, help="Delimiter to use between fields (default: ',')"
    )
    @click.option(
        "--output",
        "-o",
        default="inventory.csv",
        show_default=False,
        required=False,
        help="File to write inventory (default: inventory.csv)",
    )
    def generate(delimiter, output):
        """
        generate generic CSV inventory
        """
        server = VIRLServer()
        client = get_cml_client(server)

        current_lab = get_current_lab()
        if not current_lab:
            click.secho("Current lab is not set", fg="red")
            exit(1)

        lab = safe_join_existing_lab(current_lab, client)
        if not lab:
            click.secho("Failed to find running lab {}".format(current_lab), fg="red")
            exit(1)

        exit(CSVInventory.write_inventory(lab.nodes(), delimiter, output))
