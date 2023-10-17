# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys
import logging

import contrast
from contrast.assess_extensions import cs_str
from contrast.utils.loggers.structlog import init_structlog
from contrast.utils.configuration_utils import get_hostname
from contrast.utils.namespace import Namespace
from contrast.configuration import ConfigOptionSrc, CONTRAST_UI_SRC

from contrast_vendor import structlog

from . import (
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_PATH,
    DEFAULT_PROGNAME,
    LOGGER_NAME,
    SECURITY_LOGGER_NAME,
)

STDOUT = "STDOUT"
STDERR = "STDERR"


class module(Namespace):
    initialized: bool = False


def setup_basic_agent_logger(level=logging.INFO):
    """
    Setup a logger without any user-supplied configuration, with defaults:
        1. log to stdout
        2. log in INFO level
        3. with default progname

    The logger created here is expected to be overridden with config values
    provided later on in the middleware creation cycle.

    Note regarding init lock:
        Previously we discussed having a lock as part of logger init but since setup_basic_agent_logger is only
        called when the module is loaded (i.e during module import + executed) it should be safe not to explicitly
        have one due to the locking mechanisms used in the import machinery.
    """
    if not module.initialized:
        logger = logging.getLogger(LOGGER_NAME)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        _set_handler(logger, "STDOUT", DEFAULT_PROGNAME)
        logger.setLevel(level)

        init_structlog()
        module.initialized = True

    return structlog.getLogger(LOGGER_NAME)


def setup_agent_logger(config):
    """
    Initialize the agent logger with configurations.
    :param config: instance of AgentConfig or dict
    :return: None
    """
    config = config if config else {}
    # the or handles the case of empty string
    path = config.get("agent.logger.path", DEFAULT_LOG_PATH) or DEFAULT_LOG_PATH
    level = (
        config.get("agent.logger.level", DEFAULT_LOG_LEVEL).upper() or DEFAULT_LOG_LEVEL
    )

    logger = logging.getLogger(LOGGER_NAME)

    _set_logger_info(logger, config, path, level)
    _lock_logger(logger, config)

    cs_str.initialize_logger(structlog.getLogger(LOGGER_NAME))


def setup_security_logger(cfg):
    config = cfg if cfg else {}

    if not config.get("protect.enable", None):
        return

    path = config.get("agent.security_logger.path")
    level = config.get("agent.security_logger.level").upper()

    logger = logging.getLogger(SECURITY_LOGGER_NAME)

    _set_level(logger, level)

    handler = _get_handler(path)
    logger.addHandler(handler)

    fmt = (
        f"%(asctime)s {get_hostname()} CEF:0|Contrast Security|Contrast Agent Python|{contrast.__version__}|"
        "SECURITY|%(message)s|%(level)s|'pri=%(rule_id)s' 'src=%(source_ip)s' 'spt=%(source_port)s' "
        "'request=%(request_url)s' 'requestMethod=%(request_method)s' 'app=%(application)s' "
        "'outcome=%(outcome)s'"
    )

    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)


def security_log_msg(msg, app_name, rule_name, outcome):
    context = contrast.CS__CONTEXT_TRACKER.current()
    ip = port = url = method_name = "-"

    logger = logging.getLogger(SECURITY_LOGGER_NAME)

    if context is not None:
        ip = context.request.client_addr or "-"
        port = context.request.host_port
        method_name = context.request.method
        url = context.request.path

    log_context = dict(
        level=logger.level,
        rule_id=rule_name,
        source_ip=ip,
        source_port=port,
        request_url=url,
        request_method=method_name,
        application=app_name,
        outcome=outcome,
    )

    logger.warning(msg, extra=log_context)


