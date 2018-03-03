import click
import random
import string
import os
import shutil
import errno

# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

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
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

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
    except Exception as e:
        return None
