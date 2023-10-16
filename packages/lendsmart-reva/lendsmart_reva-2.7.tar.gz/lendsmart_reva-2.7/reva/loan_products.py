"""
    handles the loan productus
"""
from reva.lib.loan_productus.main import LoanProducts


def main(argument):
    """
    calls the action
    """
    return LoanProducts(argument).run()


def loan_products(parser):
    """
        handles loan_products \
        usage - > reva loanproducts update csbnetdev qa
    """
    parser.add_argument(
        "action",
        metavar="A",
        type=str,
        help="action for loan_products,  supported values [update, list]",
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
