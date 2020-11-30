"""
Collection of utility classes to make getting credentials and
configuration easier.
"""
import getpass
import os
from virl.helpers import find_virl


def _get_from_user(prompt):  # pragma: no cover
    """
    Get the input from the user through interactive prompt.
    """
    resp = input(prompt)
    return resp


def _get_password(prompt):
    """
    Get the password from the user through interactive prompt.
    Using this will ensure that the password is not displayed as
    it is typed.
    """
    return getpass.getpass(prompt)


def _get_from_file(virlrc, prop_name):
    if os.path.isfile(virlrc):
        with open(virlrc) as fh:
            config = fh.readlines()

        for line in config:
            if line.startswith(prop_name):
                prop = line.split("=")[1].strip()
                if prop.startswith('"') and prop.endswith('"'):
                    prop = prop[1:-1]
                return prop


def get_prop(prop_name):
    """
    Gets a variable using the following order

    * Check for .virlrc in current directory

    * recurse up directory tree for .virlrc

    * Check environment variables

    * Check ~/.virlrc

    * Prompt user

    """
    # check for .virlrc in current directory
    cwd = os.getcwd()
    virlrc = os.path.join(cwd, ".virlrc")
    prop = _get_from_file(virlrc, prop_name)

    if prop:
        return prop

    # search up directory tree for a .virlrc
    virl_dir = find_virl()
    if virl_dir:
        virlrc = os.path.join(virl_dir, ".virlrc")
        prop = _get_from_file(virlrc, prop_name)

        if prop:
            return prop

    # try environment next
    prop = os.getenv(prop_name, None)
    if prop:
        return prop

    # check for .virlrc in home directory
    path = os.path.expanduser("~")
    virlrc = os.path.join(path, ".virlrc")
    prop = _get_from_file(virlrc, prop_name)

    return prop or None


def get_credentials(rcfile="~/.virlrc"):
    """
    Used to get the VIRL credentials

    * The login credentials are taken in the following order

    * Check for .virlrc in current directory

    * Check environment variables

    * Check ~/.virlrc

    * Prompt user

    """
    # initialize vars
    host = None
    username = None
    password = None
    config = dict()

    host = get_prop("VIRL_HOST")
    username = get_prop("VIRL_USERNAME")
    password = get_prop("VIRL_PASSWORD")

    # some additional configuration that can be set / overriden
    configurable_props = [
        "VIRL_TELNET_COMMAND",
        "VIRL_CONSOLE_COMMAND",
        "VIRL_SSH_COMMAND",
        "VIRL_SSH_USERNAME",
        "CML_CONSOLE_COMMAND",
        "CML2_PLUS",
        "CML_VERIFY_CERT",
        "CML_DEVICE_USERNAME",
        "CML_DEVICE_PASSWORD",
        "CML_DEVICE_ENABLE_PASSWORD",
        "CML_PLUGIN_PATH",
    ]

    for p in configurable_props:
        if get_prop(p):
            config[p] = get_prop(p)

    if not host:  # pragma: no cover
        prompt = "Please enter the IP / hostname of your virl server: "
        host = _get_from_user(prompt)

    if not username:  # pragma: no cover
        username = _get_from_user("Please enter your VIRL username: ")

    if not password:  # pragma: no cover
        password = _get_password("Please enter your password: ")

    if not all([host, username, password]):  # pragma: no cover
        print("Unable to determine CML/VIRL credentials, please see docs")
        exit(1)
    else:
        return (host, username, password, config)
