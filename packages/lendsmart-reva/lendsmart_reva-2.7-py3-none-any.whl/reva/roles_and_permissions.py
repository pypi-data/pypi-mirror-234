"""
    handles the roles and permissions
"""

from reva.lib.roles_and_permissions.main import RolesAndPermission

def main(argument):
    """
    calls the action
    """
    return RolesAndPermission(argument).run()


def roles_and_permissions(parser):
    """
        handles roles and permissions \
        usage - > reva rolesandpermissions update csbnetdev qa
    """
    parser.add_argument(
        "action",
        metavar="A",
        type=str,
        help="action for rolesandpermissions,  supported values [update, list]",
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
