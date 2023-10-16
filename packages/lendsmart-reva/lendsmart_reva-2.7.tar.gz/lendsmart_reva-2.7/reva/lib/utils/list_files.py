"""
    This module will list the files
"""

def list_json_files(update_obj):
    """
        list the files
    """
    list_of_files = update_obj.get_json_paths_to_update()
    for file_path in list_of_files:
        print(file_path)
