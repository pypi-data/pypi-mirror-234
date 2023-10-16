"""
    update the permissions and permissions
"""
# pylint: disable=W0221
from ramda import path_or
from reva.lib.base.resource_update import ResourceUpdater
from reva.lib.graphql_queries.roles_and_permissions import (
    upsert_permissions_query, get_permissions_by_namespace
)
from reva.lib.base.errors.errors import PermissionsUpdateError


class PermissionsUpdate(ResourceUpdater):
    """
    update the permissions
    """

    def __init__(self, arguments):
        super().__init__(arguments)
        self.arguments = arguments

    def raise_exception(self, cause: str = ""):
        raise PermissionsUpdateError(
            message=f"There are conflicts in the current permissions json. CAUSE: {cause}")

    def upsert(self, permissions_to_update : list, query):
        """
            Takes the permissions data from json and create a query
            and execute it
        """
        return self.excecute_for_single_query_data(query(permissions_to_update))

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

    def start(self):
        """
        update the permissions
        """
        # Get permissions json data
        data_list = self.get_json_files_by_path(
            self.get_json_paths_to_update(prefix=["PRM_"])
        )

        permissions_json_data = path_or({}, [0, "json_data"], data_list)

        # Get permissions from the database
        remote_permissions = self.get_permissions_from_db()
        # print("permissions on Remote:=======", remote_permissions)
        local_permissions = path_or([], ["data"], permissions_json_data)

        if len(local_permissions) >= len(remote_permissions):
            # Case 1: Check fields and update
            permissions_to_update = self.compare_and_update(local_permissions, remote_permissions)
            # print("Permissions To update:=====", permissions_to_update)
            self.upsert(permissions_to_update, upsert_permissions_query)
            print("-----permissions update done!-----")

        else:
            self.raise_exception(
                cause="Number of permissions in database is greater than the permissions in json")
