"""Helpers for interacting with the AWS IAM API within the Sym SDK."""

from sym.sdk.exceptions.aws import AWSIAMError  # noqa
from sym.sdk.user import User


def is_user_in_group(user: User, *, group_name: str) -> bool:
    """Checks if the provided user is a member of the AWS IAM group specified.

    The unique AWS IAM group name must be given, and the method will check that the group exists and is
    accessible. An exception will be thrown if not.

    Args:
        user: The user to check group membership of.
        group_name: The name of the AWS IAM group.

    Returns:
        True if the user is a member of the specified AWS IAM group, False otherwise.
    """
