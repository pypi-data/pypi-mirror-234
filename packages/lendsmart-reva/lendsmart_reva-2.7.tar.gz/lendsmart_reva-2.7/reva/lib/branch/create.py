"""
    update the document access control
"""
from ramda import path_or
from reva.lib.utils.get_namespaces import get_namespace_by_argument_and_path
from reva.lib.base.base import RevaCreate
from reva.lib.utils.address import address_to_json
from reva.lib.graphql_queries.branch import (
    update_or_create_branch_query,
    get_branch_by_code_query,
)


class BranchCreate(RevaCreate):
    """
    update the document access control
    """

    def __init__(self, arguments):
        super().__init__(arguments)
        self.argument = arguments
        self.namespace_data = self.get_namespace()

    def get_paths_to_create(self):
        """
        THis function will return the json files
        to update
        """
        namespaces_to_update = get_namespace_by_argument_and_path(
            self.argument, self.get_ui_customization_path()
        )
        return self.get_file_paths_ui(namespaces_to_update, ["BNL_"])

    def get_branch_by_code(self, branch_code: str) -> dict:
        """
        THis function get the branch by code
        """
        query_data = get_branch_by_code_query(branch_code=branch_code)
        branch_response = self.excecute_for_single_query_data(query_data=query_data)
        return path_or("", ["data", "branches", 0], branch_response)

    def _mk_branch_data(self, branch_list: list):
        """
        This function will create a branch api structure from csv or json data
        """
        result = []
        converted_branch_codes = []  # to avoid duplicates
        for branch in branch_list:
            branch_code = path_or("", ["branch_code"], branch)
            already_branch_exists = self.get_branch_by_code(branch_code=branch_code)
            if already_branch_exists:
                print("---------branch already existis---  ", branch_code)
                continue
            brach_uid = path_or("", ["id"], branch)
            if branch_code in converted_branch_codes:
                continue
            converted_branch_codes.append(branch_code)
            data = {
                "object_meta": {"namespace": self.argument.namespace},
                "type_meta": {"kind": "Branches", "api_version": "v1"},
                "namespace_id": path_or("", ["id"], self.namespace_data),
                "name": path_or("", ["branch_name"], branch),
                "code": branch_code,
                "reports_to_branch": {},
                "address": address_to_json(address=path_or("", ["address"], branch)),
                "mailing_address": address_to_json(
                    address=path_or("", ["mailing_address"], branch)
                ),
                "metadata": {},
                "updated_at": "now()",
            }
            if brach_uid:
                data["id"] = int(brach_uid)
            result.append(data)
        return result

    def start(self):
        """
        update the document access control
        """
        branches_csv_path = path_or("", [0], self.get_paths_to_create())
        if not branches_csv_path:
            return {}
        branch_json_data_list = self.csv_data.get_file_data(file_path=branches_csv_path)
        converted_branch_data = self._mk_branch_data(branch_list=branch_json_data_list)
        print("branch list===>", converted_branch_data)
        query_data = update_or_create_branch_query(branches=converted_branch_data)
        return self.excecute_for_single_query_data(query_data=query_data)
