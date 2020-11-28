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

    def __new__(cls, **kwargs):
        ptype = None
        pdict = None
        pclass = None
        for t, d in {"command": cls._command_plugins, "generator": cls._generator_plugins, "viewer": cls._viewer_plugins}.items():
            nptype = kwargs.pop(t, None)
            if nptype and ptype:
                raise ValueError("plugin may only contain one type: command, generator, or viewer")

            if nptype:
                ptype = nptype
                pdict = d
                pclass = t

        if ptype:
            if ptype not in pdict:
                raise NoPluginError("no {} plugin for {}".format(pclass, ptype))

            return object.__new__(pdict[ptype])
        else:
            raise ValueError("unsupported plugin")

    def __init_subclass__(cls, **kwargs):
        if "command" in kwargs:
            command = kwargs.pop("command")
            if command not in cls._command_plugins:
                cls._command_plugins[command] = cls
        elif "generator" in kwargs:
            generator = kwargs.pop("generator")
            if generator not in cls._generator_plugins:
                cls._generator_plugins[generator] = cls
        elif "viewer" in kwargs:
            viewer = kwargs.pop("viewer")
            if viewer not in cls._viewer_plugins:
                cls._viewer_plugins[viewer] = cls


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
                plugin = Plugin(command=module.command)
                if not hasattr(plugin.run, "hidden") or not isinstance(plugin.__class__.__dict__["run"], staticmethod):
                    raise AttributeError(
                        "ERROR: Malformed plugin for command {}.  The `run` method must be static and a click.command".format(
                            plugin.command
                        )
                    )
            elif hasattr(module, "generator"):
                plugin = Plugin(generator=module.generator)
                if not hasattr(plugin.generate, "hidden") or not isinstance(plugin.__class__.__dict__["generate"], staticmethod):
                    raise AttributeError(
                        "ERROR: Malformed plugin for generator {}.  The `generate` method must be static and a click.command".format(
                            plugin.generator
                        )
                    )
            elif hasattr(module, "viewer"):
                plugin = Plugin(viewer=module.viewer)
            else:
                raise TypeError("unknown plugin type")

            yield plugin
        except (AttributeError, ImportError, ValueError, TypeError) as e:
            # This is not a valid plugin
            click.secho(str(e), fg="red")
