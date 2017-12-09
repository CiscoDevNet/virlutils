from virl.api import VIRLServer

server = VIRLServer()

print server.list_simulations()
# {u'virl_cli_default_1dNVCr': {u'status': u'ACTIVE', u'expires': None, u'launched': u'2017-12-08T23:39:07.721310'}, u'topology-fpyHFs': {u'status': u'ACTIVE', u'expires': None, u'launched': u'2017-12-08T18:48:34.174486'}}

sample_sim_data = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<topology xmlns="http://www.cisco.com/VIRL" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" schemaVersion="0.95" xsi:schemaLocation="http://www.cisco.com/VIRL https://raw.github.com/CiscoVIRL/schema/v0.95/virl.xsd">
    <node name="iosv-1" type="SIMPLE" subtype="IOSv" location="586,280"/>
    <annotations/>
</topology>
"""
print server.launch_simulation('test', sample_sim_data)
# test

print server.get_nodes('test').json()
# u'~mgmt-lxc': {u'vnc-console': False, u'subtype': u'mgmt-lxc', u'state': u'ABSENT', u'reachable': None, u'management-protocol': u'ssh', u'management-proxy': u'self', u'serial-ports': 0}, u'iosv-1': {u'vnc-console': False, u'subtype': u'IOSv', u'state': u'ABSENT', u'reachable': None, u'management-protocol': u'telnet', u'management-proxy': u'lxc', u'serial-ports': 2}}

print server.get_node_console('test').json()
#  {"iosv-1": "10.94.140.41:17016","~mgmt-lxc": null}

print server.stop_simulation('test').text
# SUCCESS
