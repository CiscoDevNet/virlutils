import requests
from .credentials import get_credentials


class VIRLServer(object):

    def __init__(self, host=None, user=None, passwd=None, port=19399):

        self._host, self._user, self._passwd, self._config = get_credentials()
        self._port = port
        self.base_api = "http://{}:{}".format(self.host, self._port)

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

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

    @property
    def config(self):
        return self._config

    def get(self, url):
        r = requests.get(url,
                         auth=(self.user, self.passwd),
                         headers=self._headers)
        r.raise_for_status()
        return r

    def get_version(self):
        url = self.base_api + "/roster/rest/test"
        r = self.get(url)
        return r.json()

    def post(self, url, data):
        r = requests.post(url,
                          auth=(self.user, self.passwd),
                          headers=self._headers,
                          data=data)
        r.raise_for_status()
        return r

    def put(self, url, data):
        r = requests.put(url,
                         auth=(self.user, self.passwd),
                         headers=self._headers,
                         data=data)
        r.raise_for_status()
        return r

    def post_with_params(self, url, data, params):
        r = requests.post(url,
                          auth=(self.user, self.passwd),
                          headers=self._headers,
                          params=params,
                          data=data)
        r.raise_for_status()
        return r

    def delete(self, url):
        r = requests.delete(url,
                            auth=(self.user, self.passwd),
                            headers=self._headers)
        r.raise_for_status()
        return r

    def list_simulations(self):
        url = self.base_api + "/simengine/rest/list"
        r = self.get(url)
        return r.json()["simulations"]

    def launch_simulation(self, simulation_name, simulation_data):
        u = self.base_api + "/simengine/rest/launch?session={}"
        u = u.format(simulation_name)
        r = self.post(u, simulation_data)
        return r

    def stop_simulation(self, simulation):
        u = self.base_api + "/simengine/rest/stop/{}".format(simulation)
        r = self.get(u)
        return r

    def get_node_summary(self, simulation):
        url = self.base_api + "/simengine/rest/nodes/{}".format(simulation)
        r = requests.get(url, auth=(self.user, self.passwd))
        nodes = r.json()[simulation]
        return nodes

    def get_node_list(self, simulation):
        """
        returns a list of node,status tuples
        """
        nodes = self.get_node_summary(simulation)
        return nodes.keys()

    def check_node_reachable(self, simulation, node_name):
        """
        returns a list of node,status tuples
        """
        nodes = self.get_node_summary(simulation)
        return nodes[node_name]['reachable']

    def export(self, simulation, ip=False):
        """
        export simulation to local virl file
        """
        url = self.base_api + "/simengine/rest/export/{}".format(simulation)
        url += "?running-configs=config"
        if ip:
            url += "&updated=true"
        r = self.get(url)
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
        u = self.base_api + "/roster/rest/"
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
        u = self.base_api + '/simengine/rest/interfaces/{}'
        u = u.format(simulation_name)
        r = self.get(u)
        return r

    def stop_node(self, simulation, node):
        """
        stops a `node` in `simulation`
        """
        u = self.base_api + "/simengine/rest/update/{}/stop?nodes={}"
        u = u.format(simulation, node)
        r = self.put(u, None)
        return r

    def start_node(self, simulation, node):
        """
        stops a `node` in `simulation`
        """
        u = self.base_api + "/simengine/rest/update/{}/start?nodes={}"
        u = u.format(simulation, node)
        r = self.put(u, None)
        return r

    def get_gateway_for_network(self, network):
        u = self.base_api + "/openstack/rest/networks"
        r = self.get(u)
        for net in r.json():
            if net.get("Network Name") == network:
                return net["Gateway"]
        return None

    def get_dns_server_for_network(self, network):
        u = self.base_api + "/openstack/rest/networks"
        r = self.get(u)
        for net in r.json():
            if net.get("Network Name") == network:
                try:
                    return net["DNS"][0]
                except IndexError:
                    return None
        return None

    def get_flavor_id(self, flavor):
        r = self.get_flavors()

        for f in list(r):
            if f['name'] == flavor:
                return f['id']

        raise IndexError('Flavor {} not found'.format(flavor))

    def get_flavors(self, flavor_id=None):
        u = self.base_api + "/rest/flavors"

        if flavor_id is not None:
            u = u + "/{}".format(flavor_id)
        r = self.get(u)

        if flavor_id:
            return r.json()['flavor']
        return r.json()['flavors']

    def add_flavor(self, flavor=None, memory=None, vcpus=None):
        u = self.base_api + "/rest/flavors"
        data = {
            'name': flavor,
            'ram': memory,
            'vcpus': vcpus,
        }
        r = self.post_with_params(u, None, data)
        return r.json()['flavor']

    def delete_flavor(self, flavor):
        f = self.get_flavor_id(flavor)
        u = self.base_api + "/rest/flavors/{}"
        u = u.format(f)
        r = self.delete(u)
        return r.json()['flavor']
