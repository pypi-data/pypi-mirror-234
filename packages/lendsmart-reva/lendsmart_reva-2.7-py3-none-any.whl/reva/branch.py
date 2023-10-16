"""
    handles the branch creation and updation
"""
from reva.lib.branch.main import Branch


def main(argument):
    """
    calls the action
    """
    return Branch(arguments=argument).run()


def branch(parser):
    """
        handles branch \
        usage - > reva branch updateorcreate rsntdev qa
    """
    parser.add_argument(
        "action",
        metavar="A",
        type=str,
        help="action for branch,  supported values [create]",
    )
    parser.add_argument(
        "namespace",
        metavar="N",
        type=str,
        help="namespaces to include for action , supported values [<namespace> ]",
    )
    parser.add_argument(
        "env",
        metavar="E",
        type=str,
        help="Environment , supported values[dev, qa, apiprod]",
    )
    parser.set_defaults(
        func=main,
    )
