from jinja2 import Environment, PackageLoader
from virl.helpers import get_node_mgmt_ip


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
                entry["prefix"] = "{{ NX_PREFIX }}"
                entry["ned"] = "{{ NX_NED_ID }}"
                entry["ns"] = "{{ NX_NAMESPACE }}"
            elif "XR" in type:
                entry["prefix"] = "{{ XR_PREFIX }}"
                entry["ned"] = "{{ XR_NED_ID }}"
                entry["ns"] = "{{ XR_NAMESPACE }}"
            elif "CSR" in type or "IOS" in type:
                entry["prefix"] = "{{ IOS_PREFIX }}"
                entry["ned"] = "{{ IOS_NED_ID }}"
                entry["ns"] = "{{ IOS_NAMESPACE }}"
            elif "ASA" in type:
                entry["prefix"] = "{{ ASA_PREFIX }}"
                entry["ned"] = "{{ ASA_NED_ID }}"
                entry["ns"] = "{{ ASA_NAMESPACE }}"
                entry["protocol"] = "ssh"
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
        mgmtip = get_node_mgmt_ip(node)

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
                entry["prefix"] = "{{ NX_PREFIX }}"
                entry["ned"] = "{{ NX_NED_ID }}"
                entry["ns"] = "{{ NX_NAMESPACE }}"
            elif "xr" in type:
                entry["prefix"] = "{{ XR_PREFIX }}"
                entry["ned"] = "{{ XR_NED_ID }}"
                entry["ns"] = "{{ XR_NAMESPACE }}"
            elif "csr" in type or "ios" in type:
                entry["prefix"] = "{{ IOS_PREFIX }}"
                entry["ned"] = "{{ IOS_NED_ID }}"
                entry["ns"] = "{{ IOS_NAMESPACE }}"
            elif "asa" in type:
                entry["prefix"] = "{{ ASA_PREFIX }}"
                entry["ned"] = "{{ ASA_NED_ID }}"
                entry["ns"] = "{{ ASA_NAMESPACE }}"
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
        xml_payload = render_xml_payload1(virl_data, roster, interfaces)
        return xml_payload
    elif style == "json":  # pragma: no cover
        raise NotImplementedError


def nso_payload_generator(lab, server, style="xml", protocol="ssh"):
    """
    given a lab produces a payload file suitable for
    use with network services orchestrator
    """
    payload = render_payload(lab, server, protocol, style)

    return payload
