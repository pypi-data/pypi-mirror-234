"""
    handles the document access control
"""
from reva.lib.document_access_control.main import DocumentAccessControl


def main(argument):
    """
    calls the action
    """
    return DocumentAccessControl(argument).run()


def document_access_control(parser):
    """
        handles document access control \
        usage - > reva documentaccesscontrol update csbnetdev qa
    """
    parser.add_argument(
        "action",
        metavar="A",
        type=str,
        help="action for document access control,  supported values [update, list]",
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
