"""
    This module will filter the data with id
"""
from ramda import path_or

def filter_data_with_id(datas: list):
    """
        THis function will get input data as list
        and filter the data with id and remove the data without id
    """
    if isinstance(datas, dict):
        datas = [datas]
    result = []
    for data in datas:
        if path_or("",["id"], data):
            result.append(data)
    return result
