"""A parameterized instance of a :class:`~sym.sdk.templates.template.Template`."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict

from sym.sdk.resource import SymResource
from sym.sdk.user import User

if TYPE_CHECKING:
    from sym.sdk.event import Channel
    from sym.sdk.strategies.integration import Integration


class Environment(SymResource, ABC):
    """The :class:`~sym.sdk.flow.Environment` class represents a container
    that shares configuration values across :class:`~sym.sdk.flow.Flow` instances.

    Read more about `Environments <https://docs.symops.com/docs/tf-environment>`_.
    """

    @property
    @abstractmethod
    def integrations(self) -> Dict[str, "Integration"]:
        """A dictionary containing all :class:`Integrations <sym.sdk.strategies.integration.Integration>` that may be used in the implementation for a :class:`~sym.sdk.flow.Flow`, as defined in Terraform.


        For example, if Slack and AWS Lambda :class:`Integrations <sym.sdk.strategies.integration.Integration>` are specified in the :class:`~sym.sdk.flow.Environment`, the ``integrations`` dictionary would look like this::

            {
                "slack": <sym.sdk.strategies.integration.Integration>,
                "aws_lambda": <sym.sdk.strategies.integration.Integration>
            }

        """


class Flow(SymResource, ABC):
    """The :class:`~sym.sdk.flow.Flow` class contains a particular parameterization
    of a :class:`~sym.sdk.templates.template.Template`.

    Read more about `Flows <https://docs.symops.com/docs/tf-flow>`_.
    """

    @property
    @abstractmethod
    def fields(self) -> Dict[str, Any]:
        """A dictionary with the field structure defined for the :class:`~sym.sdk.flow.Flow`
        in Terraform.
        """

    @property
    @abstractmethod
    def vars(self) -> Dict[str, str]:
        """A dict containing user-supplied values from the :class:`~sym.sdk.flow.Flow`'s definition in Terraform.

        This dict might contain, for example, your team's PagerDuty schedule ID.
        """

    @property
    @abstractmethod
    def environment(self) -> Environment:
        """A reference to the :class:`~sym.sdk.flow.Environment` attached to this :class:`~sym.sdk.flow.Flow`."""


class Run(SymResource, ABC):
    """A :class:`~sym.sdk.flow.Run` represents an instance of a :class:`~sym.sdk.flow.Flow`
    in progress.

    For example, each new access request using the `sym:template:approval:1.0`
    :class:`~sym.sdk.templates.template.Template` would generate a new :class:`~sym.sdk.flow.Run`
    with data pertaining to that specific access request.
    """

    @property
    @abstractmethod
    def actors(self) -> Dict[str, User]:
        """A dict mapping :class:`~sym.sdk.event.Event` names to the :class:`~sym.sdk.user.User`
        that created each :class:`~sym.sdk.event.Event`. There will be one entry for each
        :class:`~sym.sdk.event.Event` in the current :class:`~sym.sdk.flow.Run`.

        For example, with a sym:approval :class:`~sym.sdk.flow.Flow`, after the "approve"
        :class:`~sym.sdk.event.Event` is received, the actors may look like this::

            {
                "prompt": <User A>,
                "request": <User A>,
                "approve": <User B>
            }
        """

    @property
    @abstractmethod
    def contexts(self) -> Dict[str, Dict[str, Any]]:
        """A dict mapping :class:`~sym.sdk.event.Event` names to the context attached to
        each :class:`~sym.sdk.event.Event`. There will be one entry for each
        :class:`~sym.sdk.event.Event` in the current :class:`~sym.sdk.flow.Run`.

        For example, with a sym:approval :class:`~sym.sdk.flow.Flow`, after the "approve"
        :class:`~sym.sdk.event.Event` is received, the contexts may look like this::

            {
                "request": {
                    "additional_id": "12345"
                }
            }
        """

    @property
    @abstractmethod
    def source_channel(self) -> "Channel":
        """A :class:`~sym.sdk.event.Channel` object, which contains information about the where
        the :class:`~sym.sdk.flow.Run`'s first :class:`~sym.sdk.event.Event` came from.
        """
