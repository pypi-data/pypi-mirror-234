"""
    Script for updating resources
"""
# pylint: disable=W0221, C0301, W0622, C0103
from abc import ABC, abstractmethod

from reva.lib.base.base import RevaBase


class ResourceDeleter(RevaBase, ABC):
    """
        Abstract Base Class for deleting resources
    """
    def __init__(self, arguments) -> None:
        super().__init__(arguments)
        self.arguments = arguments

    def get_deploy_json_path(self):
        """
        This function will return the path to json
        """
        return self.get_ui_deploy_json_path(args=self.argument)

    def get_resource_from_database(self, query):
        """
            Returns a latest state of resource from database
        """
        # Will use graphQL query to get the latest state of resource from DB
        return self.excecute_for_single_query_data(query_data=query)

    def get_resource_by_id(self, resource_id: str, remote_resources: list) -> list:
        """
            Gets the resource by ID
        """
        return list(filter(lambda x: x["id"] == resource_id, remote_resources))

    @abstractmethod
    def raise_exception(self, cause: str):
        """
            Raise an exception in case of conflict
        """

    @abstractmethod
    def start(self):
        """
            Start the process
        """
