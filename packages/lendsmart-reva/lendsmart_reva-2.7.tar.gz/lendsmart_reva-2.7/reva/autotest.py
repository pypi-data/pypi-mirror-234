"""
    handles the workflow
"""
from reva.lib.auto.main import AutoTest

def main(argument):
    """
        calls the action
    """
    return AutoTest(arguments=argument).start()


def autotest(parser):
    """
        handles the workflow
    """
    parser.add_argument('--namespace', metavar ='N', type = str,  required=True,
                        help ='Namespace to test')
    parser.add_argument('--action', metavar ='A', type = str, default="run",
                        help ='Namespace to test')
    parser.add_argument('--workflow', metavar='WFIF', type =  str,
                        help = "Add the file name of workflow intent (WFI_cards etc...)")
    parser.add_argument('--product', metavar='PD', type =  str,  required=True,
                        help = "product name to test (Purchase , Secured etc..)")
    parser.add_argument('--group', metavar='LR', type =  str,  default = "borrower",
                        help = "loan role name to test (borrower or coborrower)")
    parser.add_argument('--project_url', metavar='EURL', type =  str,  required=True,
                        help = "the url to start the test \
                            (the first page after the product selected..)")
    parser.add_argument('--fixures', metavar='TD', type =  str,  required=True, nargs='+',
                        help = "test test data names")
    parser.add_argument('--limit_random', metavar='SR', type =  str, default = 5,
                        help = "How many samples to pick from combinations")
    parser.add_argument('--spec', metavar='SC', type =  str, default=None,
                        help = "Select particular combination to run")
    parser.add_argument('--platform', metavar='PF', type =  str, default="remote",
                        help = "where to run the lambda")

    parser.set_defaults(func=main,)
