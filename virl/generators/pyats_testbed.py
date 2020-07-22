from collections import OrderedDict
import yaml
from jinja2 import Environment, PackageLoader


def render_topl_template(devices):
    """
    renders topology: section of testbed yaml
    """
    pass


def setup_yaml():
    """ https://stackoverflow.com/a/8661021 """
    represent_dict_order = lambda self, data: self.represent_mapping("tag:yaml.org,2002:map", data.items())  # noqa
    yaml.add_representer(OrderedDict, represent_dict_order)


setup_yaml()


def render_testbed_template(name, servers, devices, topo_devs, conn_class="unicon.Unicon"):
    """
    we need to merge information from multiple sources to generate all
    the required parameters for the topology key in the testbed yaml config

    """
    # sim_name should be the only key in the dictionary
    if len(topo_devs.keys()) != 1:
        raise ValueError("too many keys in topo data")

    sim_name = list(topo_devs)[0]

    try:
        topology = topo_devs[sim_name]
    except KeyError:
        raise Exception("something went wrong")

    j2_env = Environment(loader=PackageLoader("virl"), trim_blocks=False)
    template = j2_env.get_template("pyats/testbed_yaml.j2")
    return template.render(name=sim_name, conn_class=conn_class, servers=servers, devices=devices, topology=topology)


def pyats_testbed_generator1(env, virl_data, roster, interfaces, dev_username="cisco", dev_password="cisco", conn_class="unicon.Unicon"):
    """
    given a sim roster produces a testbed file suitable for
    use with pyats
    """

    # generate a device dictionary for each device
    name = env + "_testbed"

    devices = dict()
    servers = dict()
    topology = interfaces

    for device, props in roster.items():
        # gather information about the device
        virl_server = str(props.get("SimulationHost", None))
        device_type = str(props.get("NodeSubtype", None))
        device_name = str(props.get("NodeName", None))
        console_port = str(props.get("PortConsole", None))

        # map node types to known abstraction
        os = None
        if "NX" in device_type:
            os = "nxos"
        elif "XR" in device_type:
            os = "iosxr"
        elif "CSR" in device_type:
            os = "iosxe"
        elif "IOS" in device_type:
            os = "ios"
        elif "IOS" in device_type:
            os = "ios"
        elif "ASAv" in device_type:
            os = "asa"

        # we prefer external addr
        external_ip = str(props.get("externalAddr", ""))
        mgmt_ip = str(props.get("managementIP", ""))
        if len(external_ip) > 6:
            address = external_ip
        elif len(mgmt_ip) > 6:
            address = mgmt_ip

        # add server devices to testbed->server section
        if device_type in ["mgmt-lxc", "server", "lxc"]:
            servers[device_name] = dict()
            servers[device_name]["server"] = device_name
            servers[device_name]["address"] = address
            servers[device_name]["path"] = ""
            continue

        # some devices can't conform
        elif device_type in ["LXC FLAT"]:
            continue
        # all other devices
        else:
            if device_name == "None":
                continue
            devices[device_name] = dict()
            devices[device_name]["alias"] = device_name
            if os:
                devices[device_name]["os"] = os

            devices[device_name]["type"] = device_type
            devices[device_name]["platform"] = device_type
            devices[device_name]["tacacs"] = {"username": dev_username}
            devices[device_name]["passwords"] = {"tacacs": dev_password, "enable": dev_password, "line": dev_password}
            devices[device_name]["connections"] = OrderedDict()

            devices[device_name]["connections"]["console"] = OrderedDict()
            console_info = {"protocol": "telnet", "ip": virl_server, "port": console_port}
            devices[device_name]["connections"]["console"] = console_info

    topology_yaml = render_testbed_template(name, servers, devices, topology, conn_class=conn_class)

    return topology_yaml


def pyats_testbed_generator(lab):
    return lab.get_pyats_testbed()
