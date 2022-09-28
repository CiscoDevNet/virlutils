# cmlutils Plugins

## Introduction

Have you ever wanted your own, customer cmlutils command?  Now's your chance.  The plugin capabilities
in cmlutils allow you to create your own customer commands, override existing command (e.g., provide your
own version of `cml up`), add an inventory generator, or provide a custom viewer for the various output
functions (e.g., change the output of `cml ls`).

## Requirements

- Plugin support is only provided when using CML 2+.  Support for VIRL/CML 1.x is not available.
- All plugins must be written in Python (or at least a stub that can bootstrap modules written in other languages)

## Using Plugins

To use plugins, either place all the plugin `.py` files into the `.virl/plugins` directory in the
current working directory or place them all in any other directory and set the `CML_PLUGIN_PATH`
to point to that directory.  `CML_PLUGIN_PATH` can either be set in the environment or placed in
`.virlrc`.

The syntax for `CML_PLUGIN_PATH` is a delimited list of directories.  The delimiter is ':' for UNIX-like
systems and ';' for Windows.  For example, on Linux or macOS:

```sh
CML_PLUGIN_PATH=~/cml/plugins:/opt/cml/plugins
```

And on Windows:

```cmd
CML_PLUGIN_PATH=%HOME%/cml/plugins;C:/cml/plugins
```

You'll find some examples for each plugin type in this directory.

## Developing Plugins

Plugins come in one of three types: **CommandPlugin**, **GeneratorPlugin**, and **ViewerPlugin**.  Each one uses slightly different syntax.

### Command Plugins

A command plugin is of type CommandPlugin and represents a custom or overridden command at the top level of `cmlutils`.  That is, when
you run `cml --help` you will see your command plugins listed in the output.

