from pkgutil import iter_modules
from importlib import import_module
from abc import ABC, abstractmethod
from typing import Iterable
import sys
import os
import click


class NoPluginError(Exception):
    pass


class Plugin(ABC):
    _command_plugins = {}
    _generator_plugins = {}
    _viewer_plugins = {}

    _plugin_map = {
        "command": _command_plugins,
        "generator": _generator_plugins,
        "viewer": _viewer_plugins,
    }

    def __new__(cls, **kwargs):
        for t, d in cls._plugin_map.items():
            if t in kwargs:
                val = kwargs.pop(t)
                if val in d:
                    return object.__new__(d[val])
                else:
                    raise NoPluginError("no {} plugin for {}".format(t, val))

        raise ValueError("unsupported plugin")

    def __init_subclass__(cls, **kwargs):
        ptype = None
        pdict = None
        for t, d in cls._plugin_map.items():
            nptype = kwargs.pop(t, None)
            if nptype and ptype:
                raise ValueError("plugin may only contain one type: {}".format(", ".join(cls._plugin_map.keys())))

            if nptype:
                ptype = nptype
                pdict = d

            if ptype:
                if ptype not in pdict:
                    pdict[ptype] = cls


class CommandPlugin(Plugin, ABC):
    def __init__(self, **kwargs):
        self._command = kwargs.pop("command")

    @property
    def command(self):
        return self._command

    @staticmethod
    @abstractmethod
    @click.command()
    def run():
        """
        This must be a "click" command.
        """
        raise NotImplementedError


class GeneratorPlugin(Plugin, ABC):
    def __init__(self, **kwargs):
        self._generator = kwargs.pop("generator")

    @property
    def generator(self):
        return self._generator

    @staticmethod
    @abstractmethod
    @click.command()
    def generate():
        """
        This must be a "click" command.
        """
        raise NotImplementedError


class ViewerPlugin(Plugin, ABC):
    def __init__(self, **kwargs):
        self._viewer = kwargs.pop("viewer", None)

    @property
    def viewer(self):
        return self._viewer

    @abstractmethod
    def visualize(self, **kwargs):
        raise NotImplementedError


def load_plugins(basedirs) -> Iterable[Plugin]:
    if isinstance(basedirs, str):
        basedirs = basedirs.split(os.pathsep)

    modules = iter_modules(path=basedirs)
    for d in basedirs:
        if os.path.isdir:
            sys.path.append(d)

    for mod in modules:
        try:
            module = import_module(name=mod.name)
            # This is a top-level attribute
            if hasattr(module, "command"):
                plugin = CommandPlugin(command=module.command)
                if not hasattr(plugin.run, "hidden") or not isinstance(plugin.__class__.__dict__["run"], staticmethod):
                    raise AttributeError(
                        "ERROR: Malformed plugin for command {}.  The `run` method must be static and a click.command".format(
                            plugin.command
                        )
                    )
            elif hasattr(module, "generator"):
                plugin = GeneratorPlugin(generator=module.generator)
                if not hasattr(plugin.generate, "hidden") or not isinstance(plugin.__class__.__dict__["generate"], staticmethod):
                    raise AttributeError(
                        "ERROR: Malformed plugin for generator {}.  The `generate` method must be static and a click.command".format(
                            plugin.generator
                        )
                    )
            elif hasattr(module, "viewer"):
                # We don't need to allocate a plugin for this as no additional checks are needed.
                continue
            else:
                raise TypeError("unknown plugin type")

            yield plugin
        except (AttributeError, ImportError, ValueError, TypeError) as e:
            # This is not a valid plugin
            click.secho(str(e), fg="red")
