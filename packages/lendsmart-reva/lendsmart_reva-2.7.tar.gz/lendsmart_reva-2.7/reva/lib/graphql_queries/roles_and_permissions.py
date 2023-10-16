"""
    Holds the query to update roles and permissions
"""
# pylint: disable=C0103,W0622
def get_roles_by_namespace(namespace):
    '''
		THis function will return query for getting list of
		roles by namespace
    '''
    return {
        "query": '''
         	query get_roles($object_meta: jsonb) {
  		    roles(where: {object_meta: {_contains: $object_meta}}) {
              id
              object_meta
              name
              namespace_id
              type_meta
              updated_at
              description
              created_at
            }
		      }''',
        "variables": {
            "object_meta": {"namespace":  namespace}
        }
    }

def get_permissions_by_namespace(namespace):
    '''
		THis function will return query for getting list of
		permissions by namespace
    '''
    return {
        "query": '''
         	query get_permissions($object_meta: jsonb) {
          roles(where: {object_meta: {_contains: $object_meta}}) {
                      id,
                      name,
                    permissions {
                        id
                        description
                        metadata
                        name
                        options
                        role_id
                        updated_at
                        created_at
                      }
              }		      

          }''',
        "variables": {
            "object_meta": {"namespace":  namespace}
        }
    }

def delete_role_by_id(id: str):
    """
	Delete role at ID
    """
    return {
		"query": """
			mutation delete_roles($role_id: bigint!) {
				delete_roles(where: {id: {_eq: $role_id}}) 
    				{
						affected_rows
					}
		}
 	""",
        "variables": {
            "role_id": id
        }
	}

def delete_permission_by_role_id(id: str):
    """
	Delete permission with role_id
    """
    return {
		"query": """
			mutation delete_permissions($role_id: bigint!) {
				delete_permissions(where: {role_id: {_eq: $role_id}}) 
    				{
						affected_rows
					}
		}
 	""",
        "variables": {
            "role_id": id
        }
	}

def delete_permission_by_id(id: str):
    """
	Delete permission at ID
    """
    return {
		"query": """
			mutation delete_permissions($permission_id: bigint!) {
				delete_permissions(where: {id: {_eq: $permission_id}}) 
    				{
						affected_rows
					}
		}
 	""",
        "variables": {
            "permission_id": id
        }
	}

def upsert_roles_query(roles_data_list: list):
    """
    Update roles query
    """
    return {
        "query": """
     	mutation upsert_roles($data: [roles_insert_input!]!) {
	    insert_roles(
			objects: $data, on_conflict: 
			{constraint: roles_pkey, update_columns: [object_meta,name,namespace_id,type_meta,updated_at,description]}
          )
		{
			returning {
				id
				object_meta
				name
				namespace_id
				type_meta
				updated_at
				description
			}
		}
		}""",
			"variables": {"data": roles_data_list},
	}

def upsert_permissions_query(permissions_data_list: list):
    """
    Update permissions query
    """
    return {
        "query": """
     	mutation upsert_permissions($data: [permissions_insert_input!]!) {
		insert_permissions(
				objects: $data, on_conflict:
				{constraint: permissions_pkey, update_columns: [description,metadata,name,options,role_id,updated_at]}
			)
			{
				returning {
					id
					description
					metadata
					name
					options
					role_id
					updated_at
				}
			}
		}""",
			"variables": {"data": permissions_data_list},
    }
