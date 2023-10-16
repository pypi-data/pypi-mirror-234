"""
    This module will have the graphql query
"""

def update_workflow_intent_query(workflow_intent: list):
    """
    Update workflow intent
    """
    return {
        "query": """
     mutation update_site_workflow_intents($data: [site_workflow_intents_insert_input!]!) {
        insert_site_workflow_intents(objects: $data, on_conflict: {constraint: site_workflow_intents_pkey, update_columns: [intents,sections,initializer,question_groups,product_id,object_meta,product_name,product_id,role,metadata]}) {
        returning {
             id
             metadata
             object_meta
             intents
             product_name 
            sections
            initializer
            question_groups
         }
       }
     }""",
        "variables": {"data": workflow_intent}
    }
