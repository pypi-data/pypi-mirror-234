from sym.sdk.exceptions.sym_exception import SymException


class OktaError(SymException):
    """This is the base class for all OktaErrors.

    Args:
        name: The name of the exception (used as the second part of the error code, e.g. GROUP_NOT_FOUND)
        message: The exception message to display
    """

    def __init__(self, name: str, message: str, error_type: str = "Okta"):
        super().__init__(error_type=error_type, name=name, message=message)
