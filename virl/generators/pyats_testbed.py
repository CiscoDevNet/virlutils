from collections import OrderedDict
import yaml
from jinja2 import Environment, PackageLoader


def render_topl_template(devices):
    """
    renders topology: section of testbed yaml
    """
    pass


def setup_yaml():
    """https://stackoverflow.com/a/8661021"""
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


def pyats_testbed_generator(lab):
    return lab.get_pyats_testbed()
