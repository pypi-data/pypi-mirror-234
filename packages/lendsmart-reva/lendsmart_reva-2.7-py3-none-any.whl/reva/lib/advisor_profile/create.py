"""
    handles the AdvisorProfileUpdateOrCreate
"""
import json
import requests
from ramda import path_or
from reva.lib.utils.get_namespaces import get_namespace_by_argument_and_path
from reva.lib.base.base import RevaCreate
from reva.lib.utils.address import address_to_json
from reva.lib.graphql_queries.advisor_profiles import (
    get_accounts_query,
    create_advisor_query,
    get_advisor_profiles_by_email_namespace,
)
from reva.lib.graphql_queries.branch import get_branch_by_code_query


class AdvisorProfileCreate(RevaCreate):
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
        return self.get_file_paths_ui(namespaces_to_update, ["ADP_"])

    def get_converted_flag(self, flag_value: str):
        """
        This function will return the correct flag
        matching
        """
        true_flags = ["true", "TRUE", "yes", "YES", "Yes", "True", True]
        false_flags = ["false", "FALSE", "no", "NO", "No", "False", False]
        if flag_value in true_flags:
            return "true"
        if flag_value in false_flags:
            return "false"
        return "false"

    def _mk_account(self, advisor_profile_data: dict) -> dict:
        """
        create account
        """
        user_name = path_or("", ["advisor_name"], advisor_profile_data)
        roles_id = path_or("", ["roles_id"], advisor_profile_data).split(",")
        roles_id = [role_id for role_id in roles_id if role_id]
        data = {
            "email": path_or("", ["email"], advisor_profile_data),
            "object_meta": {"namespace": self.argument.namespace},
            "type_meta": {"kind": "Account", "api_version": "v1"},
            "namespace_id": path_or("", ["id"], self.namespace_data),
            "first_name": path_or("", [0], user_name.split(" ")),
            "last_name": path_or("", [1], user_name.split(" ")),
            "home_phone": path_or("", ["phone"], advisor_profile_data),
            "is_admin": False,
            "status": "Active",
            "avatar": path_or("", ["avatar"], advisor_profile_data),
            "roles_id": roles_id if roles_id else [],
            "metadata": {
                "role": path_or("loan_officers", ["persona"], advisor_profile_data)
                or "loan_officers",
                "lendsmart_sh/nmls": path_or("", ["nmls"], advisor_profile_data),
                "lendsmart_sh/title": path_or("", ["title"], advisor_profile_data),
                "profile_url": path_or("", ["my_site"], advisor_profile_data),
                "company_address": path_or("", ["address"], advisor_profile_data),
                "branch_nmls": path_or("", ["branch_nmls"], advisor_profile_data),
                "lendsmart_sh/enable_login_timeout": self.get_converted_flag(
                    path_or("", ["enable_login_timeout"], advisor_profile_data)
                ),
                "lendsmart_sh/enable_mfa": self.get_converted_flag(
                    path_or("", ["enable_mfa"], advisor_profile_data)
                ),
            },
            "password": path_or("", ["password"], advisor_profile_data) or "Speed#123",
            "sso": {"is_enable_sso": False},
        }
        return data

    def get_branch_by_code(self, branch_code: str) -> dict:
        """
        THis function get the branch by code
        """
        query_data = get_branch_by_code_query(branch_code=branch_code)
        branch_response = self.excecute_for_single_query_data(query_data=query_data)
        return path_or("", ["data", "branches", 0], branch_response)

    def get_branch_ids(self, branch_codes: list) -> list:
        """
        THis function will create
        """
        branch_ids = []
        for branch_code in branch_codes:
            branch = self.get_branch_by_code(branch_code=branch_code)
            if not branch:
                continue
            branch_ids.append(path_or("", ["id"], branch))
        return branch_ids

    def _mk_advisor_data(self, account_data: dict, advisor_profile_data: dict):
        """
        This function create advisor profile
        """
        branch_codes = path_or("", ["branch_code"], advisor_profile_data).split(",")
        branch_ids = self.get_branch_ids(branch_codes=branch_codes)
        email = path_or("", ["email"], account_data)
        email_prefix = path_or("", [0], email.split("@"))
        user_name = path_or("", ["advisor_name"], advisor_profile_data)
        company_address = path_or(
            "", ["company_address"], advisor_profile_data
        ) or path_or("", ["company_address"], account_data)
        first_name = path_or("", [0], user_name.split(" "))
        last_name = path_or("", [1], user_name.split(" "))
        data = {
            "account_id": path_or("", ["id"], account_data),
            "namespace_id": path_or("", ["id"], self.namespace_data),
            "type_meta": {"kind": "AdvisorProfile", "api_version": "v1"},
            "object_meta": {
                "name": path_or("", ["email"], account_data),
                "labels": {},
                "account": path_or("", ["id"], account_data),
                "annotations": {},
                "owner_references": [],
                "namespace": self.argument.namespace,
            },
            "source_id": path_or("", ["id"], account_data),
            "email": path_or("", ["email"], account_data),
            "first_name": first_name,
            "last_name": last_name,
            "address": address_to_json(company_address),
            "gender": path_or("", ["gender"], advisor_profile_data),
            "birth_day": path_or("", ["birth_day"], advisor_profile_data),
            "branches": branch_ids,
            "social_security_no": path_or(
                "", ["social_security_no"], advisor_profile_data
            ),
            "phone": path_or("", ["phone"], advisor_profile_data),
            "business_name": first_name + " " + last_name,
            "license": {
                "lendsmart_sh/mls_id": path_or("", ["nmls"], advisor_profile_data)
            },
            "metadata": {
                "lendsmart_sh/title": path_or("", ["title"], advisor_profile_data),
                "lendsmart_sh/profile_url": path_or(
                    "", ["my_site"], advisor_profile_data
                ),
                "lendsmart_sh/display_location": company_address,
                "lendsmart_sh/business_location": company_address,
            },
            "persona": path_or("loan_officers", ["persona"], advisor_profile_data)
            or "loan_officers",
            "description": path_or("", ["description"], advisor_profile_data),
            "avatar": path_or("", ["avatar"], advisor_profile_data),
            "user_name": email_prefix.replace(".", "-"),
            "status": {
                "phase": "Pending",
                "reason": "initalize new advisor profile",
                "conditions": [
                    {
                        "condition_type": "ProfileCompleted",
                        "message": "",
                        "reason": "",
                        "status": "ProfileCompleted",
                        "last_update_time": "",
                        "last_transition_time": "",
                        "last_probe_time": "",
                    }
                ],
            },
        }
        return data

    def create_advisor_profiles(self, account_data: dict, advisor_data: dict):
        """
        This function will create advisor profiles
        """
        email = path_or("", ["email"], account_data)
        old_advisor_profile_query_data = get_advisor_profiles_by_email_namespace(
            email=email, namespace=self.argument.namespace
        )
        old_advisor_profile_response = self.excecute_for_single_query_data(
            query_data=old_advisor_profile_query_data
        )
        old_advisor_data = path_or(
            "", ["data", "advisor_profiles", 0], old_advisor_profile_response
        )
        if old_advisor_data:
            print("-----Advisor profiles already created--", email)
            return old_advisor_data
        advisor_create_data = self._mk_advisor_data(
            account_data=account_data, advisor_profile_data=advisor_data
        )
        query_data = create_advisor_query(advisor=advisor_create_data)
        new_advisor_data = self.excecute_for_single_query_data(query_data=query_data)
        return path_or("", ["data", "insert_advisor_profiles_one"], new_advisor_data)

    def get_accounts(self, email: str) -> dict:
        """
        This function get the account data by email
        """
        query_data = get_accounts_query(
            namespace=self.argument.namespace, email=email.lower()
        )
        account_data = self.excecute_for_single_query_data(query_data=query_data)
        return path_or({}, ["data", "accounts", 0], account_data)

    def create_account(self, advisor_data: dict):
        """
        This function creats account
        """
        old_account = self.get_accounts(email=path_or("", ["email"], advisor_data))
        if old_account:
            print(
                "---------Account already exists", path_or("", ["email"], advisor_data)
            )
            account_response = old_account
        else:
            url = "{}/{}/accounts".format(
                self.client_builder.get_api_root(), self.argument.namespace
            )
            new_account_data = self._mk_account(advisor_profile_data=advisor_data)
            response = requests.post(url, json=new_account_data)
            account_response = json.loads(response.text)
        return account_response

    def start(self):
        """
        update the document access control
        """
        advisor_profile_csv_path = path_or("", [0], self.get_paths_to_create())
        if not advisor_profile_csv_path:
            return {}
        advisor_profile_json_data_list = self.csv_data.get_file_data(
            file_path=advisor_profile_csv_path
        )
        for advisor_data in advisor_profile_json_data_list:
            account_create_response = self.create_account(advisor_data=advisor_data)
            advisor_profile_create = self.create_advisor_profiles(
                account_data=account_create_response, advisor_data=advisor_data
            )
            print("------------account resposne----", account_create_response)
            print("---- advisor response --", advisor_profile_create)
        return {}
