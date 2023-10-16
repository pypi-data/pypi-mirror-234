"""
    update the document access control
"""
from ramda import path_or
from reva.lib.utils.get_namespaces import get_namespace_by_argument_and_path
from reva.lib.base.base import RevaUpdate
from reva.lib.graphql_queries.document_access_control import (
    update_document_access_control_query,
)
from reva.lib.utils.filter_data_with_id import filter_data_with_id

class DocumentAccessControlUpdate(RevaUpdate):
    """
    update the document access control
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
        return self.get_file_paths_ui(namespaces_to_update, ["DAC_"])

    def start(self):
        """
        update the document access control
        """
        document_access_control_json_data = self.get_json_files_by_path(
            self.get_json_paths_to_update()
        )
        query_datas = []
        for json_data in document_access_control_json_data:
            filtered_json_data = filter_data_with_id(path_or([],["json_data","data"], json_data))
            if not filtered_json_data:
                continue
            query_datas.append(
                update_document_access_control_query(
                    filtered_json_data
                )
            )
        return self.excecute_for_list_of_query_data(query_datas)
