class MockCMLServer(object):
    @staticmethod
    def get_lab_tiles(req, ctx):
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
                                "tags": [],
                            },
                        ],
                        "links": [{"id": "l0", "node_a": "n0", "node_b": "n1", "state": "STOPPED"}],
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
            "system_information": {"version": "2.1.0-b89.f8805559", "ready": True},
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
    def get_labs(req, ctx):
        response = ["5eaea5", "5f0d96"]
        return response

    @staticmethod
    def download_lab(req, ctx):
        response = """
        lab:
          description: ''
          notes: ''
          timestamp: 1597805276.8213837
          title: Mock Test
          version: 0.0.3
        nodes:
          - id: n0
            label: Lab Net
            node_definition: external_connector
            x: -400
            y: 0
            configuration: bridge0
            tags: []
            interfaces:
              - id: i0
                slot: 0
                label: port
                type: physical
          - id: n1
            label: rtr-1
            node_definition: iosxrv9000
            x: -200
            y: -50
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
            image_definition: iosxrv9000-6-6-2
            tags: []
            interfaces:
              - id: i0
                label: Loopback0
                type: loopback
              - id: i1
                slot: 0
                label: MgmtEth0/RP0/CPU0/0
                type: physical
              - id: i2
                slot: 1
                label: donotuse1
                type: physical
              - id: i3
                slot: 2
                label: donotuse2
                type: physical
              - id: i4
                slot: 3
                label: GigabitEthernet0/0/0/0
                type: physical
          - id: n2
            label: rtr-2
            node_definition: iosxrv9000
            x: -200
            y: -50
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
            image_definition: iosxrv9000-6-6-2
            tags: []
            interfaces:
              - id: i0
                label: Loopback0
                type: loopback
              - id: i1
                slot: 0
                label: MgmtEth0/RP0/CPU0/0
                type: physical
              - id: i2
                slot: 1
                label: donotuse1
                type: physical
              - id: i3
                slot: 2
                label: donotuse2
                type: physical
              - id: i4
                slot: 3
                label: GigabitEthernet0/0/0/0
                type: physical
        links:
          - id: l0
            i1: i1
            n1: n1
            i2: i0
            n2: n0
        """
        return response

    @staticmethod
    def download_alt_lab(req, ctx):
        response = """
        lab:
          description: ''
          notes: ''
          timestamp: 1595337039.0416706
          title: Other Lab
          version: 0.0.3
        nodes:
          - id: n0
            label: nxos9000-0
            node_definition: nxosv9000
            x: -450
            y: -50
            configuration: hostname inserthostname_here
            image_definition: nxosv9000-9-2-3
            tags: []
            interfaces:
              - id: i0
                label: Loopback0
                type: loopback
              - id: i1
                slot: 0
                label: mgmt0
                type: physical
              - id: i2
                slot: 1
                label: Ethernet1/1
                type: physical
              - id: i3
                slot: 2
                label: Ethernet1/2
                type: physical
              - id: i4
                slot: 3
                label: Ethernet1/3
                type: physical
          - id: n1
            label: xr9kv-0
            node_definition: iosxrv9000
            x: -150
            y: -50
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
            image_definition: iosxrv9000-6-6-2
            tags: []
            interfaces:
              - id: i0
                label: Loopback0
                type: loopback
              - id: i1
                slot: 0
                label: MgmtEth0/RP0/CPU0/0
                type: physical
              - id: i2
                slot: 1
                label: donotuse1
                type: physical
              - id: i3
                slot: 2
                label: donotuse2
                type: physical
              - id: i4
                slot: 3
                label: GigabitEthernet0/0/0/0
                type: physical
        links:
          - id: l0
            i1: i1
            n1: n0
            i2: i1
            n2: n1
        """
        return response

    @staticmethod
    def get_sys_info(req, ctx):
        response = {"version": "2.1.0", "ready": True}
        return response

    @staticmethod
    def auth_ok(req, ctx):
        return "OK"

    @staticmethod
    def authenticate(req, ctx):
        return "1234567890"

    @staticmethod
    def print_req(req, ctx):
        s = "!!!URL: {}, method = {}, params = {}".format(req.url, req.method, req.path)
        print(s)
        return s

    @staticmethod
    def get_lab_element_state(req, ctx):
        return MockCMLServer._get_lab_element_state(req, ctx)

    @staticmethod
    def get_lab_element_state_down(req, ctx):
        return MockCMLServer._get_lab_element_state(req, ctx, "STOPPED")

    @staticmethod
    def _get_lab_element_state(req, ctx, n2_state="BOOTED"):
        response = {
            "nodes": {"n0": "BOOTED", "n1": n2_state, "n2": "DEFINED_ON_CORE"},
            "links": {"l0": "STARTED"},
            "interfaces": {"i0": "STARTED", "i1": "STARTED", "i2": "STARTED", "i3": "STARTED", "i4": "STARTED", "i5": "STARTED"},
        }
        return response

    @staticmethod
    def get_topology(req, ctx):
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
            "lab_notes": "",
            "lab_title": "Mock Test",
            "lab_description": "",
            "state": "STARTED",
            "created_timestamp": 1597805276.8213837,
            "cluster_id": "cluster_1",
            "version": "0.0.3",
        }
        return response

    @staticmethod
    def get_alt_topology(req, ctx):
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
            "lab_notes": "",
            "lab_title": "Other Lab",
            "lab_description": "",
            "state": "STOPPED",
            "created_timestamp": 1595337039.0416706,
            "cluster_id": "cluster_1",
            "version": "0.0.3",
        }
        return response
