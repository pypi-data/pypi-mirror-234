"""
    handles the loan productus
"""
from reva.lib.loan_productus.update import LoanProductsUpdate
from reva.lib.utils.list_files import list_json_files

class LoanProducts:
    """
        handles the loan productus
    """
    def __init__(self, arguments):
        self.argument = arguments

    def run(self):
        """
            THis function will separate the actions
        """
        if self.argument.action == "update":
            LoanProductsUpdate(self.argument).start()
        if self.argument.action == "list":
            list_json_files(LoanProductsUpdate(self.argument))


    def __str__(self) -> str:
        pass
