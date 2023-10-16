"""
    This module contains the exceptions
"""

class RevaError(Exception):
    """
        This is the base reva exception
        from base exception
    """
    def __init__(
        self,
        message="",
        obj=None
        ):
        super().__init__(message)

        self._message = message
        self.obj = obj

    @property
    def message(self):
        """
            This function will form the error message
        """
        message = [self._message]
        return ' '.join(message)

    def __str__(self) -> str:
        return self.message


class FileNotExistsError(RevaError):
    """
        THis exception will be raised when file does not exists
    """
class ConfigNotFoundError(RevaError):
    """
        This exception will be raised when config not found
    """
class EnvPathNotConfigured(RevaError):
    """
        This exception will be raised when the environment path is not configured
    """

class UnsupportedPlatformError(RevaError):
    """
        This exception will be raised when the platform is not supported
    """
