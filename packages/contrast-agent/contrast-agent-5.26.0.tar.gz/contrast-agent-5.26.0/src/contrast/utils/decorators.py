# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from typing import Optional

import os
import logging as stdlib_logging

import contrast
from contrast_vendor import structlog as logging
from contrast.agent.validator import ValidationException

logger = logging.getLogger("contrast")

DEBUG_LEVEL = stdlib_logging.DEBUG


def _log_extra_safely(
    log_message: Optional[str],
    error: Exception,
    original_func,
    args,
    kwargs,
    log_level="debug",
):
    if not contrast.telemetry_disabled():
        TELEMETRY = contrast.TELEMETRY
    else:
        TELEMETRY = None

    try:
        full_msg = (
            (log_message or "Exception in Contrast machinery") + ": " + str(error)
        )
        getattr(logger, log_level)(full_msg, exc_info=error)
        logger.debug("wrapped function args: %s", args)
        logger.debug("wrapped function kwargs: %s", kwargs)

        if TELEMETRY is not None:
            TELEMETRY.report_error(
                error=error, original_func=original_func, message=full_msg
            )
    except ValidationException as val_ex:
        logger.debug(f"Cannot report error to Telemetry: {str(val_ex)}")
    except Exception:
        # For complete safety, we're not going to try to log the logging error
        # because sometimes the logging error is actually an error (such as a recursive
        # error) within the logging module itself!
        pass


def fail_loudly(log_message=None, log_level="exception", return_value=None):
    """
    Decorator that will run the decorated function/method and, if
    an exception is raised, return a safe value and log the error.

    Note that SecurityException will always be re-raised.

    :param log_message: message to log in case of failure
    :param log_level: level to log in case of failure
    :param return_value: safe value to return in case of failure
    :return: original func return or return_value
    """

    def wrap(original_func):
        def run_safely(*args, **kwargs):
            try:
                return original_func(*args, **kwargs)
            except contrast.SecurityException:
                raise
            except Exception as ex:
                _log_extra_safely(
                    log_message, ex, original_func, args, kwargs, log_level
                )
                if os.environ.get("CONTRAST_TESTING"):
                    logger.warn(
                        "Re-raising exception in fail_loudly (CONTRAST_TESTING is set)"
                    )
                    raise

            return return_value

        return run_safely

    return wrap


def fail_quietly(log_message=None, return_value=None):
    """
    Similar to fail_loudly (see above)

    This decorator is intended to handle cases where an exception may occur but won't
    disrupt normal operation of the agent. This decorator should be used to protect
    against external exceptions we can't prevent but still want to handle.

    In these cases, we log an error message and the exception traceback, both at DEBUG
    level.
    """

    def wrap(original_func):
        def run_safely(*args, **kwargs):
            try:
                return original_func(*args, **kwargs)
            except contrast.SecurityException:
                raise
            except Exception as ex:
                _log_extra_safely(log_message, ex, original_func, args, kwargs)
                if os.environ.get("CONTRAST_TESTING"):
                    logger.warn(
                        "Re-raising exception in fail_quietly (CONTRAST_TESTING is set)"
                    )
                    raise
            return return_value

        return run_safely

    return wrap


class cached_property(object):
    """
    https://github.com/pydanny/cached-property
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self

        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value
