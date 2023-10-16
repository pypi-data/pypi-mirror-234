"""Helpers for interacting with the KnowBe4 API within the Sym SDK."""


from typing import List, Optional

from sym.sdk.exceptions import KnowBe4Error  # noqa
from sym.sdk.user import User


def get_training_enrollments_for_user(
    user: User, store_purchase_id: Optional[int] = None, campaign_id: Optional[int] = None
) -> List[dict]:
    """Gets all training enrollments for the given user, optionally filtered by ``store_purchase_id``
    and ``campaign_id``. Refer to the
    `KnowBe4 API docs <https://developer.knowbe4.com/rest/reporting#tag/Training/paths/~1v1~1training~1enrollments/get>`_
    for more details.

    Args:
        user: The :class:`~sym.sdk.user.User` whose training enrollments to retrieve.
        store_purchase_id: ID for store purchase by which to filter the training enrollments.
        campaign_id: ID for training campaign by which to filter the training enrollments.

    Returns:
        A list of all training enrollments.

    Raises:
        :class:`~sym.sdk.exceptions.knowbe4.KnowBe4Error`: If the KnowBe4 API responds with a 4xx or 5xx status code.
    """


def is_user_in_group(user: User, group_id: int) -> bool:
    """Whether the user exists in the group with the specified ``group_id``. Refer to the
    `API docs <https://developer.knowbe4.com/rest/reporting#tag/Users/paths/~1v1~1users~1%7Buser_id%7D/get>`_
    for more details.

    Returns:
        A boolean indicating if the user is in the group.

    Raises:
        :class:`~sym.sdk.exceptions.knowbe4.KnowBe4Error`: If no corresponding KnowBe4 user is found, or
            if the KnowBe4 API responds with a 4xx or 5xx status code.
    """
