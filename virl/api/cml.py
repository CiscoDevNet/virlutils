import os

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class CachedLab(object):
    """
    This is a stub class to represent a pseudo-lab that is cached locally.
    Only enough of the lab model is implemented for the required virlutils functions.
    """

    __id = None
    __title = None
    __description = None
    __stats = {
        "nodes": 0,
        "links": 0,
        "interfaces": 0,
    }

    def __init__(self, lab_id, cache_file):
        if not os.path.exists(cache_file):
            raise FileNotFoundError("Cached lab {} not found".format(cache_file))

        self.__id = lab_id

        with open(cache_file, "rb") as fd:
            lab = load(fd, Loader=Loader)

            self.__title = lab["lab"]["title"]
            self.__description = lab["lab"]["description"]
            self.__stats["nodes"] = len(lab["nodes"])
            self.__stats["links"] = len(lab["links"])
            for n in lab["nodes"]:
                self.__stats["interfaces"] += len(n["interfaces"])

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    def state(self):
        return "CACHED"

    @property
    def statistics(self):
        return self.__stats

    @property
    def owner(self):
        return "N/A"

    @property
    def username(self):
        return "N/A"
