# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import traceback
from functools import lru_cache

from contrast import (
    AGENT_CURR_WORKING_DIR,
    SORTED_SYS_PATH,
)
from contrast.api.trace_event import TraceStack
from contrast.utils.decorators import fail_quietly
from contrast.utils.library_reader.library_reader import (
    get_active_library_names_from_pkg,
)
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


APPLIES_MARKER = "cs__"
PATCH_MARKER = "__cs"
PY_FILE_EXTENSION = ".py"
UTILS_MODULES = "contrast/utils"
NONETYPE = "NoneType"

CONTRAST_EXTENSIONS = (
    "contrast_vendor",
    "contrast_rewriter",
    "contrast/assess_extensions",
    "contrast/patches",
)
DJANGO_EXCEPTION_PATH = "core/handlers/exception.py"
DJANGO_DEPRECATION_PATH = "utils/deprecation.py"
SITE_PACKAGES = "site-packages"


@fail_quietly("Failed to build stacktrace for event", return_value=[])
def build_stack():
    # PERF: only grab 30 elements to not use as much memory.
    # But the clean step will likely remove more elements.
    return traceback.extract_stack(limit=30)


@fail_quietly("Failed to clean stacktrace for event", return_value=[])
def clean_stack(frames, depth=20):
    frames.reverse()  # moves most recent to the front

    frames = [frame for frame in frames if acceptable_frame(frame)]

    return to_element_list(frames[:depth])


def acceptable_frame(frame):
    """
    Return true if frame does NOT contain contrast or __cs
    """
    ignore_string = "/contrast/"

    if isinstance(frame, tuple):
        return (
            ignore_string not in frame[0]
            and UTILS_MODULES not in frame[0]
            and not any(extension in frame[0] for extension in CONTRAST_EXTENSIONS)
            and not frame[2].startswith(APPLIES_MARKER)
            and not frame[2].startswith(PATCH_MARKER)
            and not frame[0].endswith(DJANGO_EXCEPTION_PATH)
            and not frame[0].endswith(DJANGO_DEPRECATION_PATH)
        )

    return (
        ignore_string not in frame.filename
        and UTILS_MODULES not in frame.filename
        and not any(extension in frame.filename for extension in CONTRAST_EXTENSIONS)
        and not frame.name.startswith(APPLIES_MARKER)
        and not frame.name.startswith(PATCH_MARKER)
        and not frame.filename.endswith(DJANGO_EXCEPTION_PATH)
        and not frame.filename.endswith(DJANGO_DEPRECATION_PATH)
    )


def build_and_clean_stack(depth=10):
    """
    Perform both build and clean steps.
    """
    frames = build_stack()
    return clean_stack(frames, depth=depth)


def to_element_list(frames):
    return [y for y in [to_element(x) for x in frames] if y is not None]


@fail_quietly("Failed to convert event")
def to_element(summary):
    if not summary:
        return None

    if isinstance(summary, tuple):
        # in python 2 traceback returns a tuple
        path = summary[0]
        method = summary[2]
        line_number = summary[1]
    else:
        # python 3 is a FrameSummary
        path = summary.filename
        method = summary.name
        line_number = summary.lineno

    element = TraceStack()
    element.line_number = line_number

    element.file_name = filename_formatter(path)
    element.declaring_class = element.file_name
    element.method_name = method

    return element


@fail_quietly("Unable to create file_name")
@lru_cache(maxsize=512)
def filename_formatter(file_name):
    # PERF: This method is called hundreds of times, so be mindful
    # of what additional computations are added. Small changes will have
    # significant performance impacts.

    if file_name.startswith("<frozen"):
        return file_name

    formatted = None

    if file_name.startswith(AGENT_CURR_WORKING_DIR):
        formatted = file_name.replace(AGENT_CURR_WORKING_DIR, "")
    else:
        for sys_path in SORTED_SYS_PATH:
            if file_name.startswith(sys_path):
                formatted = file_name.replace(sys_path, "")
                break

    formatted = formatted or file_name

    return formatted.replace("/", ".").lstrip(".")


def in_custom_code():
    current_stack_trace = build_and_clean_stack(depth=4)
    for trace in current_stack_trace:
        if trace:
            file_name = trace.file_name
            if file_name.endswith(".py") or file_name.endswith(".pyc"):
                file_name = file_name[:-3]
            if _is_custom_module(file_name):
                return True
    return False


def _is_custom_module(file_name):
    """

    Given a file name, determines if the file is a custom module.

    If a library name is in the file_name, we can say that the file is part of that library
    Obviously this can go wrong if users are naming their custom modules library names but hopefully import errors
    deter people away from this.

    ex:
    file_name = 'flask.router.Router'
    active_library_names = ['flask', 'wsgi', 'sqlalchemy', 'git']
    returns False

    file_name = 'core.utils.docker_constants'
    active_library_names = ['flask', 'wsgi', 'sqlalchemy', 'git']
    return True

    :param file_name: string of file_name without file type (contrast.utils.stack_trace_utils)
    :return: True if no active libraries are in the file_name else False
    """
    active_libraries_names = [
        # exclude vulnpy - a purposely-vulnerable library
        lib
        for lib in get_active_library_names_from_pkg()
        if lib != "vulnpy"
    ]
    for library_name in active_libraries_names:
        if file_name.startswith(library_name):
            return False
    return True
