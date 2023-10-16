"""
    Main file for reva cli
"""
#pylint: disable=W0702,w1201,C0103,C0209
import traceback
import argparse
import logging
import textwrap
import sys
import pkg_resources
import reva

LOG = logging.getLogger(__name__)


__header__ = textwrap.dedent(
    f"Full documentation can be found at:  \
        {reva.__version__}"
)


def log_flags(args, logger=None):
    """
    This function will log flags
    """
    logger = logger or LOG
    logger.info("lendsmart - reva options:")

    for key, value in args.__dict__.items():
        if key.startswith("_"):
            continue
        logger.info(" %-30s: %s" % (key, value))


def get_parser():
    """
    This function return the parser
    """
    epilog_text = "See 'reva <command> --help' for help on a specific command "
    parser = argparse.ArgumentParser(
        prog="reva",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Easy reva deployment",
        epilog=epilog_text,
    )
    verbosity = parser.add_mutually_exclusive_group(required=False)
    verbosity.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        default=False,
        help="be more verbose",
    )
    verbosity.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        dest="quiet",
        help="be less verbose",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{reva.__version__}",
        help="the current installed version of reva",
    )
    sub = parser.add_subparsers(
        title="commands",
        metavar="COMMAND",
        help="description",
    )
    sub.required = True
    entry_points = [
        (ep.name, ep.load()) for ep in pkg_resources.iter_entry_points("reva.cli")
    ]
    entry_points.sort(
        key=lambda name_fn: getattr(name_fn[1], "priority", 100),
    )
    for (name, function) in entry_points:
        p = sub.add_parser(
            name,
            description=function.__doc__,
            help=function.__doc__,
        )
        # flag if the default release is being used
        p.set_defaults(default_release=False)
        function(p)
        p.required = True

    return parser

def _main(args=None):
    # Set console logging first with some defaults, to prevent having exceptions
    # before hitting logging configuration. The defaults can/will get overridden
    # later.

    # Console Logger
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.INFO)

    # because we're in a module already, __name__ is not the ancestor of
    # the rest of the package; use the root as the logger for everyone
    root_logger = logging.getLogger()

    # allow all levels at root_logger, handlers control individual levels
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_logger)

    parser = get_parser()
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()
    else:
        args = parser.parse_args(args=args)
    return args.func(args)


def main(args=None):
    """
        This is the main function
    """
    try:
        _main(args=args)
    except Exception as err:
        print("Error ==>",err)
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        sys.exit(1)
    finally:
        try:
            sys.stdout.close()
        except Exception as err:
            print("Error =>",err)
            pass
        try:
            sys.stderr.close()
        except:
            pass
