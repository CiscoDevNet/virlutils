class MockCMLServer(object):
    @staticmethod
    def get_lab_tiles(req, ctx=None):
        response = {
            "lab_tiles": {
                "5eaea5": {
                    "state": "STOPPED",
                    "created": "2020-07-21 09:10:39",
                    "lab_title": "Other Lab",
                    "lab_description": "",
                    "node_count": 2,
                    "link_count": 1,
                    "id": "5eaea5",
                    "owner": "admin",
                    "topology": {
                        "nodes": [
                            {
                                "id": "n0",
                                "label": "nxos9000-0",
                                "x": -450,
                                "y": -50,
                                "node_definition": "nxosv9000",
                                "image_definition": "nxosv9000-9-2-3",
                                "state": "STOPPED",
                                "cpus": None,
                                "cpu_limit": None,
                                "ram": None,
                                "data_volume": None,
                                "boot_disk_size": None,
                                "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                                "tags": [],
                            },
                            {
                                "id": "n1",
                                "label": "xr9kv-0",
                                "x": -150,
                                "y": -50,
                                "node_definition": "iosxrv9000",
                                "image_definition": "iosxrv9000-6-6-2",
                                "state": "STOPPED",
                                "cpus": None,
                                "cpu_limit": None,
                                "ram": None,
                                "data_volume": None,
                                "boot_disk_size": None,
                                "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                                "tags": [],
                            },
                        ],
                        "links": [{"id": "l0", "node_a": "n0", "node_b": "n1", "state": "STOPPED"}],
                    },
                },
                "88119b68-9d08-40c4-90f5-6dc533fd0254": {
                    "state": "STARTED",
                    "created": "2020-08-18 22:47:56",
                    "lab_title": "Mock Test 2.3",
                    "lab_description": "",
                    "node_count": 2,
                    "link_count": 1,
                    "id": "88119b68-9d08-40c4-90f5-6dc533fd0254",
                    "owner": "admin",
                    "topology": {
                        "nodes": [
                            {
                                "id": "88119b68-9d08-40c4-90f5-6dc533fd0255",
                                "label": "Lab Net",
                                "x": -400,
                                "y": 0,
                                "node_definition": "external_connector",
                                "image_definition": None,
                                "state": "BOOTED",
                                "cpus": None,
                                "cpu_limit": None,
                                "ram": None,
                                "data_volume": None,
                                "boot_disk_size": None,
                                "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                                "tags": [],
                            },
                            {
                                "id": "88119b68-9d08-40c4-90f5-6dc533fd0256",
                                "label": "rtr-1",
                                "x": -200,
                                "y": -50,
                                "node_definition": "iosxrv9000",
                                "image_definition": "iosxrv9000-6-6-2",
                                "state": "BOOTED",
                                "cpus": None,
                                "cpu_limit": None,
                                "ram": None,
                                "data_volume": None,
                                "boot_disk_size": None,
                                "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                                "tags": [],
                            },
                            {
                                "id": "88119b68-9d08-40c4-90f5-6dc533fd0257",
                                "label": "rtr-2",
                                "x": -200,
                                "y": -50,
                                "node_definition": "iosxrv9000",
                                "image_definition": "iosxrv9000-6-6-2",
                                "state": "DEFINED_ON_CORE",
                                "cpus": None,
                                "cpu_limit": None,
                                "ram": None,
                                "data_volume": None,
                                "boot_disk_size": None,
                                "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                                "tags": [],
                            },
                        ],
                        "links": [
                            {
                                "id": "88119b68-9d08-40c4-90f5-6dc533fd0258",
                                "node_a": "88119b68-9d08-40c4-90f5-6dc533fd0256",
                                "node_b": "88119b68-9d08-40c4-90f5-6dc533fd0255",
                                "state": "STARTED",
                            }
                        ],
                    },
                },
                "5f0d96": {
                    "state": "STARTED",
                    "created": "2020-08-18 22:47:56",
                    "lab_title": "Mock Test",
                    "lab_description": "",
                    "node_count": 2,
                    "link_count": 1,
                    "id": "5f0d96",
                    "owner": "admin",
                    "topology": {
                        "nodes": [
                            {
                                "id": "n0",
                                "label": "Lab Net",
                                "x": -400,
                                "y": 0,
                                "node_definition": "external_connector",
                                "image_definition": None,
                                "state": "BOOTED",
                                "cpus": None,
                                "cpu_limit": None,
                                "ram": None,
                                "data_volume": None,
                                "boot_disk_size": None,
                                "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                                "tags": [],
                            },
                            {
                                "id": "n1",
                                "label": "rtr-1",
                                "x": -200,
                                "y": -50,
                                "node_definition": "iosxrv9000",
                                "image_definition": "iosxrv9000-6-6-2",
                                "state": "BOOTED",
                                "cpus": None,
                                "cpu_limit": None,
                                "ram": None,
                                "data_volume": None,
                                "boot_disk_size": None,
                                "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                                "tags": [],
                            },
                            {
                                "id": "n2",
                                "label": "rtr-2",
                                "x": -200,
                                "y": -50,
                                "node_definition": "iosxrv9000",
                                "image_definition": "iosxrv9000-6-6-2",
                                "state": "DEFINED_ON_CORE",
                                "cpus": None,
                                "cpu_limit": None,
                                "ram": None,
                                "data_volume": None,
                                "boot_disk_size": None,
                                "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                                "tags": [],
                            },
                        ],
                        "links": [{"id": "l0", "node_a": "n1", "node_b": "n0", "state": "STARTED"}],
                    },
                },
            },
            "health": {
                "valid": True,
                "details": {
                    "cluster_1": {
                        "compute_1": {
                            "has_hw_acceleration": True,
                            "enough_cpus": True,
                            "has_refplat_images": True,
                            "lld_connected": True,
                            "valid": True,
                        },
                        "valid": True,
                    }
                },
                "is_licensed": True,
            },
            "system_information": {"version": "2.3.0", "ready": True},
            "system_stats": {
                "clusters": {
                    "cluster_1": {
                        "high_level_drivers": {
                            "compute_1": {
                                "cpu": {
                                    "load": [1.37, 1.45, 1.47],
                                    "count": 16,
                                    "percent": 10.84375,
                                    "model": "Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz",
                                },
                                "memory": {"total": 101098348544, "free": 86657089536, "used": 13702373376},
                                "disk": {"total": 106285760512, "free": 79234523136, "used": 27051237376},
                                "dominfo": {"allocated_cpus": 2, "allocated_memory": 12582912, "total_vms": 5, "running_vms": 1},
                            }
                        }
                    }
                }
            },
            "user_roles": ["USER", "ADMIN"],
        }
        return response

    @staticmethod
    def get_labs(req, ctx=None):
        response = ["5eaea5", "5f0d96", "88119b68-9d08-40c4-90f5-6dc533fd0254"]
        return response

    @staticmethod
    def download_lab(req, ctx=None):
        response = """
        lab:
          description: ''
          notes: ''
          title: Mock Test
          version: 0.1.0
        links:
          - id: l0
            n1: n1
            n2: n0
            i1: i1
            i2: i0
            label: rtr-1-MgmtEth0/RP0/CPU0/0<->Lab Net-port
        nodes:
          - boot_disk_size: 0
            configuration: bridge0
            cpu_limit: 100
            cpus: 0
            data_volume: 0
            hide_links: false
            id: n0
            label: Lab Net
            node_definition: external_connector
            ram: 0
            tags: []
            x: -400
            y: 0
            interfaces:
              - id: i0
                label: port
                slot: 0
                type: physical
          - boot_disk_size: 0
            configuration: |-
              hostname changeme
              username cisco
              group root-lr
              group cisco-support
              password cisco
              !
              username admin
              group root-lr
              group cisco-support
              password admin
              !
              username lab
              group root-lr
              group cisco-support
              password lab
              !
              end
            cpu_limit: 100
            cpus: 0
            data_volume: 0
            hide_links: false
            id: n1
            image_definition: iosxrv9000-6-6-2
            label: rtr-1
            node_definition: iosxrv9000
            ram: 0
            tags: []
            x: -200
            y: -50
            interfaces:
              - id: i0
                label: Loopback0
                type: loopback
              - id: i1
                label: MgmtEth0/RP0/CPU0/0
                slot: 0
                type: physical
              - id: i2
                label: donotuse1
                slot: 1
                type: physical
              - id: i3
                label: donotuse2
                slot: 2
                type: physical
              - id: i4
                label: GigabitEthernet0/0/0/0
                slot: 3
                type: physical
          - boot_disk_size: 0
            configuration: |-
              hostname changeme
              username cisco
              group root-lr
              group cisco-support
              password cisco
              !
              username admin
              group root-lr
              group cisco-support
              password admin
              !
              username lab
              group root-lr
              group cisco-support
              password lab
              !
              end
            cpu_limit: 100
            cpus: 0
            data_volume: 0
            hide_links: false
            id: n2
            image_definition: iosxrv9000-6-6-2
            label: rtr-2
            node_definition: iosxrv9000
            ram: 0
            tags: []
            x: -300
            y: 50
            interfaces:
              - id: i0
                label: Loopback0
                type: loopback
              - id: i1
                label: MgmtEth0/RP0/CPU0/0
                slot: 0
                type: physical
              - id: i2
                label: donotuse1
                slot: 1
                type: physical
              - id: i3
                label: donotuse2
                slot: 2
                type: physical
              - id: i4
                label: GigabitEthernet0/0/0/0
                slot: 3
                type: physical
        """
        return response

    @staticmethod
    def download_lab_24(req, ctx=None):
        response = """
        lab:
          description: ''
          notes: ''
          title: Mock Test 2.4
          version: 0.1.0
        links:
          - id: l0
            n1: n1
            n2: n0
            i1: i1
            i2: i0
            label: rtr-1-MgmtEth0/RP0/CPU0/0<->Lab Net-port
        nodes:
          - boot_disk_size: 0
            configuration: bridge0
            cpu_limit: 100
            cpus: 0
            data_volume: 0
            hide_links: false
            id: n0
            label: Lab Net
            node_definition: external_connector
            ram: 0
            tags: []
            x: -400
            y: 0
            interfaces:
              - id: i0
                label: port
                slot: 0
                type: physical
          - boot_disk_size: 0
            configuration: |-
              hostname changeme
              username cisco
              group root-lr
              group cisco-support
              password cisco
              !
              username admin
              group root-lr
              group cisco-support
              password admin
              !
              username lab
              group root-lr
              group cisco-support
              password lab
              !
              end
            cpu_limit: 100
            cpus: 0
            data_volume: 0
            hide_links: false
            id: n1
            label: rtr-1
            node_definition: iosxrv9000
            ram: 0
            tags: []
            x: -200
            y: -50
            interfaces:
              - id: i0
                label: Loopback0
                type: loopback
              - id: i1
                label: MgmtEth0/RP0/CPU0/0
                slot: 0
                type: physical
              - id: i2
                label: donotuse1
                slot: 1
                type: physical
              - id: i3
                label: donotuse2
                slot: 2
                type: physical
              - id: i4
                label: GigabitEthernet0/0/0/0
                slot: 3
                type: physical
          - boot_disk_size: 0
            configuration: |-
              hostname changeme
              username cisco
              group root-lr
              group cisco-support
              password cisco
              !
              username admin
              group root-lr
              group cisco-support
              password admin
              !
              username lab
              group root-lr
              group cisco-support
              password lab
              !
              end
            cpu_limit: 100
            cpus: 0
            data_volume: 0
            hide_links: false
            id: n2
            label: rtr-2
            node_definition: iosxrv9000
            ram: 0
            tags: []
            x: -300
            y: 50
            interfaces:
              - id: i0
                label: Loopback0
                type: loopback
              - id: i1
                label: MgmtEth0/RP0/CPU0/0
                slot: 0
                type: physical
              - id: i2
                label: donotuse1
                slot: 1
                type: physical
              - id: i3
                label: donotuse2
                slot: 2
                type: physical
              - id: i4
                label: GigabitEthernet0/0/0/0
                slot: 3
                type: physical
        """
        return response

    @staticmethod
    def download_alt_lab(req, ctx=None):
        response = """
        lab:
          description: ''
          notes: ''
          title: Other Lab
          version: 0.1.0
        links:
          - id: l0
            n1: n0
            n2: n1
            i1: i1
            i2: i1
            label: nxos9000-0-mgmt0<->xr9kv-0-MgmtEth0/RP0/CPU0/0
        nodes:
          - boot_disk_size: 0
            configuration: hostname inserthostname_here
            cpu_limit: 100
            cpus: 0
            data_volume: 0
            hide_links: false
            id: n0
            image_definition: nxosv9000-9-2-3
            label: nxos9000-0
            node_definition: nxosv9000
            ram: 0
            tags: []
            x: -450
            y: -50
            interfaces:
              - id: i0
                label: Loopback0
                type: loopback
              - id: i1
                label: mgmt0
                slot: 0
                type: physical
              - id: i2
                label: Ethernet1/1
                slot: 1
                type: physical
              - id: i3
                label: Ethernet1/2
                slot: 2
                type: physical
              - id: i4
                label: Ethernet1/3
                slot: 3
                type: physical
          - boot_disk_size: 0
            configuration: |-
              hostname changeme
              username cisco
              group root-lr
              group cisco-support
              password cisco
              !
              username admin
              group root-lr
              group cisco-support
              password admin
              !
              username lab
              group root-lr
              group cisco-support
              password lab
              !
              end
            cpu_limit: 100
            cpus: 0
            data_volume: 0
            hide_links: false
            id: n1
            image_definition: iosxrv9000-6-6-2
            label: xr9kv-0
            node_definition: iosxrv9000
            ram: 0
            tags: []
            x: -150
            y: -50
            interfaces:
              - id: i0
                label: Loopback0
                type: loopback
              - id: i1
                label: MgmtEth0/RP0/CPU0/0
                slot: 0
                type: physical
              - id: i2
                label: donotuse1
                slot: 1
                type: physical
              - id: i3
                label: donotuse2
                slot: 2
                type: physical
              - id: i4
                label: GigabitEthernet0/0/0/0
                slot: 3
                type: physical
        """
        return response

    @staticmethod
    def get_sys_info(req, ctx=None):
        response = {"version": "2.7.0+build.7", "ready": True}
        return response

    @staticmethod
    def auth_ok(req, ctx=None):
        return "OK"

    @staticmethod
    def authenticate(req, ctx=None):
        return "1234567890"

    @staticmethod
    def print_req(req, ctx=None):
        s = "!!!URL: {}, method = {}, params = {}".format(req.url, req.method, req.path)
        print(s)
        return s

    @staticmethod
    def get_lab_element_state(req, ctx=None):
        return MockCMLServer._get_lab_element_state(req, ctx)

    @staticmethod
    def get_lab_element_state_24(req, ctx=None):
        return MockCMLServer._get_lab_element_state_24(req, ctx)

    @staticmethod
    def get_lab_element_state_down(req, ctx=None):
        return MockCMLServer._get_lab_element_state(req, ctx, "STOPPED")

    @staticmethod
    def _get_lab_element_state(req, ctx=None, n2_state="BOOTED"):
        response = {
            "nodes": {"n0": "BOOTED", "n1": n2_state, "n2": "DEFINED_ON_CORE"},
            "links": {"l0": "STARTED"},
            "interfaces": {"i0": "STARTED", "i1": "STARTED", "i2": "STARTED", "i3": "STARTED", "i4": "STARTED", "i5": "STARTED"},
        }
        return response

    @staticmethod
    def _get_lab_element_state_24(req, ctx=None, n2_state="BOOTED"):
        response = {
            "nodes": {
                "88119b68-9d08-40c4-90f5-6dc533fd0255": "BOOTED",
                "88119b68-9d08-40c4-90f5-6dc533fd0256": n2_state,
                "88119b68-9d08-40c4-90f5-6dc533fd0257": "DEFINED_ON_CORE",
            },
            "links": {"88119b68-9d08-40c4-90f5-6dc533fd0259": "STARTED"},
            "interfaces": {
                "88119b68-9d08-40c4-90f5-6dc533fd020a": "STARTED",
                "88119b68-9d08-40c4-90f5-6dc533fd020b": "STARTED",
                "88119b68-9d08-40c4-90f5-6dc533fd020c": "STARTED",
                "88119b68-9d08-40c4-90f5-6dc533fd020d": "STARTED",
                "88119b68-9d08-40c4-90f5-6dc533fd020e": "STARTED",
                "88119b68-9d08-40c4-90f5-6dc533fd020f": "STARTED",
            },
        }
        return response

    @staticmethod
    def get_topology(req, ctx=None):
        response = {
            "nodes": [
                {
                    "id": "n0",
                    "data": {
                        "node_definition": "external_connector",
                        "image_definition": None,
                        "label": "Lab Net",
                        "configuration": "bridge0",
                        "x": -400,
                        "y": 0,
                        "state": "BOOTED",
                        "ram": None,
                        "cpus": None,
                        "cpu_limit": None,
                        "data_volume": None,
                        "boot_disk_size": None,
                        "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                        "tags": [],
                    },
                },
                {
                    "id": "n1",
                    "data": {
                        "node_definition": "iosxrv9000",
                        "image_definition": "iosxrv9000-6-6-2",
                        "label": "rtr-1",
                        "configuration": "hostname changeme\n",
                        "x": -200,
                        "y": -50,
                        "state": "BOOTED",
                        "ram": None,
                        "cpus": None,
                        "cpu_limit": None,
                        "data_volume": None,
                        "boot_disk_size": None,
                        "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                        "tags": [],
                    },
                },
                {
                    "id": "n2",
                    "data": {
                        "node_definition": "iosxrv9000",
                        "image_definition": "iosxrv9000-6-6-2",
                        "label": "rtr-2",
                        "configuration": "hostname changeme\n",
                        "x": -200,
                        "y": -50,
                        "state": "DEFINED_ON_CORE",
                        "ram": None,
                        "cpus": None,
                        "cpu_limit": None,
                        "data_volume": None,
                        "boot_disk_size": None,
                        "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                        "tags": [],
                    },
                },
            ],
            "links": [{"id": "l0", "interface_a": "i2", "interface_b": "i0", "data": {"state": "STARTED"}}],
            "interfaces": [
                {"id": "i0", "node": "n0", "data": {"label": "port", "slot": 0, "state": "STARTED", "type": "physical"}},
                {"id": "i1", "node": "n1", "data": {"label": "Loopback0", "slot": None, "state": "STARTED", "type": "loopback"}},
                {"id": "i2", "node": "n1", "data": {"label": "MgmtEth0/RP0/CPU0/0", "slot": 0, "state": "STARTED", "type": "physical"}},
                {"id": "i3", "node": "n1", "data": {"label": "donotuse1", "slot": 1, "state": "STARTED", "type": "physical"}},
                {"id": "i4", "node": "n1", "data": {"label": "donotuse2", "slot": 2, "state": "STARTED", "type": "physical"}},
                {"id": "i5", "node": "n1", "data": {"label": "GigabitEthernet0/0/0/0", "slot": 3, "state": "STARTED", "type": "physical"}},
            ],
            "lab": {
                "description": "",
                "notes": "",
                "owner": "00000000-0000-4000-a000-000000000000",
                "title": "Mock Test",
                "version": "0.1.0",
            },
        }
        return response

    @staticmethod
    def get_alt_topology(req, ctx=None):
        response = {
            "nodes": [
                {
                    "id": "n0",
                    "data": {
                        "node_definition": "nxosv9000",
                        "image_definition": "nxosv9000-9-2-3",
                        "label": "nxos9000-0",
                        "configuration": "hostname inserthostname_here",
                        "x": -450,
                        "y": -50,
                        "state": "STOPPED",
                        "ram": None,
                        "cpus": None,
                        "cpu_limit": None,
                        "data_volume": None,
                        "boot_disk_size": None,
                        "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                        "tags": [],
                    },
                },
                {
                    "id": "n1",
                    "data": {
                        "node_definition": "iosxrv9000",
                        "image_definition": "iosxrv9000-6-6-2",
                        "label": "xr9kv-0",
                        "configuration": "hostname changeme\n",
                        "x": -150,
                        "y": -50,
                        "state": "STOPPED",
                        "ram": None,
                        "cpus": None,
                        "cpu_limit": None,
                        "data_volume": None,
                        "boot_disk_size": None,
                        "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                        "tags": [],
                    },
                },
            ],
            "links": [{"id": "l0", "interface_a": "i1", "interface_b": "i6", "data": {"state": "STOPPED"}}],
            "interfaces": [
                {"id": "i0", "node": "n0", "data": {"label": "Loopback0", "slot": None, "state": "STOPPED", "type": "loopback"}},
                {"id": "i1", "node": "n0", "data": {"label": "mgmt0", "slot": 0, "state": "STOPPED", "type": "physical"}},
                {"id": "i2", "node": "n0", "data": {"label": "Ethernet1/1", "slot": 1, "state": "STOPPED", "type": "physical"}},
                {"id": "i3", "node": "n0", "data": {"label": "Ethernet1/2", "slot": 2, "state": "STOPPED", "type": "physical"}},
                {"id": "i4", "node": "n0", "data": {"label": "Ethernet1/3", "slot": 3, "state": "STOPPED", "type": "physical"}},
                {"id": "i5", "node": "n1", "data": {"label": "Loopback0", "slot": None, "state": "STOPPED", "type": "loopback"}},
                {"id": "i6", "node": "n1", "data": {"label": "MgmtEth0/RP0/CPU0/0", "slot": 0, "state": "STOPPED", "type": "physical"}},
                {"id": "i7", "node": "n1", "data": {"label": "donotuse1", "slot": 1, "state": "STOPPED", "type": "physical"}},
                {"id": "i8", "node": "n1", "data": {"label": "donotuse2", "slot": 2, "state": "STOPPED", "type": "physical"}},
                {"id": "i9", "node": "n1", "data": {"label": "GigabitEthernet0/0/0/0", "slot": 3, "state": "STOPPED", "type": "physical"}},
            ],
            "lab": {
                "description": "",
                "notes": "",
                "owner": "00000000-0000-4000-a000-000000000000",
                "title": "Other Lab",
                "version": "0.1.0",
            },
        }
        return response

    @staticmethod
    def get_topology_24(req, ctx=None):
        response = {
            "nodes": [
                {
                    "id": "88119b68-9d08-40c4-90f5-6dc533fd0255",
                    "data": {
                        "node_definition": "external_connector",
                        "image_definition": None,
                        "label": "Lab Net",
                        "configuration": "bridge0",
                        "x": -400,
                        "y": 0,
                        "state": "BOOTED",
                        "ram": None,
                        "cpus": None,
                        "cpu_limit": None,
                        "data_volume": None,
                        "boot_disk_size": None,
                        "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                        "tags": [],
                    },
                },
                {
                    "id": "88119b68-9d08-40c4-90f5-6dc533fd0256",
                    "data": {
                        "node_definition": "iosxrv9000",
                        "image_definition": "iosxrv9000-6-6-2",
                        "label": "rtr-1",
                        "configuration": "hostname changeme\n",
                        "x": -200,
                        "y": -50,
                        "state": "BOOTED",
                        "ram": None,
                        "cpus": None,
                        "cpu_limit": None,
                        "data_volume": None,
                        "boot_disk_size": None,
                        "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                        "tags": [],
                    },
                },
                {
                    "id": "88119b68-9d08-40c4-90f5-6dc533fd0257",
                    "data": {
                        "node_definition": "iosxrv9000",
                        "image_definition": "iosxrv9000-6-6-2",
                        "label": "rtr-2",
                        "configuration": "hostname changeme\n",
                        "x": -200,
                        "y": -50,
                        "state": "DEFINED_ON_CORE",
                        "ram": None,
                        "cpus": None,
                        "cpu_limit": None,
                        "data_volume": None,
                        "boot_disk_size": None,
                        "compute_id": "17e91b4e-865a-4627-a6bb-50e3dfa988ab",
                        "tags": [],
                    },
                },
            ],
            "links": [
                {
                    "id": "88119b68-9d08-40c4-90f5-6dc533fd0259",
                    "interface_a": "88119b68-9d08-40c4-90f5-6dc533fd020c",
                    "interface_b": "88119b68-9d08-40c4-90f5-6dc533fd020a",
                    "data": {"state": "STARTED"},
                }
            ],
            "interfaces": [
                {
                    "id": "88119b68-9d08-40c4-90f5-6dc533fd020a",
                    "node": "88119b68-9d08-40c4-90f5-6dc533fd0255",
                    "data": {"label": "port", "slot": 0, "state": "STARTED", "type": "physical"},
                },
                {
                    "id": "88119b68-9d08-40c4-90f5-6dc533fd020b",
                    "node": "88119b68-9d08-40c4-90f5-6dc533fd0256",
                    "data": {"label": "Loopback0", "slot": None, "state": "STARTED", "type": "loopback"},
                },
                {
                    "id": "88119b68-9d08-40c4-90f5-6dc533fd020c",
                    "node": "88119b68-9d08-40c4-90f5-6dc533fd0256",
                    "data": {"label": "MgmtEth0/RP0/CPU0/0", "slot": 0, "state": "STARTED", "type": "physical"},
                },
                {
                    "id": "88119b68-9d08-40c4-90f5-6dc533fd020d",
                    "node": "88119b68-9d08-40c4-90f5-6dc533fd0256",
                    "data": {"label": "donotuse1", "slot": 1, "state": "STARTED", "type": "physical"},
                },
                {
                    "id": "88119b68-9d08-40c4-90f5-6dc533fd020e",
                    "node": "88119b68-9d08-40c4-90f5-6dc533fd0256",
                    "data": {"label": "donotuse2", "slot": 2, "state": "STARTED", "type": "physical"},
                },
                {
                    "id": "88119b68-9d08-40c4-90f5-6dc533fd020f",
                    "node": "88119b68-9d08-40c4-90f5-6dc533fd0256",
                    "data": {"label": "GigabitEthernet0/0/0/0", "slot": 3, "state": "STARTED", "type": "physical"},
                },
            ],
            "lab": {
                "description": "",
                "notes": "",
                "owner": "00000000-0000-4000-a000-000000000000",
                "title": "Mock Test 2.4",
                "version": "0.1.0",
            },
        }
        return response

    @staticmethod
    def get_pyats_testbed(req, ctx=None):
        response = """
        testbed:
        name: lab
        devices:
        terminal_server:
        os: linux
        type: server
        credentials:
            default:
            username: change_me
            password: change_me
        connections:
            cli:
            protocol: ssh
            ip: localhost
            port: 22
        internet-rtr01:
        os: iosxe
        type: router
        platform: csr1000v
        credentials:
            default:
            username: cisco
            password: cisco
        connections:
            defaults:
            class: unicon.unicon
            a:
            protocol: telnet
            proxy: terminal_server
            command: open /lab/internet-rtr01/0
        internet-rtr01:
        interfaces:
            loopback0:
            type: loopback
            gigabitethernet1:
            link: 37486a17-1d4f-4235-910a-b90fe23d18e7
            type: ethernet
        """
        return response

    @staticmethod
    def get_users(req, ctx=None):
        response = [
            {
                "id": "00000000-0000-4000-a000-000000000000",
                "created": "2022-09-30T10:03:53+00:00",
                "modified": "2024-06-21T15:16:42+00:00",
                "username": "admin",
                "fullname": "",
                "email": "",
                "description": "",
                "admin": True,
                "directory_dn": "",
                "groups": [],
                "labs": [],
                "opt_in": True,
                "resource_pool": None,
                "tour_version": "2.6.1+build.11",
                "pubkey_info": "",
            },
            {
                "id": "9e4e75b4-aaab-47af-9edb-9364460a81ae",
                "created": "2024-06-19T20:29:02+00:00",
                "modified": "2024-06-21T10:42:20+00:00",
                "username": "user",
                "fullname": "",
                "email": "",
                "description": "",
                "admin": False,
                "directory_dn": "",
                "groups": ["48c9c605-552f-4666-bd23-5b68cf4de665"],
                "labs": [],
                "opt_in": True,
                "resource_pool": None,
                "tour_version": "",
                "pubkey_info": "",
            },
        ]

        return response
