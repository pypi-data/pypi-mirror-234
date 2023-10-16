"""
    handles the document access control
"""
from reva.lib.document_access_control.update import DocumentAccessControlUpdate
from reva.lib.utils.list_files import list_json_files


class DocumentAccessControl:
    """
    handles the document access control
    """

    def __init__(self, arguments):
        self.argument = arguments

    def run(self):
        """
        THis function will separate the actions
        """
        if self.argument.action == "update":
            DocumentAccessControlUpdate(self.argument).start()
        if self.argument.action == "list":
            list_json_files(
                DocumentAccessControlUpdate(self.argument)
            )

    def __str__(self) -> str:
        pass
