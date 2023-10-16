"""Methods for invoking AWS Lambda functions."""

from typing import Any, Optional, Union

from sym.sdk.event import Event
from sym.sdk.exceptions.aws import AWSLambdaError  # noqa


def invoke(arn: str, payload: Optional[Union[Event, dict]] = None) -> Any:
    """Synchronously invokes an AWS Lambda function.

    Args:
        arn: The ARN of the Lambda function to invoke.
        payload: A dict of JSON-serializable data to pass to the function,
            or an :class:`~sym.sdk.event.Event` object.

    Returns:
        The JSON-deserialized object returned by the lambda.
    """


def invoke_async(arn: str, payload: Optional[Union[Event, dict]] = None) -> bool:
    """Asynchronously invokes an AWS Lambda function.

    Args:
        arn: The ARN of the Lambda function to invoke.
        payload: A dict of JSON-serializable data to pass to the function,
            or an :class:`~sym.sdk.event.Event` object.

    Returns:
        A boolean indicating success enqueuing the invocation.
    """
