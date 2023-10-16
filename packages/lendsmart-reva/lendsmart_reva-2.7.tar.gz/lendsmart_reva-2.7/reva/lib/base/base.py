"""
    Base class for reva
"""
from ramda import path_or
from abc import ABC, abstractmethod
from reva.conf.reva import load_conf
from reva.lib.graphql_queries.namespace import get_namespace
from reva.lib.client.builder import ClientBuilder
from reva.lib.utils.get_json_files import JsonFileGetter, FileGetterStore
from reva.lib.utils.get_paths import PathGetter
from reva.lib.base.run_query import RunQuery
from reva.exception import ConfigNotFoundError


class RevaBase(PathGetter, JsonFileGetter, RunQuery, FileGetterStore):
    """
    Reva base class
    """

    def __init__(self, argument):
        self.argument = argument
        self.conf = load_conf(argument)
        if not self.conf:
            raise ConfigNotFoundError("No config found for " + argument.env)
        self.client_builder = ClientBuilder(self.conf)
        self.graphql_client = self.client_builder.graphql_client()

    def get_namespace(self):
        """
            This function retursn the namespace data
        """
        query = get_namespace(namespace=self.argument.namespace)
        return path_or({},["data","namespaces",0], self.excecute_for_single_query_data(query_data=query))


class RevaUpdate(ABC, RevaBase):
    """
    Abstraction for update
    """

    @abstractmethod
    def get_json_paths_to_update(self):
        """
        paths to update, this helps to list the files
        """

    @abstractmethod
    def start(self):
        """
        This function start the process
        """


class RevaCreate(ABC, RevaBase):
    """
    Abstract class for update or create
    """

    @abstractmethod
    def get_paths_to_create(self):
        """
        paths to update or create, this helps to list the files
        """

    @abstractmethod
    def start(self):
        """
        This function start the process
        """
