from sym.sdk.exceptions.sym_exception import SymException


class KnowBe4Error(SymException):
    """This is the base class for all KnowBe4Errors.

    Args:
        name: The name of the exception (used as the second part of the error code, e.g. USER_NOT_FOUND)
        message: The exception message to display
    """

    def __init__(self, name: str, message: str):
        super().__init__(error_type="KnowBe4", name=name, message=message)
