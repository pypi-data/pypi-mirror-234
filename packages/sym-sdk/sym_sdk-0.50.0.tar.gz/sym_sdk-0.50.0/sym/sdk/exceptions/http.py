from sym.sdk.exceptions.sym_exception import SymException


class HTTPError(SymException):
    """This is the base class for all HTTPErrors.

    Args:
        name: The name of the exception (used as the second part of the error code, e.g. ERROR_RESPONSE)
        message: The exception message to display
    """

    def __init__(self, name: str, message: str, error_type: str = "HTTP"):
        super().__init__(error_type=error_type, name=name, message=message)
