"""
    Holds the query to update document access control
"""


def update_document_access_control_query(document_access_json_list: dict):
    """
    Update document access control
    """
    return {
        "query": """
     mutation upsert_document_access_controls($data: [document_access_controls_insert_input!] !) {
    insert_document_access_controls(
        objects: $data, on_conflict: {
        constraint: document_access_controls_pkey,
        update_columns: [object_meta, access_controls, folder, options, metadata, permitted_access, loantype, persona, type_meta]
    }) {
        returning {
            id object_meta type_meta loantype persona access_controls folder options metadata permitted_access
        }
    }
}""",
        "variables": {"data": document_access_json_list},
    }
