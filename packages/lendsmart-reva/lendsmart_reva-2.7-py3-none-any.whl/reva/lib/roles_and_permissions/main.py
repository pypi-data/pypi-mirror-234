"""
    handles the roles and permissions
"""
from reva.lib.roles_and_permissions.update import RolesAndPermissionUpdate
from reva.lib.utils.list_files import list_json_files

class RolesAndPermission:
    """
        handles the roles and permissions
    """
    def __init__(self, arguments):
        self.argument = arguments

    def run(self):
        """
            THis function will separate the actions
        """
        if self.argument.action == "update":
            RolesAndPermissionUpdate(self.argument).start()
        if self.argument.action == "list":
            list_json_files(RolesAndPermissionUpdate(self.argument))


    def __str__(self) -> str:
        pass
