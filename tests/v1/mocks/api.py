
class MockVIRLServer:

    @classmethod
    def launch_simulation(cls):
        response = u'TEST_ENV'
        return response

    @classmethod
    def get_node_console(cls):
        sim_response = {
            u'router2': u'10.94.241.194:17002',
            u'router1': u'10.94.241.194:17001'
        }
        return sim_response

    @classmethod
    def get_sim_roster(cls):
        response = {
            u'guest|TEST_ENV|virl|router1': {
                u'Status': u'ACTIVE',
                u'simLaunch': u'2018-04-06T02:57:15.217442',
                u'simID': u'virlutils_default_XzmcAm',
                u'NodeName': u'router1',
                u'simStatus': u'ACTIVE',
                u'simExpires': None,
                u'managementIP': u'1.1.1.1',
                u'managementProtocol': u'telnet',
                u'SimulationHost': u'10.10.10.170',
                u'NodeSubtype': u'IOSv',
                u'PortMonitor': 17029,
                u'Reachable': True,
                u'SerialPorts': 2,
                u'managementProxy': u'jumphost',
                u'VncConsole': False,
                u'PortConsole': 17028,
                u'Annotation': u'REACHABLE'
            },
            u'guest|TEST_ENV|virl|router2': {
                u'Status': u'ACTIVE',
                u'simLaunch': u'2018-04-06T02:57:15.217442',
                u'simID': u'virlutils_default_XzmcAm',
                u'NodeName': u'router2',
                u'simStatus': u'ACTIVE',
                u'simExpires': None,
                u'managementIP': u'172.16.30.122',
                u'managementProtocol': u'telnet',
                u'SimulationHost': u'10.10.10.170',
                u'NodeSubtype': u'CSR1000',
                u'PortMonitor': 17030,
                u'Reachable': True,
                u'SerialPorts': 2,
                u'managementProxy': u'jumphost',
                u'VncConsole': False,
                u'PortConsole': 17027,
                u'Annotation': u'REACHABLE'
            },
            u'guest|TEST_ENV|virl|~mgmt-lxc': {
                u'Status': u'ACTIVE',
                u'simLaunch': u'2018-04-06T02:57:15.217442',
                u'simID': u'virlutils_default_XzmcAm',
                u'NodeName': u'router2',
                u'simStatus': u'ACTIVE',
                u'simExpires': None,
                u'managementIP': u'LXC_IP',
                u'externalAddr': u'FAKE_EXTERNAL_IP',
                u'managementProtocol': u'telnet',
                u'SimulationHost': u'10.10.10.170',
                u'NodeSubtype': u'mgmt-lxc',
                u'PortMonitor': 17030,
                u'Reachable': True,
                u'SerialPorts': 2,
                u'managementProxy': u'jumphost',
                u'VncConsole': False,
                u'PortConsole': 17027,
                u'Annotation': u'REACHABLE'
            },
            u'guest|TEST_ENV|virl|xr2': {
                u'Status': u'ACTIVE',
                u'simLaunch': u'2018-04-06T02:57:15.217442',
                u'simID': u'virlutils_default_XzmcAm',
                u'NodeName': u'router2',
                u'simStatus': u'ACTIVE',
                u'simExpires': None,
                u'managementIP': u'172.16.30.122',
                u'managementProtocol': u'telnet',
                u'SimulationHost': u'10.10.10.170',
                u'NodeSubtype': u'XR',
                u'PortMonitor': 17030,
                u'Reachable': True,
                u'SerialPorts': 2,
                u'managementProxy': u'jumphost',
                u'VncConsole': False,
                u'PortConsole': 17027,
                u'Annotation': u'REACHABLE'
            },
            u'guest|TEST_ENV|virl|nxos': {
                u'Status': u'ACTIVE',
                u'simLaunch': u'2018-04-06T02:57:15.217442',
                u'simID': u'virlutils_default_XzmcAm',
                u'NodeName': u'router2',
                u'simStatus': u'ACTIVE',
                u'simExpires': None,
                u'managementIP': u'172.16.30.122',
                u'managementProtocol': u'telnet',
                u'SimulationHost': u'10.10.10.170',
                u'NodeSubtype': u'NXOS',
                u'PortMonitor': 17030,
                u'Reachable': True,
                u'SerialPorts': 2,
                u'managementProxy': u'jumphost',
                u'VncConsole': False,
                u'PortConsole': 17027,
                u'Annotation': u'REACHABLE'
            },
            u'guest|TEST_ENV|virl|via-lxc': {
                u'Status': u'ACTIVE',
                u'simLaunch': u'2018-04-06T02:57:15.217442',
                u'simID': u'virlutils_default_XzmcAm',
                u'NodeName': u'router2',
                u'simStatus': u'ACTIVE',
                u'simExpires': None,
                u'managementIP': u'10.5.5.5',
                u'managementProtocol': u'telnet',
                u'SimulationHost': u'10.10.10.170',
                u'NodeSubtype': u'badsubtype',
                u'PortMonitor': 17030,
                u'Reachable': True,
                u'SerialPorts': 2,
                u'managementProxy': u'lxc',
                u'VncConsole': False,
                u'PortConsole': 17027,
                u'Annotation': u'REACHABLE'
            },
            u'guest|TEST_ENV|virl|badtype': {
                u'Status': u'ACTIVE',
                u'simLaunch': u'2018-04-06T02:57:15.217442',
                u'simID': u'virlutils_default_XzmcAm',
                u'NodeName': u'router2',
                u'simStatus': u'ACTIVE',
                u'simExpires': None,
                u'managementIP': u'172.16.30.122',
                u'managementProtocol': u'telnet',
                u'SimulationHost': u'10.10.10.170',
                u'NodeSubtype': u'badsubtype',
                u'PortMonitor': 17030,
                u'Reachable': True,
                u'SerialPorts': 2,
                u'managementProxy': u'jumphost',
                u'VncConsole': False,
                u'PortConsole': 17027,
                u'Annotation': u'REACHABLE'
            },
            u'guest|TEST_ENV|virl|keyerror': {
                u'Status': u'ACTIVE',
                u'PortMonitor': 17030,
                u'Reachable': True,
                u'SerialPorts': 2,
                u'managementProxy': u'jumphost',
                u'VncConsole': False,
                u'PortConsole': 17027,
                u'Annotation': u'REACHABLE'
            }
        }
        return response

    @classmethod
    def get_interfaces(cls):

        response = {
            "2nodes_default_ngTj03": {
                "router2": {
                    "0": {
                        "status": "UP",
                        "link-state": True,
                        "name": "GigabitEthernet0/1",
                        "hw-addr": "fa:16:3e:48:8e:c2",
                        "port-state": True,
                        "external-ip-address": None,
                        "ip-address": "10.255.0.6/30",
                        "external-port": None,
                        "network": "router1-to-router2"
                    },
                    "management": {
                        "status": "UP",
                        "link-state": True,
                        "name": "GigabitEthernet0/0",
                        "hw-addr": "5e:00:c0:01:00:00",
                        "port-state": True,
                        "external-ip-address": True,
                        "ip-address": "172.16.30.126/24",
                        "external-port": True,
                        "network": "flat"
                    }
                },
                "router1": {
                    "0": {
                        "status": "UP",
                        "link-state": True,
                        "name": "GigabitEthernet0/1",
                        "hw-addr": "fa:16:3e:95:f1:c5",
                        "port-state": True,
                        "external-ip-address": None,
                        "ip-address": "10.255.0.5/30",
                        "external-port": None,
                        "network": "router1-to-router2"
                    },
                    "management": {
                        "status": "UP",
                        "link-state": True,
                        "name": "GigabitEthernet0/0",
                        "hw-addr": "5e:00:c0:00:00:00",
                        "port-state": True,
                        "external-ip-address": None,
                        "ip-address": "172.16.30.125/24",
                        "external-port": None,
                        "network": "flat"
                    }
                }
            }
        }
        return response

    @classmethod
    def export(cls):

        with open('tests/v1/static/test_virl_data', 'r') as fh:
            virl_data = fh.read()
        return virl_data

    @classmethod
    def list_simulations(cls):
        response = {
            'simulations': {
                'sim1': {
                    'status': 'ACTIVE',
                    'expires': None,
                    'launched': '2017-12-08T23:39:07.721310',
                },
                'sim3': {
                    'status': 'BUILDING',
                    'expires': None,
                    'launched': '2017-12-08T18:48:34.174486',
                },
                'sim4': {
                    'status': 'ABSENT',
                    'expires': None,
                    'launched': '2017-12-08T18:48:34.174486',
                },
                'sim2': {
                    'status': 'ACTIVE',
                    'expires': None,
                    'launched': '2017-12-08T18:48:34.174486',
                },
                'virlutils-id': {
                    'status': 'ACTIVE',
                    'expires': None,
                    'launched': '2017-12-08T18:48:34.174486',
                },

            }
        }
        return response
