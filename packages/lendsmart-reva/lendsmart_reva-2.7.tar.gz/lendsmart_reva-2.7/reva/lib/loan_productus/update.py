"""
    update the workflow
"""
from ramda import path_or
from reva.lib.utils.get_namespaces import get_namespace_by_argument_and_path
from reva.lib.base.base import RevaUpdate
from reva.lib.graphql_queries.loan_products import update_loan_products_query
from reva.lib.utils.filter_data_with_id import filter_data_with_id

class LoanProductsUpdate(RevaUpdate):
    """
    update the loan products
    """

    def __init__(self, arguments):
        super().__init__(arguments)
        self.argument = arguments

    def get_json_paths_to_update(self):
        """
        THis function will return the json files
        to update
        """
        namespaces_to_update = get_namespace_by_argument_and_path(
            self.argument, self.get_ui_customization_path()
        )
        return self.get_file_paths_ui(namespaces_to_update, ["LPD_"])

    def start(self):
        """
        update the workflow
        """
        loan_products_json_data = self.get_file_by_paths(
            self.get_json_paths_to_update()
        )
        query_datas = []
        for loan_products in loan_products_json_data:
            filtered_json_data = filter_data_with_id(path_or([],["data"], loan_products))
            if not filtered_json_data:
                continue
            query_datas.append(
                update_loan_products_query(
                    filtered_json_data
                )
            )
        return self.excecute_for_list_of_query_data(query_datas)
