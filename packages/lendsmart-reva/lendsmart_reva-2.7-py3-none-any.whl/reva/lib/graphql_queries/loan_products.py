"""
    Holds the query to update loan products
"""


def update_loan_products_query(loan_products: list):
    """
    Update loan products
    """
    return {
        "query": """
mutation MyMutation($data: [loan_products_insert_input!]!) {
  insert_loan_products(objects: $data, on_conflict: {
    constraint: loan_products_pkey,
    update_columns: [object_meta, metadata, product_visual_name, product_name, description, services, subproducts]}) {
      returning {
        id
        product_name
        product_visual_name
        services
        subproducts
      }
    }
  }""",
        "variables": {"data": loan_products},
    }
