"""
    handles the advisorprofiles
"""
from reva.lib.advisor_profile.create import AdvisorProfileCreate


class AdvisorProfile:
    """
    handles the AdvisorProfile
    """

    def __init__(self, arguments):
        self.argument = arguments

    def run(self):
        """
        THis function will separate the actions
        """
        if self.argument.action == "create":
            AdvisorProfileCreate(self.argument).start()

    def __str__(self) -> str:
        pass
