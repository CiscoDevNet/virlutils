from pkgutil import iter_modules
from importlib import import_module
from abc import ABC, abstractmethod
import sys
import os
import click

_plugins_enabled = True


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

    _plugin_types = [
        "CommandPlugin",
        "GeneratorPlugin",
        "ViewerPlugin",
    ]

    def __new__(cls, **kwargs):
        # only provide a plugin if global plugin support is enabled.
        if not _plugins_enabled:
            raise NoPluginError("plugin support is disabled")

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
        good_plugin = False
        for t, d in cls._plugin_map.items():
            nptype = kwargs.pop(t, None)
            if nptype and ptype:
                raise ValueError("plugin may only contain one type: {}".format(", ".join(cls._plugin_map.keys())))

            if nptype:
                ptype = nptype
                pdict = d

            if ptype:
                good_plugin = True

                if ptype not in pdict:
                    pdict[ptype] = cls

        if cls.__name__ not in cls._plugin_types and not good_plugin:
            raise ValueError("invalid plugin {}".format(cls.__name__))

    @classmethod
    def get_plugins(cls, t):
        return list(cls._plugin_map[t].keys())

    @classmethod
    def remove_plugin(cls, t, name):
        cls._plugin_map[t].pop(name, None)


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
        self._viewer = kwargs.pop("viewer")

    @property
    def viewer(self):
        return self._viewer

    @abstractmethod
    def visualize(self, **kwargs):
        raise NotImplementedError


def load_plugins(basedirs):
    if isinstance(basedirs, str):
        basedirs = basedirs.split(os.pathsep)

    modules = iter_modules(path=basedirs)
    for d in basedirs:
        if os.path.isdir:
            sys.path.append(d)

    for mod in modules:
        try:
            import_module(name=mod.name)
        except (AttributeError, ImportError, ValueError, TypeError) as e:
            # This is not a valid plugin
            click.secho(str(e), fg="red")


def check_valid_plugin(pl, mtd, mtd_name, is_click=True):
    if is_click:
        if not hasattr(mtd, "hidden") or not isinstance(pl.__class__.__dict__[mtd_name], staticmethod):
            return False

    return True


def _test_enable_plugins(enabled=True):
    """
    This function allows the unit tests to toggle
    plugin support on and off.  Without it, once
    pugins are loaded, they remain loaded for the whole
    test suite.  This can break subsequent tests.
    """
    global _plugins_enabled
    _plugins_enabled = enabled
