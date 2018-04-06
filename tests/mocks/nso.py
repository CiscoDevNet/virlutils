class MockNSOServer:

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
    def update_devices(cls):
        return {}

    @classmethod
    def perform_sync_from(cls):
        response = {
            "tailf-ncs:output": {
                "sync-result": [
                    {
                        "device": "router1",
                        "result": True
                    },
                    {
                        "device": "router2",
                        "result": True
                    }
                ]
            }
        }
        return response
