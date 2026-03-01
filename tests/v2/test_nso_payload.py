import pytest

from virl.generators.nso_payload import lab_info, nso_payload_generator, render_payload


class FakeInterface:
    def __init__(self, ipv4=None, ipv6=None):
        self.discovered_ipv4 = ipv4 or []
        self.discovered_ipv6 = ipv6 or []


class FakeNode:
    def __init__(self, label, definition, interfaces=None):
        self.label = label
        self.node_definition = definition
        self._interfaces = interfaces or []

    def interfaces(self):
        return self._interfaces


class FakeLab:
    def __init__(self, nodes):
        self._nodes = nodes

    def nodes(self):
        return self._nodes


class FakeServer:
    host = "example.local"
    user = "cml-user"


def test_lab_info_maps_ios_node_to_ios_ned():
    node = FakeNode("rtr-1", "iosv", interfaces=[FakeInterface(ipv4=["10.0.0.1"])])
    inventory = lab_info(FakeLab([node]), FakeServer, "ssh")

    assert len(inventory) == 1
    assert inventory[0]["name"] == "rtr-1"
    assert inventory[0]["protocol"] == "ssh"
    assert inventory[0]["ned"] == "{{ IOS_NED_ID }}"
    assert inventory[0]["ns"] == "{{ IOS_NAMESPACE }}"


def test_lab_info_skips_nodes_without_supported_ned():
    node = FakeNode("custom-1", "custom", interfaces=[FakeInterface(ipv4=["10.0.0.2"])])
    inventory = lab_info(FakeLab([node]), FakeServer, "ssh")

    assert inventory == []


def test_render_payload_raises_for_json_style():
    with pytest.raises(NotImplementedError):
        render_payload(FakeLab([]), FakeServer, protocol="ssh", style="json")


def test_nso_payload_generator_renders_xml():
    node = FakeNode("rtr-1", "nxos", interfaces=[FakeInterface(ipv4=["10.0.0.3"])])
    payload = nso_payload_generator(FakeLab([node]), FakeServer, style="xml", protocol="ssh")

    assert "<devices" in payload
    assert "<name>rtr-1</name>" in payload
