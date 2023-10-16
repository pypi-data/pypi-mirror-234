"""
    handles the roles and permissions
"""

from reva.lib.roles.main import Roles

def main(argument):
    """
    calls the action
    """
    return Roles(argument).run()


def roles(parser):
    """
        handles roles and permissions \
        usage - > reva roles update csbnetdev qa
    """
    parser.add_argument(
        "action",
        metavar="A",
        type=str,
        help="action for roles,  supported values [update, list]",
    )
    parser.add_argument(
        "namespace",
        metavar="N",
        type=str,
        help="namespaces to include for action , supported values [all, <namespace> ]",
    )
    parser.add_argument(
        "env",
        metavar="E",
        type=str,
        help="Environment , supported values[dev, qa, tao, prod, apiprod]",
    )
    parser.set_defaults(
        func=main,
    )
