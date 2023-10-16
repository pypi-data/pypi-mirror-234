"""Helpers for interacting with the OneLogin API within the Sym SDK."""
from typing import List, Optional

from sym.sdk.user import User


def list_roles(name_filter: Optional[str] = None) -> List[dict]:
    """Returns a list of all roles in the OneLogin account configured in the current
    :class:`~sym.sdk.flow.Environment`. Roles are represented as dictionaries, whose
    structure is defined by the OneLogin API.

    Details here: https://developers.onelogin.com/api-docs/2/roles/list-roles

    Note that if more than 650 roles exist in the OneLogin account, this call will
    fail. This is a limitation of the OneLogin API.

    Args:
        name_filter: If provided, only roles whose name contains the given string will
            be returned.

    Returns:
        A list of dictionaries representing OneLogin roles.
    """


def get_user_info(user: User) -> dict:
    """Get information about a OneLogin user.

    Refer to OneLogin's get-user API documentation for details on the response format:
    https://developers.onelogin.com/api-docs/2/users/get-user

    Args:
        user: The Sym :class:`~sym.sdk.user.User` to request OneLogin info for

    Returns:
        A dictionary of user information
    """


def users_in_role(role_id: int) -> List[User]:
    """Returns the members of the specified OneLogin role.

    The OneLogin role's ID must be given, and the function will check that the role
    exists and is accessible.

    Args:
        role_id: The ID of the OneLogin role.

    Returns:
        A list of :class:`Users <sym.sdk.user.User>` who are members of the given role.

    Raises:
        :class:`~sym.sdk.exceptions.sdk.MissingArgument`: If the role_id is not provided.
        :class:`~sym.sdk.exceptions.onelogin.OneLoginError`: If the role does not exist or is not accessible.
    """


def is_user_in_role(user: User, *, role_id: int) -> bool:
    """Checks if the provided :class:`~sym.sdk.user.User` is a member of the OneLogin role specified.

    The OneLogin role's ID must be given, and the function will check that the role
    exists and is accessible.

    Args:
        user: The :class:`~sym.sdk.user.User` to check role membership for.
        role_id: The ID of the OneLogin role.

    Returns:
        True if the user is a member of the specified OneLogin role, False otherwise.

    Raises:
        :class:`~sym.sdk.exceptions.sdk.MissingArgument`: If the role_id is not provided.
        :class:`~sym.sdk.exceptions.onelogin.OneLoginError`: If the role does not exist or is not accessible,
            or if no :class:`~sym.sdk.user.User` is provided.
    """
