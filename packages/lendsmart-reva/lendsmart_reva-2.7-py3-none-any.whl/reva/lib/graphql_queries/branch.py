"""
    query for branch
"""


def update_or_create_branch_query(branches: list):
    """
    Update loan products
    """
    return {
        "query": """
mutation MyMutation($data: [branches_insert_input!]!) {
  insert_branches(objects: $data, on_conflict: {
    constraint: branches_pkey,
    update_columns: [id, namespace_id, type_meta, object_meta, name, code, reports_to_branch, address , mailing_address, metadata]}) {
      returning {
        name
        code
        address
      }
    }
  }""",
        "variables": {"data": branches},
    }


def get_branch_by_code_query(branch_code: str):
    """
    THis function will return query for getting branch
    """
    return {
        "query": """
      query get_branch($code: String) {
        branches(where: {_and:[
           {code: {_eq: $code}}
      ]
    }) {
          id
          code
          name
        }
      }
    """,
        "variables": {"code": branch_code},
    }
