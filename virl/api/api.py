import requests
import os

class VIRLServer(object):

    def __init__(self, host=None, user=None, passwd=None, port=19399):
        if not host:
            host = os.getenv('VIRL_HOST')
        if not user:
            user = os.getenv('VIRL_USERNAME', 'guest')
        if not passwd:
            passwd = os.getenv('VIRL_PASSWORD', 'guest')
        self._host = host
        self._user = user
        self._passwd = passwd
        self._port = port
        self.base_api = "http://{}:{}".format(self.host, self._port)

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def passwd(self):
        return self._user

    @passwd.setter
    def passwd(self, passwd):
        self._passwd = passwd

    @property
    def _headers(self):
        return {"Content-Type": "text/xml;charset=UTF-8"}

    def get(self, url):
        r = requests.get(url, auth=(self.user, self.passwd), headers=self._headers)
        return r

    def post(self, url, data):
        r = requests.post(url, auth=(self.user, self.passwd), headers=self._headers, data=data)
        return r

    def list_simulations(self):
        url = self.base_api + "/simengine/rest/list"
        r = requests.get(url, auth=(self.user, self.passwd))
        return r.json()["simulations"]

    def launch_simulation(self, simulation_name, simulation_data):
        u = self.base_api + "/simengine/rest/launch?session={}".format(simulation_name)
        headers = {"Content-Type": "text/xml;charset=UTF-8"}
        r = self.post(u, simulation_data)
        return r

    def stop_simulation(self, simulation):
        u = self.base_api + "/simengine/rest/stop/{}".format(simulation)
        r = self.get(u)
        return r

    def get_nodes(self, simulation):
        url = self.base_api + "/simengine/rest/nodes/{}".format(simulation)
        r = requests.get(url, auth=(self.user, self.passwd))
        return r.json()[simulation]

    def export(self, simulation, ip=False):
        """
        export simulation to local virl file
        """
        url = self.base_api + "/simengine/rest/export/{}".format(simulation)
        url += "?running-configs=config"
        if ip:
            url += "&updated=true"
        r = requests.get(url, auth=(self.user, self.passwd))
        return r


    def get_node_console(self, simulation, node=None, mode='telnet', port='0'):
        u = self.base_api + "/simengine/rest/serial_port/{}".format(simulation)
        u += "?mode={}&?port={}".format(mode, port)
        if node is not None:
            u += "&nodes={}".format(node)
        r = self.get(u)
        return r

    def get_logs(self, simulation):
        u = self.base_api + "/simengine/rest/events/{}".format(simulation)
        r = self.get(u)
        return r

    def get_sim_roster(self, simulation):
        """
        return a roster entry for given sim
        """
        sim_key = "{}|{}|".format(self.user, simulation)
        u = self.base_api + "/roster/rest"
        r = self.get(u)
        roster = r.json()
        ret = dict()
        for sim in roster.keys():
            if sim.startswith(sim_key):
                ret[sim] = roster[sim]
        return ret

    # def stop_nodes(self, simulation, nodes):
    #     u = simengine_host + "/simengine/rest/update/{}/stop?".format(simulation)
    #     node_list = []
    #     for node in nodes.keys():
    #         node_list.append("nodes={}".format(node))
    #     node_list = "&".join(node_list)
    #     u += node_list
    #     r = requests.put(u, auth=(virl_user, virl_password))
    #     return r.json()
    #
    # def start_nodes(simulation, nodes):
    #     u = simengine_host + "/simengine/rest/update/{}/start?".format(simulation)
    #     node_list = []
    #     for node in nodes.keys():
    #         node_list.append("nodes={}".format(node))
    #     node_list = "&".join(node_list)
    #     u += node_list
    #     r = requests.put(u, auth=(virl_user, virl_password))
    #     return r.json()
    #
    # def test_node_state(simulation, target_state, test_nodes=None):
    #     nodes = get_nodes(simulation)
    #     if test_nodes == None:
    #         test_nodes = nodes
    #     for node in test_nodes.keys():
    #         if not nodes[node]["state"] == target_state:
    #             return False
    #     return True

    #
    # def kill_simulation(simulation):
    #     u = simengine_host + "/simengine/rest/stop/{}".format(simulation)
    #     r = requests.get(u, auth=(virl_user, virl_password))
    #     return "{} {}".format(r.status_code, r.text)
    #
    # def launch_simulation(simulation_name, simulation_data):
    #     u = simengine_host + "/simengine/rest/launch?session={}".format(simulation_name)
    #     headers = {"Content-Type": "text/xml;charset=UTF-8"}
    #     r = requests.post(u, auth=(virl_user, virl_password), headers = headers, data = simulation_data)
    #     return "{} {}".format(r.status_code, r.text)
