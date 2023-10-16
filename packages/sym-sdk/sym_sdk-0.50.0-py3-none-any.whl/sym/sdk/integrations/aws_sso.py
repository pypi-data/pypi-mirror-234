"""Helpers for interacting with the AWS SSO API within the Sym SDK."""
from typing import List, Optional

from sym.sdk.exceptions.aws import AWSSSOError  # noqa
from sym.sdk.user import User


def is_user_in_group(user: User, *, group_name: str) -> bool:
    """Checks if the provided :class:`~sym.sdk.user.User` is a member of the AWS SSO group specified.

    The AWS SSO group's display name must be given, and the method will check that the group exists and is
    accessible. An exception will be raised if not.

    Args:
        user: The :class:`~sym.sdk.user.User` to check group membership of.
        group_name: The display name of the AWS SSO group.

    Returns:
        True if the :class:`~sym.sdk.user.User` is a member of the specified AWS SSO group, False otherwise.

    Raises:
        :class:`~sym.sdk.exceptions.aws.AWSSSOError`: If no AWS SSO group with the given name exists.
    """


def list_groups() -> List[dict]:
    """Lists all the groups in the identity store of the AWS SSO account connected by an AWS SSO Sym Integration.
    See `here <https://docs.symops.com/docs/aws-sso-access#add-a-aws-sso-integration>`__ for instructions on how
    to create an AWS SSO Integration.

    Returns:
        A list of dictionaries, with each dictionary representing a Group in AWS SSO's Group structure.
        See `here <https://docs.aws.amazon.com/singlesignon/latest/IdentityStoreAPIReference/API_Group.html>`__
        for details.
    """


def users_in_group(group_name: str) -> List[User]:
    """Get all users from the specified AWS SSO group.

    *Warning: This method may only be used for groups that have 20 or fewer members.*

    The AWS SSO group's display name must be given, and the method will check that the group exists and is
    accessible. An exception will be raised if not.

    Args:
        group_name: The display name of the AWS SSO group.

    Returns:
        A list of :class:`~sym.sdk.user.User`

    Raises:
        :class:`~sym.sdk.exceptions.aws.AWSSSOError`: If no AWS SSO group with the given name exists or if the group has greater than 20 members.
    """


def list_accounts(organizational_unit_id: Optional[str] = None) -> List[dict]:
    """Returns a list of AWS accounts within the AWS SSO Organization that the AWS SSO Sym Integration is connected to,
    optionally filtered to the specified Organizational Unit.

    The behavior of this function changes based on whether the ``organizational_unit_id`` parameter is specified, and if
    so what value is provided.

    - If unspecified or set to ``None``, this function will return all AWS accounts within your Organization.
    - If a parent root ID (beginning with ``r-``) is specified, this function will return all AWS accounts *not* mapped
      to any Organizational Unit.
    - If an Organizational Unit ID (any other value) is specified, this function will return all AWS accounts mapped to
      that Organizational Unit *only*; accounts in child OUs of the specified OU will *not* be included.

    Args:
        organizational_unit_id: The ID of the parent root or Organizational Unit to filter by, or ``None`` to include
            all AWS accounts.

    Returns:
        A list of dictionaries, with each dictionary representing an AWS account. The dictionaries follow the AWS
        Account object structure; see
        `here <https://docs.aws.amazon.com/organizations/latest/APIReference/API_Account.html>`__ for details.

    Raises:
        :class:`~sym.sdk.exceptions.aws.AWSSSOError`: If the specified ``organizational_unit_id`` is invalid or does
            not exist, if and only if ``organizational_unit_id`` is specified.
    """
