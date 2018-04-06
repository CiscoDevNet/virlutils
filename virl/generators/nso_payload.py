from jinja2 import Environment, PackageLoader


def sim_info(virl_xml, roster=None, interfaces=None, protocol="telnet"):
    """
    common inventory info accross yaml/ini
    """
    inventory = list()

    for node_long_name, device in roster.items():
        # make sure we have at least enough info to be useful
        if ('managementIP') in device and ('NodeName' in device):
            entry = dict()
            entry['node_long_name'] = node_long_name
            entry['address'] = device['managementIP']
            entry['protocol'] = protocol
        # otherwise, skip this device
        else:
            continue

        name = device['NodeName']
        entry['name'] = name
        # map node types to known NED's
        try:
            type = device['NodeSubtype']
            if 'NX' in type:
                entry['ned'] = 'cisco-nx'
            elif 'XR' in type:
                entry['ned'] = 'cisco-ios-xr'
            elif 'CSR' in type:
                entry['ned'] = 'cisco-ios'
            elif 'IOS' in type:
                entry['ned'] = 'cisco-ios'
            else:
                entry['ned'] = 'unknown'
        except KeyError:
            entry['ned'] = 'unknown'

        if entry.get('ned', None) not in ['unknown', None]:
            inventory.append(entry)

    return inventory


def render_xml_payload(virl_xml, roster=None,
                       interfaces=None, protocol="telnet"):
    """
    we need to merge information from multiple sources to generate all
    the required parameters for the inventory

    """
    env = Environment(loader=PackageLoader('virl'),
                      trim_blocks=False)

    inventory = sim_info(virl_xml,
                         roster=roster,
                         interfaces=interfaces,
                         protocol=protocol)
    # pass all available data to template for rendering, this can probably be
    # pruned back at some point
    xml = env.get_template('nso/xml_payload.j2').render(inventory=inventory)
    return xml


def nso_payload_generator(env, virl_data, roster, interfaces,
                          style="xml", protocol="telnet"):
    """
    given a sim roster produces a payload file suitable for
    use with network services orchestrator

    """
    if style == "xml":
        xml_payload = render_xml_payload(virl_data, roster, interfaces)
        return xml_payload
    elif style == "json":  # pragma: no cover
        raise NotImplementedError
