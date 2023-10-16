"""Helpers for interacting with a Slack workspace."""

from typing import Optional, Sequence, Union

from sym.sdk.exceptions.slack import SlackError  # noqa
from sym.sdk.request_destination import (
    RequestDestination,
    RequestDestinationFallback,
    SlackChannelID,
    SlackChannelName,
    SlackUser,
    SlackUserGroup,
)
from sym.sdk.user import User


def user(
    identifier: Union[str, User], allow_self: bool = False, timeout: Optional[int] = None
) -> SlackUser:
    """A reference to a Slack user.

    Args:
        identifier: The unique Slack user ID, email, or @mention for a Slack user, or a Sym :class:`~sym.sdk.user.User`
            instance. (e.g. "U12345", "jane\@symops.io", "@Jane Austen").
        allow_self: A boolean indicating whether the requester may approve this Request.
        timeout: An integer representing the number of seconds for the request to remain active for this user. After
            timeout elapses, the request message will expire and can no longer be interacted with.
    """  # noqa: W605 (The "\@" is the correct way avoid implicit mailto links in Sphinx/rST)


def mention(identifier: Union[str, User]) -> str:
    """Returns a string that mentions a Slack user given their identifier.

    Users can be specified with a Slack user ID, email,
    a string version of an @mention. (e.g. "U12345", "jane\@symops.io", "@Jane Austen", or a
    Sym :class:`~sym.sdk.user.User` instance).
    """  # noqa: W605 (The "\@" is the correct way avoid implicit mailto links in Sphinx/rST)


def channel(
    name: str, allow_self: bool = False, timeout: Optional[int] = None
) -> Union[SlackChannelID, SlackChannelName]:
    """A reference to a Slack channel.

    Args:
        name: The unique channel name or channel ID. (e.g. '#sym-requests' or 'C12345').
        allow_self: A boolean indicating whether the requester may approve this Request.
        timeout: An integer representing the number of seconds for the request to remain active for this user. After
            timeout elapses, the request message will expire and can no longer be interacted with.
    """


def group(
    users: Sequence[Union[str, User]], allow_self: bool = False, timeout: Optional[int] = None
) -> SlackUserGroup:
    """A reference to a Slack group DM.

    Args:
        users: A list of Slack Users to include in the group. Users can be specified with a Slack user ID, email,
            a string version of an @mention. (e.g. "U12345", "jane\@symops.io", "@Jane Austen", or a
            Sym :class:`~sym.sdk.user.User` instance).
        timeout: An integer representing the number of seconds for the request to remain active for this user. After
            timeout elapses, the request message will expire and can no longer be interacted with.
    """  # noqa: W605 (The "\@" is the correct way avoid implicit mailto links in Sphinx/rST)


def fallback(
    *destinations: RequestDestination,
    continue_on_delivery_failure: Optional[bool] = True,
    continue_on_timeout: Optional[bool] = False,
) -> RequestDestinationFallback:
    """Returns a :class:`~sym.sdk.request_destination.RequestDestinationFallback` that contains the specified
    :class:`~sym.sdk.request_destination.RequestDestination` objects, with `continue_on_delivery_failure=True`.

    If used as the return value of a `get_approvers` reducer, when a Sym Request is made,
    each :class:`~sym.sdk.request_destination.RequestDestination` will be attempted in sequence until one succeeds.

    For example::

        def get_approvers(event):
            return slack.fallback(slack.channel("#missing"), slack.user("@david"))

    Args:
        destinations: At least 2 :class:`~sym.sdk.request_destination.RequestDestination` objects.
        continue_on_delivery_failure: A boolean representing whether to deliver to the next destination if a failure
            occurs while delivering to the current destination.
        continue_on_timeout: A boolean representing whether to deliver to the next destination if the Request at the
            current destination times out.
    """


def send_message(destination: Union[User, RequestDestination], message: str) -> None:
    """Sends a simple message to a destination in Slack. Accepts either a :class:`~sym.sdk.user.User`
    or a :class:`~sym.sdk.request_destination.RequestDestination`, which may represent a user, group, or channel
    in Slack.

    For example::

        # To send to #general:
        slack.send_message(slack.channel("#general"), "Hello, world!")

        # To DM a specific user:
        slack.send_message(slack.user("me@symops.io"), "It works!")

        # To DM the user who triggered an event:
        slack.send_message(event.user, "You did a thing!")

    Args:
        destination: Where the message should go.
        message: The text contents of the message to send.
    """


def get_user_info(user: User) -> dict:
    """Get information about a Slack user.

    Refer to Slack's users.info API documentation for the details on the response format:
    https://api.slack.com/methods/users.info

    Args:
        user: A Sym :class:`~sym.sdk.user.User` instance to get info about.
    """


def list_users(active_only: bool = True) -> list:
    """Returns a list of all users in the workspace.

    Refer to Slack's users.info API documentation for the details on the response format:
    https://api.slack.com/methods/users.list

    Args:
        active_only: A boolean indicating whether to exclude deactivated and deleted users.
    """


def is_user_in_group(user: User, *, group_id: str) -> bool:
    """Check if the provided :class:`~sym.sdk.user.User` is a member of the Slack user group specified.

    Login to Slack via web and retrieve the Slack user group ID in the left menu bar: `More` -> `People & user groups`
    -> `User groups` and select your user group. You can see the Slack user group ID in the URL:
    ``https://app.slack.com/client/{workspaceID}/browse-user-groups/user_groups/{usergroupID}``.

    If you have installed the Sym app before Aug 22nd 2023, then you may need to reinstall the Sym app to use this
    feature. Refer to the `main docs <https://docs.symops.com/docs/slack-app-integration#reinstall-slack-app>`_ for more details.

    Args:
        user: The :class:`~sym.sdk.user.User` to check group membership of.
        group_id: The ID of the Slack user group in which to search for the user.
    """
