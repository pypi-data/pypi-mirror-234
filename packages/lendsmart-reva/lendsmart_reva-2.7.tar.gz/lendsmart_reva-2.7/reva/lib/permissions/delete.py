"""
    Delete permissions
"""

# pylint: disable=W0102, W0718, W0221, W0622, C0103, R0901
from ramda import path_or, empty
from reva.lib.base.resource_delete import ResourceDeleter
from reva.lib.base.errors.errors import PermissionsDeleteError
from reva.lib.graphql_queries.roles_and_permissions import (
    delete_permission_by_id, get_permissions_by_namespace
)

class PermissionsDeleter(ResourceDeleter):
    """
    delete the permissions
    """

    def __init__(self, arguments):
        super().__init__(arguments)
        self.arguments = arguments
        self.deploy_json = self.get_file_by_path(self.get_deploy_json_path())
        self.remote_permissions = self.get_permissions_from_db()

    def raise_exception(self, cause: str):
        raise PermissionsDeleteError(f"Error occured while deleting permissions, Error: {cause}")

    def get_permissions_from_db(self) -> list:
        """
        Get permissions from database using graphql query
        """
        remote_permissions = []
        query_response = self.get_resource_from_database(
            get_permissions_by_namespace(self.argument.namespace))

        list_of_roles = path_or([], ["data", "roles"], query_response)

        for role in list_of_roles:
            permission = path_or([], ["permissions"], role)
            remote_permissions.extend(permission)

        return remote_permissions

    def __get_list_of_ids(self):
        """
        Returns the list of ids of roles to be deleted
        """
        roles = path_or({}, ["reva", "permissions"], self.deploy_json)
        return path_or([],
                       [0, "delete"],
                       list(filter(lambda x: x["namespace"] == self.arguments.namespace, roles)))

    def delete(self, query):
        """
            Delete rresources
        """
        list_of_ids = self.__get_list_of_ids()
        # print("List of IDs: ", list_of_ids)
        query_datas = []
        for id in list_of_ids:
            if empty(self.get_resource_by_id(id, self.remote_permissions)):
                self.raise_exception(cause=f"No record found for ID: {id}.")

            query_datas.append(
                query(
                    id
                )
            )
        # print("Query Data:===", query_datas)
        self.excecute_for_list_of_query_data(query_datas)
        print("-----permissions were deleted successfully!-----")
        return

    def start(self):
        """
        update the permissions and permissions
        """
        self.delete(query=delete_permission_by_id)
