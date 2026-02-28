from virl.generators.ansible_inventory import ansible_inventory_generator, generate_inventory_dict, render_inventory


class FakeInterface:
    def __init__(self, ipv4=None, ipv6=None):
        self.discovered_ipv4 = ipv4 or []
        self.discovered_ipv6 = ipv6 or []


class FakeNode:
    def __init__(self, label, node_id, definition, tags=None, interfaces=None):
        self.label = label
        self.id = node_id
        self.node_definition = definition
        self._tags = tags or []
        self._interfaces = interfaces or []

    def tags(self):
        return self._tags

    def interfaces(self):
        return self._interfaces


class FakeLab:
    def __init__(self, lab_id, title, nodes):
        self.id = lab_id
        self.title = title
        self._nodes = nodes

    def nodes(self):
        return self._nodes


class FakeServer:
    host = "example.local"
    user = "cml-user"


def test_generate_inventory_places_tagged_nodes_into_children_group():
    node = FakeNode(
        label="rtr-1",
        node_id="node1",
        definition="iosv",
        tags=["ansible_group=routers"],
        interfaces=[FakeInterface(ipv4=["10.0.0.1"])],
    )
    lab = FakeLab("lab-id", "Demo Lab", [node])

    inventory = generate_inventory_dict(lab, FakeServer)

    assert "routers" in inventory["all"]["children"]
    assert "rtr-1" in inventory["all"]["children"]["routers"]
    entry = inventory["all"]["children"]["routers"]["rtr-1"]
    assert entry["ansible_host"] == "10.0.0.1"
    assert entry["device_type"] == "ios"


def test_generate_inventory_uses_unknown_device_type_when_not_mapped():
    node = FakeNode(
        label="custom-1",
        node_id="node1",
        definition="custom-os",
        interfaces=[FakeInterface(ipv4=["10.0.0.5"])],
    )
    lab = FakeLab("lab-id", "Demo Lab", [node])

    inventory = generate_inventory_dict(lab, FakeServer)

    assert inventory["all"]["hosts"]["custom-1"]["device_type"] == "unknown"


def test_render_inventory_returns_none_for_unsupported_style():
    node = FakeNode(
        label="rtr-1",
        node_id="node1",
        definition="iosv",
        interfaces=[FakeInterface(ipv4=["10.0.0.1"])],
    )
    lab = FakeLab("lab-id", "Demo Lab", [node])

    assert render_inventory(lab, FakeServer, "json") is None


def test_ansible_inventory_generator_renders_ini_style():
    node = FakeNode(
        label="rtr-1",
        node_id="node1",
        definition="iosv",
        tags=["ansible_group=routers"],
        interfaces=[FakeInterface(ipv4=["10.0.0.1"])],
    )
    lab = FakeLab("lab-id", "Demo Lab", [node])

    rendered = ansible_inventory_generator(lab, FakeServer, style="ini")

    assert rendered is not None
    assert "[routers]" in rendered
    assert "rtr-1" in rendered
