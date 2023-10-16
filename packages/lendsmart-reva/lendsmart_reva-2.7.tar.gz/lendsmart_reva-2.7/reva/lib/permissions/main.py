"""
    handles the Permissions and permissions
"""
from reva.lib.permissions.update import PermissionsUpdate
from reva.lib.permissions.delete import PermissionsDeleter
from reva.lib.utils.list_files import list_json_files

class Permissions:
    """
        handles the permissions
    """
    def __init__(self, arguments):
        self.argument = arguments

    def run(self):
        """
            THis function will separate the actions
        """
        if self.argument.action == "update":
            PermissionsUpdate(self.argument).start()
        if self.argument.action == "delete":
            PermissionsDeleter(self.argument).start()
        if self.argument.action == "list":
            list_json_files(PermissionsUpdate(self.argument))


    def __str__(self) -> str:
        pass
