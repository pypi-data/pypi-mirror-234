"""
    This module will convert the address
"""
from ramda import path_or

def address_to_json(address):
    """
    sample address '1101 Sylvan Avenue, Modesto, CA, USA'
    """

    _split_addresses = address.split(",")
    return {
        "street": path_or("",[0], _split_addresses),
        "city": path_or("",[1], _split_addresses),
        "state": path_or("",[2], _split_addresses),
        "country": path_or("",[3], _split_addresses),
        "zip_code": path_or("",[4], _split_addresses),
    }
