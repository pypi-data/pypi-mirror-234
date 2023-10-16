"""
    handles the roles and permissions
"""
from reva.lib.roles.update import RolesUpdate
from reva.lib.roles.delete import RolesDeleter
from reva.lib.utils.list_files import list_json_files

class Roles:
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
            RolesUpdate(self.argument).start()
        if self.argument.action == "delete":
            RolesDeleter(self.argument).start()
        if self.argument.action == "list":
            list_json_files(RolesUpdate(self.argument))


    def __str__(self) -> str:
        pass
