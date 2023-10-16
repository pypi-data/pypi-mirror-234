"""
    This module will get the json from file paths
"""
import json
import csv
from os.path import exists as file_exists
from reva.exception import FileNotExistsError


class FileGetterStore:
    """
    This class will get the files
    """
    @property
    def csv_data(self):
        """
            This function return the csv getter
        """
        return CsvFileGetter()

    @property
    def json_data(self):
        """
            This function return the json getter
        """
        return JsonFileGetter()

class FileGetter:
    """
        This class is base for all file getter
    """
    def is_exists(self, file_path: str) -> dict:
        """
        This function will get json file by path
        """
        if not file_exists(file_path):
            raise FileNotExistsError(
                "Config file does not exists, please configure the file at path =>"
                + file_path
            )

class JsonFileGetter(FileGetter):
    """
    This class will get the json files from paths
    """

    def get_file_by_path(self, file_path: str) -> dict:
        """
        This function will get json file by path
        """
        self.is_exists(file_path=file_path)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def get_file_by_paths(self, file_paths: list) -> list:
        """
        THis function will return list of json files
        """
        result = []
        for file_path in file_paths:
            result.append(self.get_file_by_path(file_path))
        return result

    def get_json_files_by_path(self, file_paths: list) -> list:
        """
        This function will return list of json data with file paths
        This function is to support update and create
        once we support update and create in workflow, sitesettings and loanproducts
        we will depreciate the above function get_file_by_paths
        """
        result = []
        for file_path in file_paths:
            result.append(
                {"path": file_path, "json_data": self.get_file_by_path(file_path)}
            )
        return result


class CsvFileGetter(FileGetter):
    """
    This class will load the csv files
    """

    def get_file_data(self, file_path: str):
        """
        This function will return the files data
        """
        self.is_exists(file_path=file_path)
        all_data = []
        with open(file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                all_data.append(row)
        return all_data
