import click
import random
import string
import os
import shutil
import errno
import ctypes
import platform


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
        else: raise  # noqa


def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')


def store_sim_info(name, env='default'):
    with safe_open_w('./.virl/{}/id'.format(env)) as f:
        f.write(name)


def remove_sim_info(env='default'):
    path = './.virl/{}'.format(env)
    click.secho("Removing {}".format(path))
    try:
        shutil.rmtree(path)
    except OSError:
        click.secho("Could not remove {}".format(path))


def generate_sim_id():
    letters = string.ascii_letters
    digits = string.digits
    return ''.join(random.choice(letters + digits) for _ in range(6))


def get_env_sim_name(env):
    fname = './.virl/{}/id'.format(env)
    with open(fname, 'r') as f:
        sim_name = f.read()

    return sim_name


def check_sim_running(env):
    """
    determines if a sim is already running for a given environment
    """
    try:
        fname = './.virl/{}/id'.format(env)
        with open(fname, 'r') as f:
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
        if k.endswith('mgmt-lxc'):
            lxc_ip = v.get('externalAddr', None)
            print("lxc is at {}".format(lxc_ip))
    return lxc_ip


def get_node_from_roster(name, roster):
    for k, v in roster.items():
        if k.endswith(name):
            return v
