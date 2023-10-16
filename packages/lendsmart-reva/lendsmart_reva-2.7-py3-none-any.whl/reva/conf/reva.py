"""
    This module will load the config
"""
from ramda import path_or
from reva.lib.utils.get_paths import PathGetter
from reva.lib.utils.get_json_files import JsonFileGetter


def build_path():
    """
    This function build the path for conf file
    """
    return PathGetter().get_config_path()


class RevaConf:
    """
    Loads the reva config
    """

    def load(self, env):
        """
        This function will load the config
        """
        config_json = JsonFileGetter().get_file_by_path(build_path())
        return path_or({},[env], config_json)

    def __str__(self) -> str:
        pass


def load_conf(argument):
    """
    This function returns the reva config
    """
    return RevaConf().load(argument.env)
