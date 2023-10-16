"""Helpers for interacting with the Okta API within the Sym SDK."""


from typing import List, Optional

from sym.sdk.exceptions import OktaError  # noqa
from sym.sdk.user import User


def is_user_in_group(user: User, *, group_id: str) -> bool:
    """Checks if the provided user is a member of the Okta group specified.

    The Okta group's ID must be given, and the method will check that the group exists and is
    accessible. An exception will be thrown if not.

    Args:
        user: The user to check group membership of.
        group_id: The ID of the Okta group.

    Returns:
        True if the user is a member of the specified Okta group, False otherwise.
    """


def users_in_group(*, group_id: str) -> List[User]:
    """Get all users from the specified Okta group.

    The Okta group's ID must be given, and the method will check that the group exists and is
    accessible. An exception will be thrown if not.

    Args:
        group_id: The ID of the Okta group.
    """


def get_user_info(user: User) -> dict:
    """Returns Okta User Info for the Sym user.

    The user info follows the data format of Okta's Users API, details here:
    https://developer.okta.com/docs/reference/api/users/#response-example-10

    Args:
        user: The Sym user to request Okta info for

    Returns:
        A dict of user info
    """


def list_groups(
    *,
    name_filter: Optional[str] = None,
    filter: Optional[str] = None,
    expand: Optional[List[str]] = None,
    only_native_groups: bool = True,
) -> List[dict]:
    """Returns a list of Okta Group Info.

    The arguments match the arguments in Okta's List Groups API,
    details `here <https://developer.okta.com/docs/reference/api/groups/#request-parameters-3>`__

    Args:
        name_filter: Finds a group whose name starts with ``name_filter``, case-insensitive.
        filter: A filter expression for groups. See `here <https://developer.okta.com/docs/reference/core-okta-api/#filter>`__
                for syntax and details.
                Note: The expressions for filter queries must use double quotes:

                .. code-block:: python

                    filter='id eq "00g12345"'
        expand: If specified, additional metadata will be included in the response.
                Possible values are: ``stats`` and/or ``app``.
        only_native_groups: If true, only groups of source type "Native Okta" (i.e. the only group source type modifiable by Sym)
                will be included in the results. See
                `here <https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-group-types.htm>`__
                for more information on Okta group source types.

    Returns:
        A list of dictionaries, with each dictionary representing a Group in Okta's
        Group structure. See
        `here <https://developer.okta.com/docs/reference/api/groups/#group-attributes>`__
        for details.
    """
