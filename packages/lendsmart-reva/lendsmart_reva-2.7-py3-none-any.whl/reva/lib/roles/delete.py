"""
    update the roles and permissions
"""

# pylint: disable=W0102, W0718, W0221, W0622, C0103
from ramda import path_or, empty
from reva.lib.base.resource_delete import ResourceDeleter
from reva.lib.base.errors.errors import RolesDeleteError
from reva.lib.graphql_queries.roles_and_permissions import (
    delete_role_by_id, get_roles_by_namespace,
    delete_permission_by_role_id
)

class RolesDeleter(ResourceDeleter):
    """
    delete the roles
    """

    def __init__(self, arguments):
        super().__init__(arguments)
        self.arguments = arguments
        self.remote_roles = self.get_roles_from_db()
        self.deploy_json = self.get_file_by_path(self.get_deploy_json_path())

    def raise_exception(self, cause: str):
        raise RolesDeleteError(f"Error occured while deleting roles, Error: {cause}")

    def get_roles_from_db(self):
        """
            Gets the roles from database using graphql query
        """
        query_response = self.get_resource_from_database(
            get_roles_by_namespace(self.arguments.namespace))

        return path_or([], ["data", "roles"], query_response)

    def __get_list_of_ids(self):
        """
        Returns the list of ids of roles to be deleted
        """
        roles = path_or({}, ["reva", "roles"], self.deploy_json)
        return path_or([],
                       [0, "delete"],
                       list(filter(lambda x: x["namespace"] == self.arguments.namespace, roles)))

    def delete(self):
        """
            Delete resources
        """
        list_of_ids = self.__get_list_of_ids()
        # print("List of ids==", list_of_ids)
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

        # print("Query Data:===", query_datas)
        self.excecute_for_list_of_query_data(query_datas)
        print("-----roles were deleted successfully!-----")
        return

    def start(self):
        """
        update the roles and permissions
        """
        self.delete()
