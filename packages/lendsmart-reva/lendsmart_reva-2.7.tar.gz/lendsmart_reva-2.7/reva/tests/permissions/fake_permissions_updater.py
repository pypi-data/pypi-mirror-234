"""
    update the roles and permissions
"""
# pylint: disable=W0221
from ramda import path_or
from reva.lib.base.resource_update import ResourceUpdater
from reva.lib.base.errors.errors import PermissionsUpdateError
from reva.lib.fixtures.permissions import UPDATE_TEST_CASES

class FakePermissionsUpdate(ResourceUpdater):
    """
    update the roles and permissions
    """

    def __init__(self, arguments, test_case: str):
        super().__init__(arguments)
        self.arguments = arguments
        self.test_case = test_case

    def raise_exception(self, cause):
        raise PermissionsUpdateError(
            message=f"There are conflicts in the current permissions. CAUSE: {cause}")

    def upsert(self, permissions_to_update : list, query):
        """
            Takes the roles data from json and create a query
            and execute it
        """
        return self.excecute_for_single_query_data(query(permissions_to_update))

    def start(self):
        """
        update the permissions
        """
        # Get roles from the database
        remote_permissions = path_or([], [self.test_case, "remote"], UPDATE_TEST_CASES)
        print("Permissions on Remote:=======", remote_permissions)

        local_permissions = path_or([], [self.test_case, "local"], UPDATE_TEST_CASES)
        print("Permissions on Local:=====", local_permissions)

        if len(local_permissions) >= len(remote_permissions):
            # Case 1: Check fields and update
            permissions_to_update = self.compare_and_update(local_permissions, remote_permissions)
            print("Roles To update:=====", permissions_to_update)
            return permissions_to_update

        return self.raise_exception(
            cause="Number of permissions in database is greater than the permissions in json"
        )
