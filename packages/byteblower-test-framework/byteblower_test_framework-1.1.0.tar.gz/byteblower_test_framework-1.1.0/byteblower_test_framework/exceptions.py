"""Module related to exceptions and handling of them."""
import logging
from functools import wraps
from typing import Callable  # for type hinting

from byteblowerll.byteblower import ByteBlowerAPIException

__all__ = (
    'log_api_error',
    'ByteBlowerTestFrameworkException',
    'NotDurationBased',
    'InfiniteDuration',
)


class ByteBlowerTestFrameworkException(Exception):
    """Base exception for all ByteBlower Test Framework related exceptions."""


class NotDurationBased(ByteBlowerTestFrameworkException):
    """Raised when a flow is not duration based."""


class InfiniteDuration(ByteBlowerTestFrameworkException):
    """Raised when a flow duration is not specified."""


class InvalidInput(ByteBlowerTestFrameworkException):
    """Raised when an invalid input is provided."""

class ConflictingInput(InvalidInput):
    """Raised when conflicting input is provided."""

class IncompatibleHttpServer(ByteBlowerTestFrameworkException):
    """Raised when an invalid HTTP server is found."""

    def __init__(self) -> None:
        super().__init__('Incompatible existing HTTP server found')


def log_api_error(func: Callable) -> Callable:
    """Decorate method or function to logs ByteBlower API errors.

    Any exception will be (re-)raised.

    :param func: Function to decorate
    :type func: Callable
    :return: Decorated function
    :rtype: Callable
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ByteBlowerAPIException as e:
            logging.error("API error: %s", e.getMessage())
            raise

    return wrapper
