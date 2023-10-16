"""
    This module will contain the exception class
"""

class RevaError(Exception):
    """
        This is the base lendsmart exception
        from base exception
    """
    def __init__(self, message=""):
        super().__init__(message)
        self._message = message

    @property
    def message(self):
        """
            This function will form the error message
        """
        message = [self._message]
        return ' '.join(message)

    def __str__(self) -> str:
        return self.message
