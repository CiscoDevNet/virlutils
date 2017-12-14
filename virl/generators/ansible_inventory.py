import os
from collections import OrderedDict
from virl.api import VIRLServer
from virl import helpers
import yaml
from jinja2 import Environment, FileSystemLoader, PackageLoader
import os

def setup_yaml():
  """ https://stackoverflow.com/a/8661021 """
  represent_dict_order = lambda self, data:  self.represent_mapping('tag:yaml.org,2002:map', data.items())
  yaml.add_representer(OrderedDict, represent_dict_order)

setup_yaml()


def render_inventory(virl_xml, roster=None, interfaces=None):
    """
    we need to merge information from multiple sources to generate all
    the required parameters for the topology key in the testbed yaml config

    """
    if not all([virl_xml, roster, interfaces]):
        raise ValueError("we really need virl_xml, roster, and interfaces")

    # sim_name should be the only key in the dictionary
    if len(interfaces.keys()) != 1:
        raise ValueError("too many keys in interface response")

    sim_name = list(interfaces)[0]

    try:
        devices = interfaces[sim_name]
    except KeyError:
        raise Exception('something went wrong')

    j2_env = Environment(loader=PackageLoader('virl'),
                         trim_blocks=False)


    # create some tests for use in the templates
    # virl has a lot of node types, and all of them
    # may not be applicable to ansible
    def is_server(field):
        subtype = field.get("NodeSubtype")
        server_subtypes = ['mgmt-lxc']
        return subtype and (subtype in server_subtypes)

    def is_net_device(field):
        subtype = field.get("NodeSubtype")
        # for now we will exclude known bad and assume everything else is ok
        bad_subtypes = ['mgmt-lxc', 'LXC FLAT']
        return subtype and (subtype not in bad_subtypes)

    j2_env.tests['server'] = is_server
    j2_env.tests['net_device'] = is_net_device

    # pass all available data to template for rendering
    inventory = j2_env.get_template('ansible/inventory_template.j2').render(devices=devices,
                                                                     roster=roster,
                                                                     interfaces=interfaces,
                                                                     sim_name=sim_name)
    return inventory


def ansible_inventory_generator(env, virl_data, roster, interfaces):
    """
    given a sim roster produces a inventory file suitable for
    use with ansible

    """
    inventory_yaml = render_inventory(virl_data, roster, interfaces)
    return inventory_yaml