def reset_agent_logger(log_path, log_level, config):
    """
    Reset agent logger path and/or level after the logger has already been created.

    Note that this function will return early if the lock_ attributes are not set,
    as this is what we set when we initialize the logger.

    Also note that progname is never reset so we use the one already set to the logger.

    :return: Bool if any logger value is reset
    """
    logger = logging.getLogger(LOGGER_NAME)

    if not hasattr(logger, "lock_path") or not hasattr(logger, "lock_level"):
        structlog.getLogger(LOGGER_NAME).debug(
            "Will not reset agent logger without set lock_attr values."
        )
        return False

    is_reset = False

    if not logger.lock_path and log_path:
        current_handler = logger.handlers[0]
        progname = current_handler.filters[0].progname
        _set_handler(logger, log_path, progname)
        # print so it shows up in STDOUT
        print(f"Contrast Agent Logger updated path to {log_path}")
        is_reset = True

        if config is not None:
            config.put(
                "agent.logger.path",
                log_path,
                src=ConfigOptionSrc(
                    name="contrast.agent.logger.path", source=CONTRAST_UI_SRC
                ),
            )

    if not logger.lock_level and log_level:
        # Avoid circular import
        from contrast.agent.agent_lib import update_log_options

        _set_level(logger, log_level)

        # print so it shows up in STDOUT
        print(f"Contrast Agent Logger updated level to {log_level}")

        if update_log_options(log_level):
            print(f"Contrast Agent Lib Logger updated level to {log_level}")

        is_reset = True

        if config is not None:
            config.put(
                "agent.logger.level",
                log_level,
                src=ConfigOptionSrc(
                    name="contrast.agent.logger.level", source=CONTRAST_UI_SRC
                ),
            )

    return is_reset


def _set_logger_info(logger, config, path, level):
    progname = config.get("agent.logger.progname", DEFAULT_PROGNAME)

    _set_handler(logger, path, progname)
    _set_level(logger, level)


def _set_handler(logger, path, progname):
    """
    A logger's handler is what determines where the log records will be printed to
    and what format they will have.

    To reset a handler, we delete the existing handlers and create a new one.

    CONTRAST-39746 defined the datetime format as ISO_8601. The one here is
    without ms as the logger doesn't natively support both ms and time zone at this time.
    """
    handler = _get_handler(path)
    program_filter = AgentFilter(progname=progname)
    handler.addFilter(program_filter)

    # empty all handlers so there is only one logging handler with this config
    logger.handlers = []
    logger.addHandler(handler)


def _get_handler(path):
    if path == STDOUT:
        handler = logging.StreamHandler(sys.stdout)
    elif path == STDERR:
        handler = logging.StreamHandler(sys.stderr)
    else:
        try:
            handler = logging.FileHandler(path)
        except Exception as e:
            print(e)
            # path could be '' or None
            handler = logging.StreamHandler()

    return handler


def _set_level(logger, level: str) -> None:
    if level.upper() == "TRACE":
        level = "DEBUG"
        print("Contrast Python Agent: TRACE logging is equivalent to DEBUG")
    try:
        logger.setLevel(level)
    except ValueError:
        # this fails validation if the level is an invalid value
        logger.setLevel(DEFAULT_LOG_LEVEL)


def _lock_logger(logger, config):
    """
    Determine if to lock the logger by looking at if the config had specified values
    for path and level.

    Locking the logger means its path and/or level cannot be changed later on by
    TS server feature values.
    """
    _lock_logger_attr(logger, "path", config)
    _lock_logger_attr(logger, "level", config)


def _lock_logger_attr(logger, logger_attr, config):
    """
    Assign a lock_{logger_attr} attribute to the logger.
    logger.logger_attr will be True if the user provided a legitimate string,
    but will be False if the attr value is '' or None.
    """
    attr_value = config.get(f"agent.logger.{logger_attr}")
    setattr(logger, f"lock_{logger_attr}", bool(attr_value))


class AgentFilter(logging.Filter):
    def __init__(self, progname=None):
        self.progname = progname
        super().__init__()

    def filter(self, record):
        record.progname = self.progname
        return super().filter(record)
