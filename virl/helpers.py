import click
import random
import string
import os
import shutil
import errno
import platform
import ctypes
from virl2_client import ClientLibrary


# http://code.activestate.com/recipes/578035-disable-file-system-redirector/
# https://github.com/CiscoDevNet/virlutils/issues/45
class disable_file_system_redirection:
    if platform.system() == "Windows":
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))

    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise  # noqa


def safe_open_w(path):
    """ Open "path" for writing, creating any parent directories as needed.
    """
    mkdir_p(os.path.dirname(path))
    return open(path, "w")


def store_sim_info(name, env="default"):
    with safe_open_w("./.virl/{}/id".format(env)) as f:
        f.write(name)


def remove_sim_info(env="default"):
    path = "./.virl/{}".format(env)
    click.secho("Removing {}".format(path))
    try:
        shutil.rmtree(path)
    except OSError:
        click.secho("Could not remove {}".format(path))


def generate_sim_id():
    letters = string.ascii_letters
    digits = string.digits
    return "".join(random.choice(letters + digits) for _ in range(6))


def get_env_sim_name(env):
    fname = "./.virl/{}/id".format(env)
    with open(fname, "r") as f:
        sim_name = f.read()

    return sim_name


def find_virl():
    pwd = os.getcwd().split(os.sep)
    root = os.path.abspath(os.sep)
    while pwd != root:
        if platform.system() == "Windows":
            lookin = "\\".join(pwd)
        else:
            lookin = os.path.join(os.sep, *pwd)
        if ".virl" in os.listdir(lookin):
            return lookin
        try:
            pwd.pop()
        except IndexError:
            return None


def check_sim_running(env):
    """
    determines if a sim is already running for a given environment
    """
    try:
        virl_root = find_virl()
        fname = virl_root + "/.virl/{}/id".format(env)
        with open(fname, "r") as f:
            sim_name = f.read()
        if sim_name:
            return sim_name
        else:
            return None
    except Exception:
        return None


def get_mgmt_lxc_ip(sim_roster):
    # grab mgmt-lxc info in case we need it later
    for k, v in sim_roster.items():
        if k.endswith("mgmt-lxc"):
            lxc_ip = v.get("externalAddr", None)
            print("lxc is at {}".format(lxc_ip))
    return lxc_ip


def get_node_from_roster(name, roster):
    for k, v in roster.items():
        if k.endswith(name):
            return v


"""
CML helper functions
"""


def get_cache_root():
    """
    get the path to the directory to store cached labs
    """
    virl_root = find_virl()
    return virl_root + "/.virl/cached_cml_labs"


def get_current_lab_link():
    """
    get the path to the symlink representing the current lab
    """
    virl_root = find_virl()
    return virl_root + "/.virl/current_cml_lab"


def safe_join_existing_lab(lab_id, client):
    """
    gets a lab by its ID only if it exists on the server
    """
    if lab_id in client.get_lab_list():
        return client.join_existing_lab(lab_id)

    return None


def safe_join_existing_lab_by_title(lab_name, client):
    """
    gets a lab ID using its name/title

    This will return None if multiple labs exist for a given name/title.
    Since CML allows duplicate titles, we don't know what the user may want.
    """
    labs = client.find_labs_by_title(lab_name)
    if len(labs) == 1:
        return labs[0]

    return None


def check_lab_active(lab):
    """
    check if a lab is active on a CML server
    """

    # XXX: We need this because lab.is_active() is currently broken.
    return lab.state() in {"STARTED", "QUEUED", "BOOTED"}


def check_lab_cache(lab_id):
    """
    determines if a given lab ID is in the local topology cache
    """
    try:
        cache_root = get_cache_root()
        fname = "{}/{}".format(cache_root, lab_id)
        if os.path.exists(fname):
            return fname
    except Exception:
        return None

    return None


def cache_lab(lab):
    """
    save a topology YAML file into a local cache
    """
    topo = None
    topo = lab.download()

    cache_root = get_cache_root()
    fname = "{}/{}".format(cache_root, lab.id)
    if not os.path.exists(fname):
        with safe_open_w(fname) as fd:
            fd.write(topo)


def set_current_lab(lab_id):
    """
    creates a link to the cached lab to say it's current
    """

    cache_root = get_cache_root()
    fname = "{}/{}".format(cache_root, lab_id)
    if not os.path.exists(fname):
        raise FileNotFoundError("Failed to find cached lab for ID {}".format(lab_id))

    # This is supported on Windows and Unix as of Python 3.2
    # provided a new enough version of Windows.
    target = get_current_lab_link()
    clear_current_lab()
    os.symlink(fname, target)


def get_current_lab():
    """
    gets the current lab on which we're operating
    """

    lname = get_current_lab_link()
    if os.path.exists(lname):
        return os.path.basename(os.readlink(lname))

    return None


def clear_current_lab(lab_id=None):
    """
    unsets the current lab
    """
    lname = get_current_lab_link()
    if os.path.exists(lname):
        if lab_id is None or lab_id == get_current_lab():
            os.remove(lname)


def get_cml_client(server):
    """
    Helper function to get a consistent CML client library object
    """

    ssl_verify = True

    if "VIRL_VERIFY_CERT" in os.environ:
        if os.environ["VIRL_VERIFY_CERT"].lower() == "false":
            ssl_verify = False
        else:
            ssl_verify = os.environ["VIRL_VERIFY_CERT"]
    elif "CA_BUNDLE" in os.environ:
        ssl_verify = os.environ["CA_BUNDLE"]

    return ClientLibrary(server.host, server.user, server.passwd, ssl_verify=ssl_verify)
