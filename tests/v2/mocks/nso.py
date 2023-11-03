class MockNSOServer:
    @classmethod
    def launch_simulation(cls):
        response = u"TEST_ENV"
        return response

    @classmethod
    def get_node_console(cls):
        sim_response = {u"router2": u"10.94.241.194:17002", u"router1": u"10.94.241.194:17001"}
        return sim_response

    @classmethod
    def update_devices(cls):
        return {}

    @classmethod
    def perform_sync_from(cls):
        response = {"tailf-ncs:output": {"sync-result": [{"device": "router1", "result": True}, {"device": "router2", "result": True}]}}
        return response

    @classmethod
    def get_module_list(cls):
        response = {
            "ietf-yang-library:module": [
                {
                    "name": "cisco-ios-cli-6.42",
                    "revision": "",
                    "schema": "http://localhost:8080/restconf/tailf/modules/cisco-ios-cli-6.42",
                    "namespace": "http://tail-f.com/ns/ned-id/cisco-ios-cli-6.42",
                    "conformance-type": "import",
                },
            ],
        }
        return response

    @classmethod
    def get_ned_list(cls):
        response = {
            "tailf-ncs:ned-id": [
                {
                    "id": "cisco-ios-cli-6.42:cisco-ios-cli-6.42",
                    "module": [
                        {"name": "ietf-interfaces", "revision": "2014-05-08", "namespace": "urn:ietf:params:xml:ns:yang:ietf-interfaces"},
                        {"name": "ietf-ip", "revision": "2014-06-16", "namespace": "urn:ietf:params:xml:ns:yang:ietf-ip"},
                        {"name": "tailf-ned-cisco-ios", "revision": "2020-01-03", "namespace": "urn:ios"},
                        {"name": "tailf-ned-cisco-ios-id", "namespace": "urn:ios-id"},
                        {"name": "tailf-ned-cisco-ios-stats", "namespace": "urn:ios-stats"},
                    ],
                },
            ],
        }
        return response
