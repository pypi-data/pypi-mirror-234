"""Helpers for interacting with the Boundary API within the Sym SDK."""


from typing import List, Optional

from sym.sdk.exceptions import BoundaryError  # noqa


def list_groups(
    scope_id: str = "global", filter: Optional[str] = None, recursive: bool = False
) -> List[dict]:
    """
    Returns a list of Boundary groups.

    Args:
        scope_id: The scope ID used to access users defined in that scope and potentially sub-scopes.
        filter: A string containing certain criteria to filter the groups.
            See `Filtering <https://developer.hashicorp.com/boundary/docs/concepts/filtering>`_ for details.
            To access nested JSON-values, create a path with `/`.
            For example, a selector for group["scope"]["id"] would be "/item/scope/id".

            Other valid filters:
                - '"/item/member_ids" is not empty'
                - '"/item/name" == "Group Name"'
                - '"/item/scope/id" == "o_12345"'

        recursive: A boolean indicating whether to list groups defined in all the sub-scopes.

    Returns:
        A list of groups where each group is a dictionary. See
        `Group Service <https://developer.hashicorp.com/boundary/api-docs/group-service>`_ for details.

    Raises:
        :class:`~sym.sdk.exceptions.boundary.BoundaryError`: If the credentials configured in the Boundary integration
            do not have permissions to list groups in any scope.
    """


def get_group(group_id: str) -> dict:
    """
    Returns the Boundary group with the given group ID.

    Args:
        group_id: The group ID of the group to fetch.

    Returns:
        The group with the given group ID in the form of a dictionary. See
        `Group Service <https://developer.hashicorp.com/boundary/api-docs/group-service>`_ for details.

    Raises:
        :class:`~sym.sdk.exceptions.boundary.BoundaryError`: If no Boundary group with the given group_id exists, or
            the credentials configured in the Boundary integration do not have permissions to get the given group.
    """
