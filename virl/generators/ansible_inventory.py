from collections import OrderedDict
import yaml
from jinja2 import Environment, PackageLoader
from lxml import etree


def setup_yaml():
    """ https://stackoverflow.com/a/8661021 """
    represent_dict_order = lambda self, data:  self.represent_mapping('tag:yaml.org,2002:map', data.items()) # noqa
    yaml.add_representer(OrderedDict, represent_dict_order)


setup_yaml()


def create_group_map(virl_xmlstr):
    """
    retrieves ansible group information from `virl_xmlstr`
    returns a dictionary handy for determining the group that a node belongs to

    NOTE:  `virl_xmlstr` must be received from the VIRL API, not the virl file

    Ansible Groups are controlled by adding an extension to the VIRL XML file

    e.g

    <node name="router1" type="SIMPLE" subtype="CSR1000v">
        <extensions>
            <entry key="ansible_group" type="String">mygroup</entry>
        </extensions>
     </node>

     """
    root = etree.fromstring(virl_xmlstr)

    # get all ansible_groups
    groups = root.xpath("//virl:entry[@key='ansible_group']/text()",
                        namespaces={"virl": "http://www.cisco.com/VIRL"})
    groups = set(groups)
    group_map = dict()

    # populate nodes in correct groups
    for g in groups:
        # query returns a list strings representing the node names in group
        q = '//virl:node//virl:entry[text()="{}"]/ancestor::virl:node/@name'
        query = q.format(g)
        members = root.xpath(query,
                             namespaces={"virl": "http://www.cisco.com/VIRL"})
        # add to map so that hostnames can be resolved to groups later
        for m in members:
            group_map[m] = g

    return group_map


def generate_inventory_dict(virl_xml, roster=None, interfaces=None):
    """
    common inventory info accross yaml/ini
    """
    # create inventory skeleton
    inventory = dict()
    inventory['all'] = dict()
    inventory['all']['children'] = dict()
    inventory['all']['hosts'] = dict()

    for node_long_name, device in roster.items():
        # make sure we have at least enough info to be useful
        if ('managementIP') in device and ('NodeName' in device):
            entry = dict()
            entry['node_long_name'] = node_long_name
            entry['ansible_host'] = device['managementIP']
        # otherwise, skip this device
        else:
            continue

        name = device['NodeName']
        # map console ports if they are available
        if all(k in device for k in ("SimulationHost", "PortConsole")):
            entry['console_server'] = device['SimulationHost']
            entry['console_port'] = device['PortConsole']

        # determine device/os type
        try:
            type = device['NodeSubtype']
            if 'NX' in type:
                entry['device_type'] = 'nxos'
            elif 'XR' in type:
                entry['device_type'] = 'iosxr'
            elif 'CSR' in type:
                entry['device_type'] = 'ios'
            elif 'IOS' in type:
                entry['device_type'] = 'ios'

            else:
                entry['device_type'] = 'unknown'

        except KeyError:
            entry['device_type'] = 'unknown'

        # create data structure for resolving group name from node name
        group_map = create_group_map(virl_xml)
        # add group to children

        # try to map to ansible group
        try:
            group = group_map[name]
            print("Placing {} into ansible group {}".format(name, group))
            if group not in inventory['all']['children']:
                inventory['all']['children'][group] = dict()
            if name not in inventory['all']['children']:
                inventory['all']['children'][group][name] = entry

        # otherwise it will go in all:
        except: # noqa
            inventory['all']['hosts'][name] = entry

    # try:
    #     devices = interfaces[sim_name]
    # except KeyError:
    #     raise Exception('something went wrong')

    return inventory


def render_yaml_inventory(virl_xml, roster=None, interfaces=None):
    """
    we need to merge information from multiple sources to generate all
    the required parameters for the inventory

    """

    j2_env = Environment(loader=PackageLoader('virl'),
                         trim_blocks=False)

    inventory = generate_inventory_dict(virl_xml,
                                        roster=roster,
                                        interfaces=interfaces)
    template = j2_env.get_template('ansible/inventory_template.j2')
    return template.render(inventory=inventory)


def render_ini_inventory(virl_xml, roster=None, interfaces=None):
    """
    we need to merge information from multiple sources to generate all
    the required parameters for the inventory

    """

    j2_env = Environment(loader=PackageLoader('virl'),
                         trim_blocks=False)

    inventory = generate_inventory_dict(virl_xml,
                                        roster=roster,
                                        interfaces=interfaces)
    # pass all available data to template for rendering, this can probably
    # be pruned back at some point
    template = j2_env.get_template('ansible/inventory_ini_template.j2')
    return template.render(inventory=inventory)


def ansible_inventory_generator(env,
                                virl_data,
                                roster,
                                interfaces,
                                style="yaml"):
    """
    given a sim roster produces a inventory file suitable for
    use with ansible

    """
    if not all([virl_data, roster, interfaces]):
        raise ValueError("we really need virl_xml, roster, and interfaces")

    # sim_name should be the only key in the dictionary
    if len(interfaces.keys()) != 1:
        raise ValueError("too many keys in interface response")

    if style == "yaml":
        inventory_yaml = render_yaml_inventory(virl_data, roster, interfaces)
        return inventory_yaml
    elif style == "ini":
        inventory_ini = render_ini_inventory(virl_data, roster, interfaces)
        return inventory_ini
