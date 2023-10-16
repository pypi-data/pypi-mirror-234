"""
    namespace
"""

def get_namespace(namespace):
    """
        get namespace
    """
    return {
        "query": '''query get_namespace($object_meta: jsonb!) {
        namespaces(where: {object_meta: {_contains: $object_meta}}) {
            id
            object_meta
            metadata
        }
        }''',
        "variables": {"object_meta": {"name": namespace}}

    }