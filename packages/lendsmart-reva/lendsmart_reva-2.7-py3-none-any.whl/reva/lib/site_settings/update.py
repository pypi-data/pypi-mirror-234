"""
    update the site settings
"""
# pylint: disable=W0718, R0901
from ramda import path_or
from reva.lib.utils.get_namespaces import get_namespace_by_argument_and_path
from reva.lib.base.base import RevaUpdate
from reva.lib.base.site_settings import SiteSettings
from reva.lib.utils.filter_data_with_id import filter_data_with_id
from reva.lib.client.builder import ClientBuilder


class SiteSettingsUpdate(RevaUpdate):
    """
    update the site settings
    """

    def __init__(self, arguments):
        super().__init__(arguments)
        self.argument = arguments
        self.ls_client = ClientBuilder(self.conf).lendsmart_api(arguments)
        self.site_settings_obj = SiteSettings().set_ls_client(self.ls_client)

    def get_json_paths_to_update(self):
        """
        THis function will return the json files
        to update
        """
        namespaces_to_update = get_namespace_by_argument_and_path(
            self.argument, self.get_ui_customization_path()
        )
        return self.get_file_paths_ui(namespaces_to_update, ["STS_"])

    def get_list_of_site_settings(self):
        """
            returns a list of site settings
        """
        return self.get_file_by_paths(self.get_json_paths_to_update())

    def _update(self, list_of_site_settings: list):
        """
            updates all the site settings in the list
        """
        for json_data in list_of_site_settings:
            site_settings = filter_data_with_id(path_or([],["data"], json_data))
            if not site_settings:
                continue
            print("======Payload: ", site_settings[0])
            self.site_settings_obj.update(path_or({}, [0], site_settings))

    def start(self) -> None:
        """
        update the site settings
        """
        return self._update(self.get_list_of_site_settings())
