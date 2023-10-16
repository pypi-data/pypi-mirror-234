"""
    Holds the query to update site settings
"""


def update_site_settings_query(site_settings: dict):
    """
    Update site settings
    """
    return {
        "query": """
     mutation update_site_settings($data: [site_settings_insert_input!]!) {
        insert_site_settings(objects: $data, on_conflict: {constraint: site_settings_pkey, update_columns: [company_url, theme, metadata, updated_at, settings, capabilities, object_meta]}) {
        returning {
             id
             metadata
         }
       }
     }""",
        "variables": {"data": site_settings},
    }
