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
from reva.lib.fixtures.permissions import DELETE_TEST_CASES

class FakePermissionsDeleter(ResourceDeleter):
    """
    delete the permissions
    """

    def __init__(self, arguments, case):
        super().__init__(arguments)
        self.arguments = arguments
        self.deploy_json = path_or({}, [case], DELETE_TEST_CASES)
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

    def delete(self, query):
        """
            Delete resources
        """
        # print("JSON DATA: ====", self.deploy_json)
        list_of_ids = path_or([], ["delete_permissions"],self.deploy_json)

        query_datas = []

        for id in list_of_ids:
            if empty(self.get_resource_by_id(id, self.remote_permissions)):
                self.raise_exception(cause=f"No record found with ID: {id}.")

            query_datas.append(
                query(
                    id
                )
            )
        print("-----permissions were deleted successfully!-----")
        return query_datas

    def start(self):
        """
        delete the permissions
        """
        return self.delete(query=delete_permission_by_id)
