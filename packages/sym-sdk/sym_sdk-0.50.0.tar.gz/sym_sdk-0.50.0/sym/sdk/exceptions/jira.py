from sym.sdk.exceptions.sym_exception import SymException


class JiraError(SymException):
    """This is the base class for all JiraErrors.

    Args:
        name: The name of the exception (used as the second part of the error code, e.g. MISSING_INSTALLATION)
        message: The exception message to display
    """

    def __init__(self, name: str, message: str):
        super().__init__(error_type="Jira", name=name, message=message)
