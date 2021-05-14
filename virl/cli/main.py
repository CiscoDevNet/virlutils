import click
from virl.api import VIRLServer, load_plugins, CommandPlugin, Plugin, check_valid_plugin, NoPluginError
from virl.helpers import get_default_plugin_dir
import requests
from urllib3.exceptions import InsecureRequestWarning
import warnings
import virl2_client
import traceback
from virl.helpers import get_cml_client, get_command
from .console.commands import console, console1  # noqa: F401
from .nodes.commands import nodes, nodes1  # noqa: F401
from .logs.commands import logs1  # noqa: F401
from .up.commands import up, up1  # noqa: F401
from .use.commands import use, use1  # noqa: F401
from .down.commands import down, down1  # noqa: F401
from .ls.commands import ls, ls1  # noqa: F401
from .save.commands import save, save1  # noqa: F401
from .telnet.commands import telnet, telnet1  # noqa: F401
from .ssh.commands import ssh, ssh1  # noqa: F401
from .generate import generate, generate1, init_generators  # noqa: F401
from .start.commands import start, start1  # noqa: F401
from .stop.commands import stop, stop1  # noqa: F401
from .pull.commands import pull, pull1  # noqa: F401
from .search.commands import search  # noqa: F401
from .swagger.commands import swagger1  # noqa: F401
from .uwm.commands import uwm1  # noqa: F401
from .viz.commands import viz1  # noqa: F401
from .id.commands import lid, sid  # noqa: F401
from .version.commands import version, version1  # noqa: F401
from .flavors import flavors1  # noqa: F401
from .definitions import definitions  # noqa: F401
from .cockpit.commands import cockpit  # noqa: F401
from .wipe import wipe  # noqa: F401
from .extract.commands import extract  # noqa: F401
from .clear.commands import clear  # noqa: F401
from .ui.commands import ui  # noqa: F401
from .license import license  # noqa: F401
from .rm.commands import rm  # noqa: F401
from .command.commands import command  # noqa: F401


class CatchAllExceptions(click.Group):
    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except Exception as exc:
            click.secho("Exception raised while running your command", fg="red")
            if not virl.debug:
                click.secho(
                    "Please re-run as '{} --debug ...' and collect the output before opening an issue".format(get_command()),
                    fg="red",
                )
            else:
                click.secho("Please open an issue and provide this output:", fg="red")
            click.secho("%s" % exc, fg="red")
            if virl.debug:
                click.secho(traceback.format_exc(), fg="red")
            exit(1)


@click.group(cls=CatchAllExceptions)
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Print any debugging output.",
    required=False,
)
def virl(**kwargs):
    if kwargs.get("debug"):
        virl.debug = True

    # We need to pull this out or subcommands fail.
    kwargs.pop("debug", None)


# Shall we print any debugging output?
virl.debug = False


def __get_server_ver():
    """
    Taste a VIRL/CML server and try and determine its version.
    This tries the 2.x flow and assumes 1.x if that flow fails in an
    unexpected way.  The reason for this is that compatibility with 1.x
    is stressed, but the code has been factored in a way so that the 1.x
    code can be removed when the time is right.

    Returns:
        string: Either '1' for VIRL/CML 1.x or the empty string for CML 2+
    """
    res = ""
    try:
        server = VIRLServer()
        if "CML2_PLUS" not in server.config:
            # If the user hasn't explicitly said they are on the CML 2+, then
            # attempt to guess the server version.

            # We don't care about cert validation here.  If this is a CML server,
            # we'll fail validation later anyway.
            #
            # Because of that, pass obviously bogus credentials.  The login will fail
            # in a predictable way if this is a CML server.
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            r = requests.get("https://{}/".format(server.host), verify=False)
            warnings.simplefilter("default", InsecureRequestWarning)
            r.raise_for_status()
            # While one could have a user called virutils-test, the user must have a password.
            # So if we send an empty password, that will fail with a known error.
            server.user = "virlutils-test"
            server.passwd = ""
            get_cml_client(server, ignore=True)
    except virl2_client.InitializationError:
        # The client library will raise this error if it encounters an authorization failure.
        pass
    except Exception:
        # Any other error likely means a VIRL/CML 1.x host.
        res = "1"

    return res


def __init_plugins():
    """
    Scan a set of plugin directories and load them if any are found.
    Plugins come in one of three types: command, generator, viewer.
    In general, plugins can override base functionality.
    """

    server = VIRLServer()
    plugin_dirs = server.config.get("CML_PLUGIN_PATH", "")
    if plugin_dirs != "":
        plugin_dirs += ":"

    plugin_dirs += get_default_plugin_dir()
    load_plugins(plugin_dirs)

    for cmd in Plugin.get_plugins("command"):
        try:
            pl = CommandPlugin(command=cmd)
        except NoPluginError:
            continue
        if not check_valid_plugin(pl, pl.run, "run"):
            click.secho(
                "ERROR: Malformed plugin for command {}.  The `run` method must be static and a click.command".format(cmd), fg="red"
            )
            Plugin.remove_plugin("command", cmd)
        else:
            virl.add_command(pl.run, name=cmd)

    # initialize the 'generate' command arguments after we've loaded
    # any plugins.  Else the plugins will not be available
    init_generators()


__server_ver = __get_server_ver()

if __server_ver == "1":
    virl.add_command(uwm1, name="uwm")
    virl.add_command(flavors1, name="flavors")
    virl.add_command(logs1, name="logs")
    virl.add_command(swagger1, name="swagger")
    virl.add_command(viz1, name="viz")
    virl.add_command(sid, name="id")
else:
    virl.add_command(cockpit)
    virl.add_command(definitions)
    virl.add_command(wipe)
    virl.add_command(extract)
    virl.add_command(clear)
    virl.add_command(ui)
    virl.add_command(license)
    virl.add_command(rm)
    virl.add_command(lid, name="id")
    virl.add_command(command)

virl.add_command(search)

__sub_commands = [
    "console",
    "nodes",
    "up",
    "down",
    "ls",
    "use",
    "save",
    "telnet",
    "ssh",
    "generate",
    "start",
    "stop",
    "pull",
    "version",
]

for cmd in __sub_commands:
    virl.add_command(globals()[cmd + __server_ver], name=cmd)

# Load plugins, but only for CML 2+
if __server_ver != "1":
    __init_plugins()

if __name__ == "__main__":
    virl()  # pragma: no cover
