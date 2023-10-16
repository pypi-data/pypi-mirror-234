"""
    create advisor profiles
"""


def create_advisor_query(advisor):
    """
    create advisor profiles
    """
    return {
        "query": """mutation create_advisor($advisor: advisor_profiles_insert_input!) {
                insert_advisor_profiles_one(object: $advisor) {
       		       id
                   email
                   account_id
    			   namespace_id
                   address
                   first_name
                   last_name
                   persona
                   avatar
                   object_meta
                   metadata
                }
            }""",
        "variables": {"advisor": advisor},
    }


def get_advisor_profiles_by_email_namespace(email, namespace):
    '''
		THis function will return query for getting list of
		advisor profiles by namespace
	'''
    return {
        "query": '''
      query list_group_by_account_id($email: String, $object_meta: jsonb) {
        advisor_profiles(where: {_and:[
           {object_meta: {_contains: $object_meta}}
           {email: {_eq: $email}}
      ]
    }) {
          id
          source_id
          email
        }
      }
    ''',
        "variables": {"email": email, "object_meta": {"namespace":  namespace}}
    }


def get_accounts_query(namespace, email):
    """
    get accounts
    """
    return {
        "query": """query get_accounts($email: String!, $object_meta: jsonb!) {
        accounts(where: {email: {_eq: $email}, _and: {object_meta: {_contains: $object_meta}}}) {
            id
            type_meta
            email
            first_name
            last_name
            home_phone
            avatar
            status
            object_meta
            metadata
            updated_at
            created_at
            is_admin
            namespace_id
            roles_id
            sso
        }
        }""",
        "variables": {"email": email, "object_meta": {"namespace": namespace}},
    }
