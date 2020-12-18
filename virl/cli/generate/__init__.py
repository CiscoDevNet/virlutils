import click
from virl.api import plugin, check_valid_plugin, NoPluginError
from virl.cli.generate.ansible.commands import ansible, ansible1
from virl.cli.generate.pyats.commands import pyats, pyats1
from virl.cli.generate.nso.commands import nso, nso1


@click.group()
def generate():
    """
    generate inv file for various tools
    """
    pass


@click.group()
def generate1():
    """
    generate inv file for various tools
    """
    pass


generate1.add_command(ansible1, name="ansible")
generate1.add_command(pyats1, name="pyats")
generate1.add_command(nso1, name="nso")


def init_generators():
    generate.add_command(ansible)
    generate.add_command(pyats)
    generate.add_command(nso)

    for gen in plugin.Plugin.get_plugins("generator"):
        try:
            pl = plugin.GeneratorPlugin(generator=gen)
        except NoPluginError:
            continue
        if not check_valid_plugin(pl, pl.generate, "generate"):
            click.secho(
                "ERROR: Malformed plugin for generator {}.  The `generate` method must be static and a click.command".format(gen), fg="red"
            )
            plugin.Plugin.remove_plugin("generator", gen)
        else:
            generate.add_command(pl.generate, name=gen)
