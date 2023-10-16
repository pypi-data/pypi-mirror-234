"""
    Handles the site settings
"""
from lendsmart_api.lendsmart_client import LendsmartClient
from lendsmart_api.errors import ApiError
from ramda import path_or

GET_SITE_SETTINGS = "/{}/site_settings"
UPDATE_SITE_SETTINGS = "/{}/site_settings/{}"

class SiteSettings:
    """
    This class will handle the site setting api
    """
    def __init__(self)->None:
        """
            This function initialize the arttributes
        """
        self._ls_client = None

    def set_ls_client(self, ls_client : LendsmartClient)->'SiteSettings':
        """
            set the lendsmart client
        """
        self._ls_client = ls_client
        return self

    def get(self) -> dict:
        """
        This function will get the the site settings
        """
        try:
            response = self._ls_client.get(
                GET_SITE_SETTINGS.format(
                    self._ls_client.tenant_namespace
                )
            )
            return response
        except ApiError as err:
            print("======Error happened while fetching site settings", err)
            return {}

    def update(self, data: dict) -> dict:
        """
        This function will update the the site settings
        """
        try:
            response = self._ls_client.put(
                UPDATE_SITE_SETTINGS.format(
                    self._ls_client.tenant_namespace,
                    path_or("", ["id"], data)
                ),
                data=data,
            )
            return response
        except ApiError as err:
            print("======Error happened while fetching site settings", err)
            return {}

    def __str__(self) -> str:
        pass
