import requests
import os
from .credentials import get_credentials
# TODO implement common credentials module
# TODO implement basic models for the objects (swagger-gen)
# TODO catch errors at VIRLServer().get() and VIRLServer().post()

class VIRLServer(object):

    def __init__(self, host=None, user=None, passwd=None, port=19399):

        self._host, self._user, self._passwd = get_credentials()
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
        return self._passwd

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

    def put(self, url, data):
        r = requests.put(url, auth=(self.user, self.passwd), headers=self._headers, data=data)
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

    def get_interfaces(self, simulation_name):
        """
        returns all interfaces for a simulation
        """
        u = self.base_api + '/simengine/rest/interfaces/{}'.format(simulation_name)
        r = self.get(u)
        return r

    def stop_node(self, simulation, node):
        """
        stops a `node` in `simulation`
        """
        u = self.base_api + "/simengine/rest/update/{}/stop?nodes={}".format(simulation, node)
        r = self.put(u, None)
        return r

    def start_node(self, simulation, node):
        """
        stops a `node` in `simulation`
        """
        u = self.base_api + "/simengine/rest/update/{}/start?nodes={}".format(simulation, node)
        r = self.put(u, None)
        return r
