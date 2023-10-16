"""
    handles the advisor profile creation and updation
"""
from reva.lib.advisor_profile.main import AdvisorProfile


def main(argument):
    """
    calls the action
    """
    return AdvisorProfile(arguments=argument).run()


def advisor_profile(parser):
    """
        handles advisor profile \
        usage - > reva advisorprofile updateorcreate rsntdev qa
    """
    parser.add_argument(
        "action",
        metavar="A",
        type=str,
        help="action for advisorprofile,  supported values [create]",
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
