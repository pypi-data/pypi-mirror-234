"""
    update the roles and permissions
"""

# pylint: disable=W0102, W0718, W0221, W0622, C0103
from ramda import path_or, empty
from reva.lib.base.resource_delete import ResourceDeleter
from reva.lib.base.errors.errors import RolesDeleteError
from reva.lib.fixtures.roles import DELETE_TEST_CASES
from reva.lib.graphql_queries.roles_and_permissions import (
    delete_role_by_id, get_roles_by_namespace,
    delete_permission_by_role_id
)

class FakeRolesDeleter(ResourceDeleter):
    """
    delete the roles
    """

    def __init__(self, arguments, case):
        super().__init__(arguments)
        self.arguments = arguments
        self.remote_roles = self.get_roles_from_db()
        self.deploy_json = path_or({}, [case], DELETE_TEST_CASES)

    def raise_exception(self, cause: str):
        raise RolesDeleteError(f"Error occured while deleting roles, Error: {cause}")

    def get_roles_from_db(self):
        """
            Gets the roles from database using graphql query
        """
        query_response = self.get_resource_from_database(
            get_roles_by_namespace(self.arguments.namespace))

        return path_or([], ["data", "roles"], query_response)

    def delete(self):
        """
            Delete resources
        """
        # print("JSON DATA: ====", self.deploy_json)
        list_of_ids = path_or([], ["delete_roles"],self.deploy_json)

        query_datas = []

        for id in list_of_ids:
            if empty(self.get_resource_by_id(id, self.remote_roles)):
                self.raise_exception(cause=f"No record found for ID: {id}.")

            # delete all the permissions associated with the role
            query_datas.append(
                delete_permission_by_role_id(id)
            )
            # delete the role itself
            query_datas.append(
                delete_role_by_id(id)
            )

        print("-----roles were deleted successfully!-----")
        return query_datas

    def start(self):
        """
        update the roles and permissions
        """
        return self.delete()
