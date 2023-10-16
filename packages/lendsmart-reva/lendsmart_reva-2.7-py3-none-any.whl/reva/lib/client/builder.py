"""
    This module will build the client
"""
from ramda import path_or
from reva.lib.client.graphql_client import GraphQlClient
from reva.lib.client.lendsmart_client import LendsmartClientBuilder


class ClientBuilder:
    """
    This class build the client
    """

    def __init__(self, conf: dict):
        self.conf = conf

    def get_api_root(self):
        """
        return api root
        """
        return path_or("", ["api_root"], self.conf)

    def graphql_client(self):
        """
        This function return the grqphql client
        """
        return GraphQlClient(self.conf).get_client()

    def lendsmart_api(self, arguments):
        """
        This function return the lendsmart core api
        """
        return LendsmartClientBuilder(self.conf, arguments).get_client()
