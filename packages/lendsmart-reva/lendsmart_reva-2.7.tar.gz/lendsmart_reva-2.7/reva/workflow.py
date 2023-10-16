"""
    handles the workflow
"""
from reva.lib.workflow.main import Workflow

def main(argument):
    """
        calls the action
    """
    return Workflow(argument).run()


def workflow(parser):
    """
        handles the workflow \
            usage - > reva workflow update csbnetdev qa
    """
    parser.add_argument('action', metavar ='U', type = str,
                        help ='action for workflow, supported values [update, list]')
    parser.add_argument('namespace', metavar ='N', type = str,
                        help ='namespaces to include for action , supported values [all, <namespace> ]')
    parser.add_argument('env', metavar ='E', type = str,
                        help ='Environment , supported values[dev, qa, tao, prod, apiprod]')
    parser.set_defaults(
        func=main,
        )
