"""
    handles the site settings
"""
from reva.lib.site_settings.main import SiteSettings

def main(argument):
    """
        calls the action
    """
    return SiteSettings(argument).run()


def site_settings(parser):
    """
        handles the site settings \
        usage - > reva sitesettings update csbnetdev qa
    """
    parser.add_argument('action', metavar ='A', type = str,
                        help ='action for site settings, supported values [update, list]')
    parser.add_argument('namespace', metavar ='N', type = str,
                        help ='namespaces to include for action , supported values [all, <namespace> ]')
    parser.add_argument('env', metavar ='E', type = str,
                        help ='Environment , supported values[dev, qa, tao, prod, apiprod]')
    parser.set_defaults(
        func=main,
        )
