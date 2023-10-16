from typing import Callable, List

from sym.sdk.event import Event
from sym.sdk.field_option import FieldOption


def reducer(fn):
    """A decorator marking this method as a Reducer.

    Reducers take in an Event and return a single value.py

    Reducer names are always prefixed with ``get_``."""
    return fn


def hook(fn):
    """A decorator marking this method as a Hook.

    Hooks allow you to alter control flow by overriding default implementations of Template steps.
    Hook names may be prefixed with ``on_`` or ``after_``.

    If a Hook name is prefixed with ``on_``, it will be executed after the :class:`~sym.sdk.event.Event` is fired
    but before the default implementation.

    If a Hook name is prefixed with ``after_``, it will be executed after the default implementation.
    """
    return fn


def prefetch(field_name: str) -> Callable[[Event], List[FieldOption]]:
    """A decorator marking this method as a Prefetch Reducer.

    Prefetch Reducers allow you to retrieve a list of options for the Prompt Field identified by `field_name`.
    The logic will be executed prior to displaying the request form to users in Slack, such that the options
    are dynamically populated with the values returned by this Reducer.

    Note: Prefetch Reducers are time-sensitive! The request form will display "Loading..." until all Prefetch Reducers have been executed, so long-running Prefetch Reducers may result in performance delays.
    """
