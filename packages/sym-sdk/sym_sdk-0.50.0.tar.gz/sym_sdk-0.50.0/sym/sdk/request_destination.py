"""Representation of different options for routing Sym Requests."""

from typing import List, Optional

from pydantic import BaseModel, Field, validator


class RequestDestination(BaseModel):
    """A super-class for classes representing a Sym Request Destination."""

    allow_self: bool = False
    """A boolean indicating whether the requester may approve this Request."""

    timeout: Optional[int] = None
    """An optional integer representing the duration until this destination will time out, in seconds.
    If not specified, then the destination will never time out, i.e the Request will hang indefinitely until responded
    to.
    """


class SlackChannelID(RequestDestination):
    """A Request to be sent to a Slack Channel, identified by a Slack Channel ID, e.g. 'C12345'."""

    channel_id: str
    """A string that identifies a Slack Channel by its unique ID. e.g. 'C12345'."""

    @validator("channel_id")
    def validate_channel_id_format(cls, value):
        """Validates that the given `channel_id` follows Slack's convention of starting with a C, D or G.
        (e.g. 'D12345').
        """
        value = value.strip()

        if not value:
            raise ValueError("channel_id must be non-empty")

        if not value[0] in {"C", "D", "G"}:
            raise ValueError(
                f"{value} is not a valid Slack Channel ID. Channel IDs must start with one of 'C', 'D', or 'G'."
            )

        return value

    def __str__(self):
        """A method that will print a human readable explanation of the type of data,
        in this case a SlackChannelId with a string of the channel id."""
        return f"SlackChannelID '{self.channel_id}'"


class SlackChannelName(RequestDestination):
    """A Request to be sent to a Slack Channel, identified by a Slack Channel name."""

    channel_name: str
    """A string that identifies a Slack Channel by its unique name. (e.g. '#sym-errors')."""

    def __str__(self):
        """A method that will print a human readable explanation of the type of data,
        in this case a SlackChannelName with a string of the channel name."""
        return f"SlackChannelName '{self.channel_name}'"

    @validator("channel_name")
    def validate_channel_name_format(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("channel_name must be non-empty")

        return value


class SlackUser(RequestDestination):
    """A Request to be sent to a Slack User, identified by a Slack User ID."""

    user_id: str
    """A string that identifies a Slack User by their unique ID (also called Member ID). (e.g. 'U12345')."""

    @validator("user_id")
    def validate_user_id_format(cls, value):
        """Validates that the given `user_id` follows Slack's convention of starting with a U or W. (e.g. 'U12345')."""
        value = value.strip()

        if not value:
            raise ValueError("user_id must be non-empty")

        if not value[0] in {"U", "W"}:
            raise ValueError(
                f"{value} is not a valid Slack User ID. Slack User IDs must start with 'U' or 'W'."
            )

        return value

    def mention(self) -> str:
        """Returns a string that can be used to @mention this User in a Slack message."""
        return f"<@{self.user_id}>"

    def __str__(self):
        """Returns a human readable string indicating the type of data, in this case Slack User and the user_id"""
        return f"SlackUser '{self.user_id}'"


class SlackUserGroup(RequestDestination):
    """A Request to be sent in a Slack Group DM including the given Slack Users, with a maximum of 7 Users."""

    users: List[SlackUser] = Field(..., min_items=1, max_items=7)
    """A list of :class:`~sym.sdk.request_destination.SlackUser` objects to include in the group DM.
    Note: While each SlackUser object supports an `allow_self` attribute, this attribute will ignored in favor of the
    `allow_self` attribute set on the SlackUserGroup object.
    """

    def __str__(self):
        """Returns a human readable string indicating the type of data, in this case SlackUserGroup
        and the user IDs printed in a comma seperated list"""
        user_ids = [user.user_id for user in self.users]
        return f"SlackUserGroup '{user_ids}'"


class RequestDestinationFallback(BaseModel):
    """A list of :class:`~sym.sdk.request_destination.RequestDestination` to attempt to send requests to.
    The next :class:`~sym.sdk.request_destination.RequestDestination` will be attempted based on the failure mode
    configuration.
    """

    destinations: List[RequestDestination]
    """The list of :class:`~sym.sdk.request_destination.RequestDestination` objects to attempt to send requests to."""

    continue_on_delivery_failure: bool = True
    """If set to True, if Sym fails to deliver a Request to a :class:`~sym.sdk.request_destination.RequestDestination`
    (such as when the Slack Channel does not exist), then the next
    :class:`~sym.sdk.request_destination.RequestDestination` in the `destinations` list will be attempted."""

    continue_on_timeout: bool = False
    """If set to True, if the current Request times out, then a new Request will be sent to the next
    :class:`~sym.sdk.request_destination.RequestDestination` in the `destinations` list."""


class RequestForwardContext(BaseModel):
    """An object containing additional context about the current and next destinations of the Sym Request. An instance
    of this class is included as an argument when `on_request_forward` and `after_request_forward` hooks are invoked by
    the Sym Runtime.
    """

    all_request_destinations: List[RequestDestination]
    """A list of all :class:`~sym.sdk.request_destination.RequestDestination` instances that this Sym Request may be
    sent to"""
    current_destination_index: int
    """An integer representing the index of the current destination in `all_request_destinations`"""
    next_destination_index: Optional[int]
    """An integer representing the index of the next destination in `all_request_destinations`. When set to `None`,
    this means that the `current_destination_index` is at the last element of `all_request_destinations`, i.e there
    are no more destinations to try next.
    """
