
"""
    This module builds the lendsmart client
"""
# pylint: disable=R0903
from base64 import b64decode
from ramda import path_or, is_empty
from lendsmart_api import LendsmartClient
from lendsmart_api.jwt.access_token.service_account import ServiceAccount

class LendSmartClientWithSecurity:
    """Class which gives the lendsmart core_api client"""

    def __init__(self, api_endpoint, service_key, namespace=""):
        """Intializer for LendsmartClientWithSecurity class

        Args:
            api_endpoint (string): contians the API endpoint
            service_key (string): contains the decoded service-key
            from the env var for connect specific endpoint
        """
        self.api_endpoint = api_endpoint
        self.service_key = service_key
        self.namespace = namespace

    def set_namespace(self, namespace):
        """
            Sets the namespace
        """
        self.namespace = namespace

    def get_client(self):
        """Function which give the client instance

        Returns:
            dict: instance of lensmart core_api client
        """
        client = LendsmartClient(ServiceAccount(self.service_key), self.api_endpoint)
        if not is_empty(self.namespace):
            client.set_namespace(self.namespace)
        return client

class LendsmartClientBuilder:
    """
        Class to create Lendsmart Client object
    """
    def __init__(self, env_variables: dict, arguments) -> None:
        """Initializer for Lendsmart Client object

        Args:
            env_variables dict: Reva configuration
        """
        self.ls_access_token = path_or(
            "", ["lendsmart_access_token"], env_variables)
        self.namespace = arguments.namespace
        self.api_root = path_or(
            "", ["api_root"], env_variables)

    def decode_service_access_key(self, access_token):
        """
        This function will return the
        decoded access key
        """
        return b64decode(access_token).decode()
    def get_client(self):
        """
            Returns the lendsmart core api
        """
        return LendSmartClientWithSecurity(
            api_endpoint=self.api_root,
            service_key=self.decode_service_access_key(self.ls_access_token),
            namespace=self.namespace
        ).get_client()
