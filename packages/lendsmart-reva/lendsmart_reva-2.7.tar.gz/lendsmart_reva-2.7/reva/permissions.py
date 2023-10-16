"""
    handles the permissions
"""

from reva.lib.permissions.main import Permissions

def main(argument):
    """
    calls the action
    """
    return Permissions(argument).run()


def permissions(parser):
    """
        handles permissions and permissions \
        usage - > reva permissions update csbnetdev qa
    """
    parser.add_argument(
        "action",
        metavar="A",
        type=str,
        help="action for permissions,  supported values [update, list]",
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
