"""
    handles the branch
"""
from reva.lib.branch.create import BranchCreate

class Branch:
    """
        handles the branch
    """
    def __init__(self, arguments):
        self.argument = arguments

    def run(self):
        """
            THis function will separate the actions
        """
        if self.argument.action == "create":
            BranchCreate(self.argument).start()


    def __str__(self) -> str:
        pass