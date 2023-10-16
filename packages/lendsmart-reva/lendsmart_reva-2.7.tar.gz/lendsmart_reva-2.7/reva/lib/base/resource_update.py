"""
    Script for updating resources
"""
# pylint: disable=W0221, C0301
from abc import ABC, abstractmethod

from ramda import empty, equals, path_or

from reva.lib.base.base import RevaUpdate
from reva.lib.base.constants import CREATED_AT, NOW, UPDATED_AT
from reva.lib.utils.get_namespaces import get_namespace_by_argument_and_path


class ResourceUpdater(RevaUpdate, ABC):
    """
        Abstract Base Class for updating resources
    """
    def __init__(self, arguments) -> None:
        super().__init__(arguments)
        self.arguments = arguments

    def get_json_paths_to_update(self, prefix):
        """
        This function will return the path to json
        """
        namespaces_to_update = get_namespace_by_argument_and_path(
            self.arguments, self.get_ui_customization_path()
        )
        return self.get_file_paths_ui(namespaces_to_update, prefix)

    def get_resource_from_database(self, query):
        """
            Returns a latest state of resource from database
        """
        # Will use graphQL query to get the latest state of resource from DB
        return self.excecute_for_single_query_data(query_data=query)

    def set_updated_at(self, resource):
        """
            Set updated at time as now
        """
        resource[UPDATED_AT] = NOW

    def set_created_at(self, resource):
        """
            Set created at time as now
        """
        resource[CREATED_AT] = NOW

    def get_resource_by_id(self, resource_id: str, remote_resources: list) -> list:
        """
            Gets the resource by ID
        """
        return list(filter(lambda x: x["id"] == resource_id, remote_resources))

    def compare_and_update(self, local_resources: list, remote_resources) -> list:
        """
            Compare each field 
        """
        for resource in local_resources:
            # If the "id" field is missing or is empty string ("")
            if not path_or("", ["id"], resource):
                self.raise_exception(
                    cause="resource is missing 'id' field or it is set as empty string ('')."
                )

            # Get resource from remote with ID
            remote_resource = self.get_resource_by_id(
                path_or("", ["id"], resource),
                remote_resources
            )

            # Added new resource, not present at remote
            if empty(remote_resource):
                self.set_created_at(resource)
                self.set_updated_at(resource)
                continue

            # No changes in the resources at local
            # resource at local == resource at remote
            if equals(resource, remote_resource[0]):
                continue

            # updated_at fields of resources are different
            # CONFLICT case
            if not equals(path_or("", [UPDATED_AT], resource),
                          path_or("", [UPDATED_AT], remote_resource[0])):
                print("There is mismatch in updated_at field of the corresponding resource at remote")

                print("updated_at in Local Resource: ",
                      path_or("", [UPDATED_AT], resource))

                print("updated_at in Remote Resource: ",
                      path_or("", [UPDATED_AT], remote_resource[0]))
                self.raise_exception(cause=f"resource ID: {path_or('', ['id'], resource)}")


            # Changes in local resource
            # No conflict case
            self.set_updated_at(resource)

        return local_resources

    @abstractmethod
    def upsert(self):
        """
            Upsert the resource
        """

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
        # Steps:
        # 1. Get json
        # 2. Get latest resource from database
        # 3. Compare their size, if size of JSON < Database; Raise Error

        # 4. If size of JSON >= Database:
        ## 1. If size greater than > Resource in database: Update + Insert needed;
            #   i. On update check for conflict if no conflict and there are changes in the fields
            #      set updated at time ELSE Raise ERROR
            #   ii. set updated at time and created at time
            #   iii. Do upsert

        ## 2. If size == Resource in database: Update needed;
            # i.  On update check for conflict if no conflict and there are changes in the fields
            #      set updated at time ELSE Raise ERROR
            # ii. Do upsert
