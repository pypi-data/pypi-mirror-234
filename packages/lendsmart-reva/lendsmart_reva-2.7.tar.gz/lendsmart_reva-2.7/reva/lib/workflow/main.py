"""
    handles the workflow
"""
from reva.lib.workflow.update import WorkflowUpdate
from reva.lib.utils.list_files import list_json_files


class Workflow:
    """
        handles the workflow
    """
    def __init__(self, arguments):
        self.argument = arguments

    def run(self):
        """
            THis function will separate the actions
        """
        if self.argument.action == "update":
            WorkflowUpdate(self.argument).start()
        if self.argument.action == "list":
            list_json_files(WorkflowUpdate(self.argument))

    def __str__(self) -> str:
        pass
