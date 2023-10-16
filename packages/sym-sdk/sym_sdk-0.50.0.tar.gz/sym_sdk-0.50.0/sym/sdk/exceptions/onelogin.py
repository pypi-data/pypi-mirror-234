from sym.sdk.exceptions.sym_exception import SymException


class OneLoginError(SymException):
    """This is the base class for all ``OneLoginError``\ s.

    Args:
        name: The name of the exception (used as the second part of the error code, e.g. ``AUTH_FAILED``)
        message: The exception message to display
    """  # noqa: W605 (The "\ " is apparently the correct way to do this formatting in Sphinx/rST)

    def __init__(self, name: str, message: str, error_type: str = "OneLogin"):
        super().__init__(error_type=error_type, name=name, message=message)
