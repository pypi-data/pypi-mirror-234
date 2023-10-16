from sym.sdk.exceptions.sym_exception import SymException


class SDKError(SymException):
    """Generic exceptions raised by the Sym SDK at runtime.

    Args:
        name: The name of the exception (used as the second part of the error_code, e.g. MISSING_ARGUMENT)
        message: The exception message to display
    """

    def __init__(self, name: str, message: str, error_type: str = "SymSDK"):
        super().__init__(error_type=error_type, name=name, message=message)


class MissingArgument(SDKError):
    """This error is raised when a Sym SDK method is called without the required arguments.

    Args:
        arg: The name of the missing argument
        method: The name of the SDk method that was called
    """

    def __init__(self, arg: str, method: str):
        super().__init__(
            name="MISSING_ARGUMENT",
            message=(
                f"Required argument '{arg}' for method '{method}' not provided. "
                "Please check your implementation file to ensure that all required arguments are passed."
            ),
        )
