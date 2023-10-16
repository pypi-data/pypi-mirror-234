"""
    handles the workflow
"""
from reva.lib.autotest_runner.main import RunnerInitializer

def main(argument):
    """
        calls the action
    """
    return RunnerInitializer(arguments=argument).start()


def autotest(parser):
    """
        handles the workflow
    """
    parser.add_argument('--file_path', metavar ='FP', type = str,  required=True,
                        help ='Namespace to test, possible values [/home/makesh/test.json]')

    parser.add_argument('--file_location', metavar ='FL', type = str,  required=True,
                        help ='Namespace to test, possible values [local, s3]')
    parser.add_argument('--bucket', metavar ='FL', type = str,  required=False,
                        help ='Namespace to test, possible values [local, s3]')
    
    parser.add_argument('--platform', metavar='P', type =  str, default="remote",
                        help = "where to run the lambda, possible values [remote, local]")

    parser.set_defaults(func=main,)