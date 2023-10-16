"""
    update the roles and permissions
"""
# pylint: disable=W0221
from ramda import path_or
from reva.lib.base.resource_update import ResourceUpdater
from reva.lib.graphql_queries.roles_and_permissions import (
    upsert_roles_query, get_roles_by_namespace
)
from reva.lib.base.errors.errors import RolesUpdateError


class RolesUpdate(ResourceUpdater):
    """
    update the roles and permissions
    """

    def __init__(self, arguments):
        super().__init__(arguments)
        self.arguments = arguments

    def raise_exception(self, cause: str=""):
        raise RolesUpdateError(message=f"There are conflicts in current roles json. CAUSE: {cause}")

    def upsert(self, roles_to_update : list, query):
        """
            Takes the roles data from json and create a query
            and execute it
        """
        return self.excecute_for_single_query_data(query(roles_to_update))

    def get_roles_from_db(self):
        """
            Gets the roles from database using graphql query
        """
        query_response = self.get_resource_from_database(
            get_roles_by_namespace(self.argument.namespace))

        return path_or([], ["data", "roles"], query_response)

    def start(self):
        """
        update the roles
        """
        # Get roles json data
        data_list = self.get_json_files_by_path(
            self.get_json_paths_to_update(prefix=["ROL_"])
        )
        roles_json_data = path_or({}, [0, "json_data"], data_list)

        # Get roles from the database
        remote_roles = self.get_roles_from_db()
        # print("Remote Roles:===", remote_roles)
        local_roles = path_or([], ["data"], roles_json_data)

        if len(local_roles) >= len(remote_roles):
            # Case 1: Check fields and update
            roles_to_update = self.compare_and_update(local_roles, remote_roles)
            # print("Roles To update:=====", roles_to_update)
            self.upsert(roles_to_update, upsert_roles_query)
            print("-----roles update done!-----")

        else:
            self.raise_exception(
                cause="Number of roles in database is greater than the roles in json.")
