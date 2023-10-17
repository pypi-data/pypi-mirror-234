# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Using logger.info/debug/someOtherLevel() is not supported in this module. In order to get the correct
frame info, we must skip over functions called in this module and in vendored structlog. If logging is attempted,
incorrect frame info will be displayed on the log message if used in this file.

Use print(...) instead
"""
import asyncio
import sys
from os import getpid
from os.path import basename
import threading

import contrast
from contrast_vendor.structlog._frames import _find_first_app_frame_and_name
from contrast_vendor import structlog
from contrast.utils.configuration_utils import get_hostname

LOGGING_TO_BUNYAN_LOG_LEVEL_CONVERSION = {
    "critical": 60,
    "error": 50,
    "warning": 40,
    "info": 30,
    "debug": 20,
}


def add_hostname(logger, method_name, event_dict):
    event_dict["hostname"] = get_hostname()

    return event_dict


def add_pid(logger, method_name, event_dict):
    event_dict["pid"] = getpid()

    return event_dict


def add_thread_id(logger, method_name, event_dict):
    event_dict["thread_id"] = threading.get_ident()

    return event_dict


def add_request_id(logger, method_name, event_dict):
    context = contrast.CS__CONTEXT_TRACKER.current()
    obj_id = -1

    if context:
        obj_id = id(context)

    event_dict["request_id"] = obj_id

    return event_dict


def rename_key(old_name, new_name):
    def event_key_to_msg(logger, method_name, event_dict):
        """
        msg is a required key for bunyan parsing. The event key is renamed to msg
        """

        value = event_dict.get(old_name)
        if value and not event_dict.get(new_name):
            event_dict[new_name] = value
            del event_dict[old_name]

        return event_dict

    return event_key_to_msg


def add_bunyan_log_level(logger, log_level, event_dict):
    """
    This Processor must be installed AFTER structlog.stdlib.add_log_level.
    structlog.stdlib.add_log_level adds level: "info/debug/...". This function
    converts that string to the bunyan integer value equivalent (whenever possible).
    """
    if log_level == "warn":
        # The stdlib has an alias
        log_level = "warning"

    new_value = LOGGING_TO_BUNYAN_LOG_LEVEL_CONVERSION.get(log_level, None)

    if new_value:
        event_dict["level"] = new_value

    return event_dict


def add_v(logger, method_name, event_dict):
    """
    Required key for bunyan log parsing
    """
    event_dict["v"] = 0

    return event_dict


def add_frame_info(logger, method_name, event_dict):
    """
    Adds filename, function name and line number based on where the logger is called
    """
    ignore_frames = [
        "contrast_vendor.structlog",
        "contrast.utils.loggers.structlog",
        "logging",
    ]

    frame_info = _find_first_app_frame_and_name(ignore_frames)

    if frame_info and frame_info[0]:
        frame = frame_info[0]

        event_dict[
            "frame_info"
        ] = f"{basename(frame.f_code.co_filename)}:{frame.f_code.co_name}:{frame.f_lineno}"

    return event_dict


def add_progname(logger, method_name, event_dict):
    """
    progname is the name of the process the agents uses in logs.
    The default value is Contrast Agent. progname will be used
    as the name of the logger as seen in the logs.
    """
    field = "name"
    current_handler = logger.handlers[0]

    if hasattr(current_handler.filters[0], field):
        progname = current_handler.filters[0].progname

        if progname:
            event_dict[field] = progname

    return event_dict


def add_asyncio_info(logger, method_name, event_dict):
    try:
        current_task = asyncio.current_task()

        if sys.version_info[:2] > (3, 7):
            # get_name and get_coro are only supported on 3.8+

            # If no name has been explicitly assigned to the Task, the default asyncio Task implementation
            # generates a default name during instantiation.
            event_dict["asyncio_task_name"] = current_task.get_name()

            current_coro = current_task.get_coro()
            if hasattr(current_coro, "__name__"):
                event_dict["asyncio_coro_name"] = current_coro.__name__

        event_dict["asyncio_task_id"] = id(current_task)
    except Exception:
        # This can happen when there is no running event loop
        pass

    return event_dict


def init_structlog():
    """
    Configures structlog -- must be called AFTER logging module is configured
    """
    structlog.configure(
        # Each processor is called from the top down and can modify the event_dict passed to it
        processors=[
            add_bunyan_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            # rename_key must be called after timestamp is added by TimeStamper
            rename_key("timestamp", "time"),
            rename_key("event", "msg"),
            add_v,
            add_hostname,
            add_pid,
            add_thread_id,
            add_request_id,
            add_frame_info,
            add_progname,
            add_asyncio_info,
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
