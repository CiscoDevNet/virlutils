"""
Collection of utility classes to make getting credentials and configuration easier.
"""
import getpass
import os
import sys
import inspect


def _get_from_user(prompt):
    """
    Get the input from the user through interactive prompt.
    Use raw_input or input based on the Python version.
    """
    try:
        resp = raw_input(prompt)
    except NameError:
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
                prop = line.split('=')[1].strip()
                return prop


def get_prop(prop_name):
    """
    Gets a variable using the following order

    * Check for .virlrc in current directory

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

    # try environment next
    prop = os.getenv(prop_name, None)
    if prop:
        return prop

    #check for .virlrc in home directory
    path = os.path.expanduser("~")
    virlrc = os.path.join(path, ".virlrc")
    prop = _get_from_file(virlrc, prop_name)

    return prop or None


def get_credentials(rcfile='~/.virlrc'):
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

    host = get_prop('VIRL_HOST')
    username = get_prop('VIRL_USERNAME')
    password = get_prop('VIRL_PASSWORD')
    if not host:
        host = _get_from_user('Please enter the IP / hostname of your virl server: ')

    if not username:
        username = _get_from_user("Please enter your VIRL username: ")

    if not password:
        password = _get_password("Please enter your password: ")

    if not all([host, username, password]):
        sys.exit("Unable to determine VIRL credentials, please see docs for configuring")
    else:
        return (host, username, password)