cmlutils makes use of the Python [click](https://click.palletsprojects.com/en/7.x/) package for exposing commands and parsing command
arguments.  Therefore, your command plugins must import and use this package.  A very simple command plugin will start with the following:

```python
from virl.api import CommandPlugin
import click

class MyCommandPlugin(CommandPlugin, command="my-cmd"):
    @staticmethod
    @click.command()
    def run():
        """
        my custom command
        """
        pass
```

The import bits here are that your command plugin must extend the `CommandPlugin` base class.  It also must specify a keyword argument,
`command` that is the command name that will appear in the `cml --help` output (and will be the way to run your plugin).

The class must contain the `run()`method at the very least.  This method must be static and must also be a `click.command()`.  You are
free to specify as many other click arguments or options that you want or need for your command.

Click uses the initial comment in the `run()` method as the help or description string for the command.  Therefore, it is desirable to
include something there.  Else your command name will appear with an empty description next to it.

See [Common Functions](#common-functions) for more capabilities you can use within cmlutils or within CML itself.

### Generator Plugins

A generator plugin is of type GeneratorPlugin and represents a sub-command of the `generate` top-level command.  It allows you to create
an inventory export from a CML lab for use in another tool or framework.  Built-in generators are provided for
[Ansible](https://www.ansible.com/), [Cisco Network Services Orchestrator](https://developer.cisco.com/docs/nso/), and
[pyATS](https://developer.cisco.com/pyats/).  While a generator typically provides an output file formatted to the specifications of the
tool or framework, it is perfectly permissible to push that inventory directly to the external tool (as is done in the case of Cisco NSO).
The functionality is up to you.

As with command plugins, generator plugins are [click](ttps://click.palletsprojects.com/en/7.x/) commands, which gives you the freedom to
provide whatever command line arguments you require to achieve your generator's goals.  A very simple generator plugin will start with
the following:

```python
from virl.api import GeneratorPlugin
import click

class MyGenPlugin(GeneratorPlugin, generator="my-app"):
    @staticmethod
    @click.command()
    def generate():
        """
        generate inventory for my-app
        """
        pass
```

A generator plugin must extend the `GeneratorPlugin` base class and specify a keyword argument, `generator` that is the sub-command
that will appear in the `cml generate --help` output (and will be used to execute your custom generator from the command line).

The class must contain the `generator()` method at the very least.  This method must be static and must also be a `click.command()`.  You are
free to specify as many other click arguments or options that you want or need to support your generation functionality.

Click uses the initial comment in the `generate()` method as the help or description string for the sub-command.  Therefore, it is desirable to
include something here.  Else your generate sub-command will appear with an empty description next to it.

See [Common Functions](#common-functions) for more capabilities you can use within cmlutils or within CML itself.

### Viewer Plugins

A viewer plugin is of type ViewerPlugin and provides an content formatter for the various commands within cmlutils that display output.
Viewer plugins are passed the data to be displayed, and it's up to your plugin how you want to represent that data.  By default, all of
the commands that display output use the Python [tabulate](https://pypi.org/project/tabulate/) module.  While this output is good for
humans to read, it's not so friendly for machines.  So perhaps a viewer plugin might instead produce more script-friendly output...
(in fact, that's what the same `labs_tsv.py` plugin does).

Each command that produces output has its own set of arguments that are passed to viewer plugins.  However, the basic structure for
any viewer plugin is as follows:

```python
from virl.api import ViewerPlugin

class MyViewPlugin(ViewerPlugin, viewer="lab"):
    def visualize(self, **kwargs):
        pass
```

Each viewer plugin must extend the `ViewerPlugin` base class and provide a `viewer` keyword argument indicating which output it will
support.  The list of viewers are:

- **lab** : Render the output of `cml ls`
- **node** : Render the output of `cml nodes`
- **console** : Render the output of `cml console`
- **license** : Render the output of `cml license show`
- **license_feature** : Render the output of `cml license features show`
- **image_def** : Render the output of `cml definitions image ls`
- **node_def** : Render the output of `cml definitions node ls`
- **search** : Render the output of `cml search`

Each one of these viewers is discussed in more details below.

#### _lab_ Viewer

The _lab_ viewer renders the output of `cml ls` (i.e., the list of labs on the server and optionally in the local cache).  Your
viewer will be passed two keys in the `kwargs` dictionary: `labs` and `cached_labs`.

The value of `labs` is a list containing elements of type `virl2_client.models.lab.Lab` ([documentation](https://developer.cisco.com/docs/virl2-client/)).
The value of `cached_labs` is a list containing elements of type `virl.api.cml.CachedLabs`.  Instances of this class offer only basic properties from
a "live" lab on the server.  That is, you can call `.id`, `.title`, `.description`, `.state()`, `.statistics`, and `.owner` on
a CachedLab instance.

#### _node_ Viewer

The _node_ viewer renders the output of `cml nodes` (i.e., the list of nodes for a given lab).  Your viewer will be passed
`nodes` and `computes` keys in the `kwargs` dictionary.

The value of `nodes` is a list containing elements of type `virl2_client.models.node.Node` ([documentation](https://developer.cisco.com/docs/virl2-client/)).

The value of `computes` is a dict representing available compute nodes.  See below under the cluster info plugin for the structure of this dict.

#### _console_ Viewer

The _console_ viewer renders the output of `cml console` (i.e., a list of each node and its console URL).  Your viewer will be passed a
`consoles` key in the `kwargs` dictionary.

The value of `consoles` is a list of dictionaries.  Each dictionary will contain two keys: `node` and `console` where `node` is the name
of the node (a string) and `console` is the console URL (a string).

#### _license_ Viewer

The _license_ viewer renders the output of `cml license show` (i.e., the license details of the CML server).  Your viewer will be passed
a `license` key in the `kwargs` dictionary.

The value of `license` is an object representing the license details of the CML server.  This structure is document at
<https://CML_SERVER/api/v0/ui/#/Licensing/simple_ui.http_handlers.licensing_status_get> where CML_SERVER is your CML server's
IP or hostname.

#### _license_feature_ Viewer

The _license_feature_ viewer renders the output of `cml license features show` (i.e., the selected license features of the CML server).  Your viewer will be passed
a `features` key in the `kwargs` dictionary.

The value of `features` is an object representing the licensed feature details of the CML server.  This structure is document at
<https://CML_SERVER//api/v0/ui/#/Licensing/simple_ui.http_handlers.licensing_features_get> where CML_SERVER is your CML server's
IP or hostname.

#### _image_def_ Viewer

The _image_def_ viewer renders the output of `cml definitions image ls` (i.e., the list of available image definitions on the CML server).  Your viewer will be
passed an `image_defs` key in the `kwargs` dictionary.

The value of `image_defs` is an object representing the list of image definitions on the CML server.  This structure is documented
at <https://CML_SERVER/api/v0/ui/#/Image%20Definitions/simple_ui.http_handlers.image_definitions_list> where CML_SERVER is your CML server's
IP or hostname.

#### _node_def_ Viewer

The _node_def_ viewer renders the output of `cml definitions node ls` (i.e., the list of available node definitions on the CML server).  Your viewer will be
passed an `node_defs` key in the `kwargs` dictionary.

The value of `node_defs` is an object representing the list of node definitions on the CML server.  This structure is documented
at <https://CML_SERVER/api/v0/ui/#/Node%20Definitions/simple_ui.http_handlers.node_definition_get_list> where CML_SERVER is your CML server's
IP or hostname.

#### _search_ Viewer

The _search_ viewer renders the output of `cml search` (i.e., a list of repositories that have CML labs).  Your viewer will be passed
a `repos` key in the `kwargs` dictionary.

The value of `repos` is a list of elements of type string that match the given query.

#### _cluster_ Viewer

The _cluster_ viewer renders the output of `cml cluster info` (i.e., a list of cluster compute nodes).  Your viewer will be passed a dict, `computes` in the `kwargs` dictionary.

The value of `computes` is a dictionary of compute nodes, keyed on the node ID.  For example:

```json
"17e91b4e-865a-4627-a6bb-50e3dfa988ab": {
      "kvm_vmx_enabled": true,
      "enough_cpus": true,
      "refplat_images_available": true,
      "lld_connected": true,
      "valid": true,
      "is_controller": true,
      "hostname": "cml-controller"
    }
```

### Common Functions

In general, your plugins have access to all of the power in the `virl2_client` Python library.  However, in practice,
you don't need to import this library or any of its sub-modules.  Within cmlutils, there is a set of common functions
defined in `virl.helpers` ([code](https://github.com/CiscoDevNet/virlutils/blob/master/virl/helpers.py))
that are useful to interact with the CML server.  Search for "CML helper functions" as this begins the set of
functions specific to CML 2+.

For any command or generator plugin, your first couple of lines in the `run()` or `generate()` method will likely be:

```python
server = VIRLServer()
client = get_cml_client(server)
```

The `VIRLServer` class is defined in `virl.api` and the `get_cml_client()` function is defined in `virl.helpers`.  It
is the client that provides access to all of the `virl2_client` functionality.

And, of course, look at the example plugins in this directory as well as the code for the base commands themselves to
see how to make the most of your cmlutils development.
