"""
    This module will provide the paths
"""
import os
from reva.exception import EnvPathNotConfigured


class PathGetter:
    """
    This class will hold the functions to get paths
    """

    def __init__(self):
        self.root_path = self.get_root_path()

    def get_root_path(self):
        """
        This function returns the root path
        """
        try:
            home_path = os.environ["LENDSMART_REVA_HOME"]
        except KeyError as err:
            home_path = ""
            print("error on accessing home path", err)
        if not home_path:
            raise EnvPathNotConfigured(
                "Root home path is not configured in LENDSMART_REVA_HOME"
            )
        return home_path

    def get_reva_ui_home_path(self):
        """
        Returns the ui home path
        """
        try:
            ui_home_path = os.environ["LENDSMART_REVA_UI_HOME"]
        except KeyError as err:
            print("error on accessing ui home path", err)
            ui_home_path = ""
        if not ui_home_path:
            raise EnvPathNotConfigured(
                "UI home path is not configured in LENDSMART_REVA_UI_HOME"
            )
        return ui_home_path

    def get_reva_worklet_home_path(self):
        """
        Returns the worklet home path
        """
        try:
            worklet_home_path = os.environ["LENDSMART_REVA_WORKLET_HOME"]
        except KeyError as err:
            print("error on accessing worklet home path", err)
            worklet_home_path = ""
        if not worklet_home_path:
            raise EnvPathNotConfigured(
                "Worklet home path is not configured in LENDSMART_REVA_WORKLET_HOME"
            )
        return worklet_home_path

    def get_config_path(self):
        """
        Returns the config path
        """
        return self.get_root_path() + "/config.json"

    def get_ui_customization_path(self):
        """
        This function will return the ui customization path
        """
        return self.get_reva_ui_home_path() + "/packages/lendsmart_ui/customization/"

    def get_ui_config_path(self, namespace: str):
        """
        This function will return the ui config path
        """
        return self.get_ui_customization_path() + namespace + "/config"

    def concat_files_with_folder(self, list_of_files : list, folder_path :str):
        """
            This function will return the file paths
        """
        file_paths = []
        for file_name in list_of_files:
            file_paths.append(
                folder_path + "/" + file_name
            )
        return file_paths

    def get_files_with_prefix(self, folder_path : str, prefix_list : list):
        """
            Returns the list of file paths
        """
        all_files = os.listdir(folder_path)
        wanted_files = prefix_list
        filtered_paths = [mf for mf in all_files if mf[0:4] in wanted_files]
        return self.concat_files_with_folder(
            filtered_paths, folder_path
        )

    def get_file_paths_ui(self, namespaces : list, prefixes : list):
        """
            Returns the file paths for ui configs with matching prefix
        """
        files_to_update = []
        for namespace in namespaces:
            files_to_update.extend(
                self.get_files_with_prefix(
                    self.get_ui_config_path(namespace), prefixes
                    )
            )
        return files_to_update

    def get_worklets_deploy_json_path(self, args):
        """
            Returns deploy json file path from worklet based on env
        """
        if args.env in ["dev", "qa"]:
            return [self.get_reva_worklet_home_path() + "/deploy/qadeploy.json"]

        if args.env in ["prod"]:
            return [self.get_reva_worklet_home_path() + "/deploy/proddeploy.json"]
        return []

    def get_ui_deploy_json_path(self, args) -> list:
        """
            Returns the deploy json path from UI based on the env
        """
        if args.env in ["dev"]:
            return self.get_ui_config_path("systemdev") + "/deploy.json"

        if args.env in ["qa"]:
            return self.get_ui_config_path("systemqa") + "/deploy.json"

        if args.env in ["apiprod"]:
            return self.get_ui_config_path("systemprod") + "/deploy.json"

        return []
