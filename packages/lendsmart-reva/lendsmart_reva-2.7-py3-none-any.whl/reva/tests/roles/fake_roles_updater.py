"""
    update the roles and permissions
"""
# pylint: disable=W0221
from ramda import path_or
from reva.lib.base.resource_update import ResourceUpdater
from reva.lib.base.errors.errors import RolesUpdateError
from reva.lib.fixtures.roles import UPDATE_TEST_CASES

class FakeRolesUpdate(ResourceUpdater):
    """
    update the roles and permissions
    """

    def __init__(self, arguments, test_case: str):
        super().__init__(arguments)
        self.arguments = arguments
        self.test_case = test_case

    def raise_exception(self, cause):
        raise RolesUpdateError(
            message=f"There are conflicts in the current roles. CAUSE: {cause}")

    def upsert(self, roles_to_update : list, query):
        """
            Takes the roles data from json and create a query
            and execute it
        """
        return self.excecute_for_single_query_data(query(roles_to_update))

    def start(self):
        """
        update the roles
        """
        # Get roles from the database
        remote_roles = path_or([], [self.test_case, "remote"], UPDATE_TEST_CASES)
        print("Roles on Remote:=======", remote_roles)

        local_roles = path_or([], [self.test_case, "local"], UPDATE_TEST_CASES)
        print("Roles on Local:=====", local_roles)

        if len(local_roles) >= len(remote_roles):
            # Case 1: Check fields and update
            roles_to_update = self.compare_and_update(local_roles, remote_roles)
            print("Roles To update:=====", roles_to_update)
            return roles_to_update

        return self.raise_exception(
            cause="Number of roles in database is greater than the roles in json.")
