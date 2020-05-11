from jinja2 import Environment, PackageLoader


def sim_info(virl_xml, roster=None, interfaces=None, protocol="telnet"):
    """
    common inventory info accross yaml/ini
    """
    inventory = list()

    for node_long_name, device in roster.items():
        # make sure we have at least enough info to be useful
        if ("managementIP") in device and ("NodeName" in device):
            entry = dict()
            entry["node_long_name"] = node_long_name
            entry["address"] = device["managementIP"]
            entry["protocol"] = protocol
        # otherwise, skip this device
        else:
            continue

        name = device["NodeName"]
        entry["name"] = name
        entry["ned"] = "unknown"
        entry["ns"] = "unkown"
        # map node types to known NED's
        try:
            type = device["NodeSubtype"]
            if "NX" in type:
                entry["prefix"] = "cisco-nx-id"
                entry["ned"] = "cisco-nx"
                entry["ns"] = "http://tail-f.com/ned/cisco-nx-id"
            elif "XR" in type:
                entry["prefix"] = "cisco-ios-xr-id"
                entry["ned"] = "cisco-ios-xr"
                entry["ns"] = "http://tail-f.com/ned/cisco-ios-xr-id"
            elif "CSR" in type or "IOS" in type:
                entry["prefix"] = "ios-id"
                entry["ned"] = "cisco-ios"
                entry["ns"] = "urn:ios-id"
        except KeyError:
            pass

        if entry.get("ned", None) not in ["unknown", None]:
            inventory.append(entry)

    return inventory


def lab_info(lab, server, protocol):
    """
    common inventory info across xml/json
    """
    inventory = list()

    for node in lab.nodes():
        mgmtip = None
        for i in node.interfaces():
            if i.discovered_ipv4 and len(i.discovered_ipv4) > 0:
                mgmtip = i.discovered_ipv4[0]
            elif i.discovered_ipv6 and len(i.discovered_ipv6) > 0:
                if not ipaddress.ip_address(i.discovered_ipv6[0]).is_link_local:
                    mgmtip = i.discovered_ipv6[0]
            if mgmtip:
                break

        if not mgmtip:
            continue

        name = node.label
        entry = dict()
        entry["address"] = mgmtip
        entry["protocol"] = protocol
        name = node.label
        entry["name"] = name
        entry["ned"] = "unknown"
        entry["ns"] = "unkown"

        # determine device/os type
        try:
            type = node.node_definition.lower()
            if "nx" in type:
                entry["prefix"] = "cisco-nx-id"
                entry["ned"] = "cisco-nx"
                entry["ns"] = "http://tail-f.com/ned/cisco-nx-id"
            elif "xr" in type:
                entry["prefix"] = "cisco-ios-xr-id"
                entry["ned"] = "cisco-ios-xr"
                entry["ns"] = "http://tail-f.com/ned/cisco-ios-xr-id"
            elif "csr" in type or "ios" in type:
                entry["prefix"] = "ios-id"
                entry["ned"] = "cisco-ios"
                entry["ns"] = "urn:ios-id"
        except KeyError:
            pass

        if entry.get("ned", None) not in ["unknown", None]:
            inventory.append(entry)

    return inventory


def render_xml_payload1(virl_xml, roster=None, interfaces=None, protocol="telnet"):
    """
    we need to merge information from multiple sources to generate all
    the required parameters for the inventory

    """
    env = Environment(loader=PackageLoader("virl"), trim_blocks=False)

    inventory = sim_info(virl_xml, roster=roster, interfaces=interfaces, protocol=protocol)
    # pass all available data to template for rendering, this can probably be
    # pruned back at some point
    xml = env.get_template("nso/xml_payload.j2").render(inventory=inventory)
    return xml


def render_payload(lab, server, protocol, style):
    env = Environment(loader=PackageLoader("virl"), trim_blocks=False)

    if style == "json":  # pragma: no cover
        raise NotImplementedError

    inventory = lab_info(lab, server, protocol)
    payload = env.get_template("nso/xml_payload.j2").render(inventory=inventory)
    return payload


def nso_payload_generator1(env, virl_data, roster, interfaces, style="xml", protocol="telnet"):
    """
    given a sim roster produces a payload file suitable for
    use with network services orchestrator

    """
    if style == "xml":
        xml_payload = render_xml_payload(virl_data, roster, interfaces)
        return xml_payload
    elif style == "json":  # pragma: no cover
        raise NotImplementedError


def nso_payload_generator(lab, server, style="xml", protocol="telnet"):
    """
    given a lab produces a payload file suitable for
    use with network services orchestrator
    """
    payload = render_payload(lab, server, protocol, style)

    return payload
