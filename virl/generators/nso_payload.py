from jinja2 import Environment, PackageLoader

from virl.helpers import get_node_mgmt_ip


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
            node_type = node.node_definition.lower()
            if "nx" in node_type:
                entry["prefix"] = "{{ NX_PREFIX }}"
                entry["ned"] = "{{ NX_NED_ID }}"
                entry["ns"] = "{{ NX_NAMESPACE }}"
            elif "xr" in node_type:
                entry["prefix"] = "{{ XR_PREFIX }}"
                entry["ned"] = "{{ XR_NED_ID }}"
                entry["ns"] = "{{ XR_NAMESPACE }}"
            elif "csr" in node_type or "ios" in node_type or "cat" in node_type:
                entry["prefix"] = "{{ IOS_PREFIX }}"
                entry["ned"] = "{{ IOS_NED_ID }}"
                entry["ns"] = "{{ IOS_NAMESPACE }}"
            elif "asa" in node_type:
                entry["prefix"] = "{{ ASA_PREFIX }}"
                entry["ned"] = "{{ ASA_NED_ID }}"
                entry["ns"] = "{{ ASA_NAMESPACE }}"
        except KeyError:
            pass

        if entry.get("ned", None) not in ["unknown", None]:
            inventory.append(entry)

    return inventory


def render_payload(lab, server, protocol, style):
    env = Environment(loader=PackageLoader("virl"), trim_blocks=False)

    if style == "json":  # pragma: no cover
        raise NotImplementedError

    inventory = lab_info(lab, server, protocol)
    payload = env.get_template("nso/xml_payload.j2").render(inventory=inventory)
    return payload


def nso_payload_generator(lab, server, style="xml", protocol="ssh"):
    """
    given a lab produces a payload file suitable for
    use with network services orchestrator
    """
    payload = render_payload(lab, server, protocol, style)

    return payload
