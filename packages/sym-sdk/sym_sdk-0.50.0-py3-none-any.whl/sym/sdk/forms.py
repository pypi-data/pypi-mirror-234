"""Models for working with Sym access request forms."""

from enum import Enum
from typing import Any, Dict, List, Optional, OrderedDict

from pydantic import BaseModel, Field, validator


class FieldType(str, Enum):
    """Allowed data types for :class:`~sym.sdk.forms.PromptField` objects."""

    STRING = "string"
    """Basic text data."""

    INT = "int"
    """Basic integer data."""

    BOOL = "bool"
    """Basic "True" or "False" data."""

    DURATION = "duration"
    """A length of time in seconds."""

    SLACK_USER = "slack_user"
    """A Slack User ID."""

    SLACK_USER_LIST = "slack_user_list"
    """A list of Slack User IDs."""

    STR_LIST = "str_list"
    """A list of strings."""

    INT_LIST = "int_list"
    """A list of integers."""


class FieldOption(BaseModel):
    """An option to display in a drop-down menu.
    FieldOptions represent value-label pairs to use in drop-down menus. They may be returned by
    Prefetch Reducers to dynamically generate a list of options for Prompt Fields with
    `prefetch = true`.

    They are also used in :class:`~sym.sdk.forms.PromptField` objects to represent the selected
    drop-down value as well as the list of selectable options for that field.
    """

    value: Any
    """The actual value to pass through when selected.

    When cast to a string, this value's length cannot exceed 55 characters.
    """

    label: str = Field(max_length=55)
    """A short label, no more than 55 characters, to display in the drop-down menu.

    This label will be used to filter the options to display when a requester types into an input box.
    """

    @validator("value")
    def validate_value_length(cls, value):
        """Validates that the given value will not exceed Slack-imposed length limits."""

        if value is None:
            raise ValueError("value must be non-empty")

        if len(str(value)) > 55:
            raise ValueError(f"{value} exceeds the max length of 55 characters.")

        return value


class SlackUserSelection(BaseModel):
    """A representation of a Slack user who has been selected in a Slack user drop-down menu
    (i.e. a Sym prompt_field with a type of "slack_user" or "slack_user_list").
    """

    class Config:
        validate_assignment = True

    user_id: str = Field(allow_mutation=False)
    """The Slack ID of the Slack user who was selected."""

    username: Optional[str] = Field(allow_mutation=False)
    """The Sym username (i.e. email or bot username) of the user who was selected.

    If the selected Slack user is not already a known Sym user in your organization, this attribute will return None.
    """


class PromptField(BaseModel):
    """The current state of a prompt_field Terraform block representing an input field
    for a form used to make a Sym access request.

    See `the Terraform registry <https://registry.terraform.io/providers/symopsio/sym/latest/docs/resources/flow#nestedblock--params--prompt_field>`_
    for more information about how these are defined on a :class:`~sym.sdk.flow.Flow`.
    """

    class Config:
        validate_assignment = True

    name: str = Field(allow_mutation=False)
    """A unique identifier for this field."""

    type: FieldType = Field(allow_mutation=False)
    """The type of data this field will accept."""

    value: Any = None
    """The current input value for this field."""

    label: Optional[str] = None
    """A display name for this field, to be displayed in the UI."""

    required: bool = True
    """Whether this field is a required input.

    Required inputs are only enforced if `visible = True`.
    """

    current_allowed_values: List[FieldOption] = []
    """The current list of :class:`~sym.sdk.forms.FieldOption` objects to be displayed in a drop-down menu."""

    original_allowed_values: List[FieldOption] = Field(allow_mutation=False, default=[])
    """The full list of :class:`~sym.sdk.forms.FieldOption` objects either defined in Terraform or
    returned by this field's Prefetch Reducer.
    """

    visible: bool = True
    """Whether this field should be displayed in the UI."""


class SymPromptForm(BaseModel):
    """The current state of a form used to submit an access request to Sym."""

    fields: OrderedDict[str, PromptField]
    """A dictionary of :class:`~sym.sdk.forms.PromptField` objects, keyed by field name
    and in the order they would be displayed in the UI.

    NOTE: While the :class:`~sym.sdk.forms.PromptField` objects may be modified to change the
    form's state, the dictionary itself should not be modified.
    """

    flow_vars: Dict[str, str] = {}
    """A dictionary of Flow vars and their string values, as defined in the
    `sym_flow Terraform resource's vars attribute <https://registry.terraform.io/providers/symopsio/sym/latest/docs/resources/flow#vars>`__.
    """
