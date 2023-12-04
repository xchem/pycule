"""Decorators for Mcule API."""
from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from typing import Optional, Callable
from functools import wraps, partial
from ratelimit import limits, sleep_and_retry

from .callbacks import default_on_success

LOGGER = logging.getLogger("mcule:decorators")

# Get this from a .yaml file?
ENAMINE_MAXIMUM_REQUESTS_PER_MINUTE = 100
ENAMINE_MAXIMUM_REQUESTS_PER_DAY = 1000
MCULE_MAXIMUM_REQUESTS_PER_MINUTE = 100
MCULE_MAXIMUM_REQUESTS_PER_DAY = 1000


class RequestsPerMinuteExceeded(RuntimeError):
    """Exception raised when too many requests are sent in a minute."""

    pass


class RequestTimeoutNotElapsed(RuntimeError):
    """Exception raised when the timeout between requests has not elapsed."""

    pass


def enamine_api_limits(function: Callable) -> Callable:
    """
    Decorator to handle the limits in the Enamine API.
    Args:
        function (Callable): function to decorate.
    Raises:
        RequestsPerMinuteExceeded: too many requests in a minute.
        RequestTimeoutNotElapsed: consecutive requests too close in time.
    Returns:
        Callable: a function wrapped with the decorator.
    """

    @sleep_and_retry
    @limits(calls=ENAMINE_MAXIMUM_REQUESTS_PER_DAY, period=86400)
    def _check_too_many_requests():
        return

    @sleep_and_retry
    @limits(calls=ENAMINE_MAXIMUM_REQUESTS_PER_MINUTE, period=60)
    def _check_too_frequent_requests():
        return

    @wraps(function)
    def _wrapper(*args, **kwargs):
        _check_too_many_requests()
        _check_too_frequent_requests()
        result = function(*args, **kwargs)
        return result

    return _wrapper


def mcule_api_limits(function: Callable) -> Callable:
    """
    Decorator to handle the limits in the MCule API.
    Args:
        function (Callable): function to decorate.
    Raises:
        RequestsPerMinuteExceeded: too many requests in a minute.
        RequestTimeoutNotElapsed: consecutive requests too close in time.
    Returns:
        Callable: a function wrapped with the decorator.
    """

    @sleep_and_retry
    @limits(calls=MCULE_MAXIMUM_REQUESTS_PER_DAY, period=86400)
    def _check_too_many_requests():
        return

    @sleep_and_retry
    @limits(calls=MCULE_MAXIMUM_REQUESTS_PER_MINUTE, period=60)
    def _check_too_frequent_requests():
        return

    @wraps(function)
    def _wrapper(*args, **kwargs):
        _check_too_many_requests()
        _check_too_frequent_requests()
        result = function(*args, **kwargs)
        return result

    return _wrapper


def response_handling(
    function: Optional[Callable] = None,
    success_status_code: int = 200,
    on_success: Callable = default_on_success,
) -> Callable:
    """
    Decorator to handle request responses.
    Args:
        function (Callable, optional): function to decorate.
        success_status_code (int): status expected on success.
        on_success (Callable): function to call on success.
    Returns:
        Callable: a function wrapped with the decorator.
    """
    if function is None:
        return partial(
            response_handling,
            success_status_code=success_status_code,
            on_success=on_success,
        )

    @wraps(function)
    def _wrapper(*args, **kwargs):

        response = function(*args, **kwargs)

        if response.status_code == success_status_code:
            return on_success(response)
        elif response.status_code == 400:
            LOGGER.error("Bad request - probably a validation error")
            LOGGER.debug(response.text)
        elif response.status_code == 401:
            LOGGER.error("Unauthorised - check your API key")
            LOGGER.debug(response.text)
        elif response.status_code == 403:
            LOGGER.error("Permission denied")
            LOGGER.debug(response.text)
        elif response.status_code == 404:
            LOGGER.error("Not found")
            LOGGER.debug(response.text)
        elif response.status_code == 429:
            LOGGER.error("Too many requests made")
            LOGGER.debug(response.text)
        elif response.status_code == 500:
            LOGGER.error("Server error")
            LOGGER.debug(response.text)
        return {"response": response}

    return _wrapper
