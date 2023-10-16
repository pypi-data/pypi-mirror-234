"""
    This module will show the information
"""
import logging
import reva
from reva.lib.utils.get_paths import PathGetter


LOG = logging.getLogger(__name__)

def show(parser):
    """
        shows the info
    """
    LOG.info("Lendsmart Reva version "+ reva.__version__)
    parser.set_defaults(
        func=callable,
        )

def is_ready(parser):
    """
        checks if reva is ready
    """
    PathGetter().get_root_path()
    if parser.repos == "ui":
        PathGetter().get_reva_ui_home_path()
        print("===UI IS READY")
    if parser.repos == "worklet":
        PathGetter().get_reva_worklet_home_path()
        print("===Worklet IS READY")
    return True

def ready(parser):
    """
        This will check does the environment is ready or not
    """
    parser.add_argument('repos', metavar ='U', type = str,
                        help ='update the workflow')

    parser.set_defaults(
        func=is_ready,
        )
    