# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

import argparse
import os
import sys
import shutil

from contrast import __file__
from contrast.configuration import AgentConfig
from contrast_rewriter import ENABLE_REWRITER, REWRITE_FOR_PYTEST
from contrast_vendor import structlog as logging

USING_RUNNER_ENV_VAR = "__CONTRAST_USING_RUNNER"

logger = logging.getLogger("contrast")

DESCRIPTION = """
The command-line runner for the Contrast Python Agent.
"""

USAGE = "%(prog)s [-h] -- cmd [cmd ...]"

EPILOG = """
Insert this command before the one you usually use to start your webserver
to apply Contrast's instrumentation. See our public documentation for details:
https://docs.contrastsecurity.com/en/python.html
"""


def runner() -> None:
    logger.info("Starting Contrast Agent runner pre-process")
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        usage=USAGE,
        epilog=EPILOG,
    )
    parser.add_argument(
        "--rewrite-for-pytest", action="store_true", help=argparse.SUPPRESS
    )
    # if you add public arguments here, update USAGE accordingly
    parser.add_argument("cmd", nargs="+")

    parsed = parser.parse_args()

    config = AgentConfig()

    loader_path = os.path.join(os.path.dirname(__file__), "loader")
    os.environ["PYTHONPATH"] = os.path.pathsep.join([loader_path] + sys.path)
    os.environ[USING_RUNNER_ENV_VAR] = "true"

    if parsed.rewrite_for_pytest:
        os.environ[REWRITE_FOR_PYTEST] = "true"
    elif config.should_rewrite:
        os.environ[ENABLE_REWRITER] = "true"

    os.execl(shutil.which(parsed.cmd[0]), *parsed.cmd)
