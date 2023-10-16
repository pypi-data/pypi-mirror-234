"""
    Contains the error classes
"""
from reva.lib.base.errors import RevaError

class RolesUpdateError(RevaError):
    """
        Error class for roles update
    """

class RolesDeleteError(RevaError):
    """
        Error class for roles delete
    """

class PermissionsUpdateError(RevaError):
    """
        Error class for permissions update
    """

class PermissionsDeleteError(RevaError):
    """
        Error class for roles delete
    """
