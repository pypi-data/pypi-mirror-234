# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Rules for coverage:

- new routes on init get count 0
- new routes after init get count 1 per context
- routes without a method type specified on init are ['GET', 'POST']
- a route needs verb, route, url, and count
- url should be normalized uri
- route should be the path to the view function (aka controller for Java people)
- one method type per route

Example:
      GET /blog/foo/bar - app.blogs.find(request, ) 0
"""

import re


DEFAULT_ROUTE_METHODS = ("GET", "POST")


# A format template for constructing "path-component" regexps, ie between "/"-s in a URI
# This is used to build regexps for uri normalization
# We use a look-ahead to ensure correctness for back-to-back path components
_RE_PATH_COMPONENT_FORMAT = r"(^|/){regex}(?=(/|$))"

# examples:
# /123
# 123/
# 123
# /123/
# 123/123
RE_DIGITS_PATH_COMPONENT = _RE_PATH_COMPONENT_FORMAT.format(regex=r"\d+")

# example:
# /fd4b78312634a236d11da0f9c32526e5b8261afa
RE_HASH_PATH_COMPONENT = _RE_PATH_COMPONENT_FORMAT.format(
    regex=r"([a-fA-F0-9]{2}){16,}"
)

# example:
# /b09112a0-a58f-487a-ab4b-3608bd64fb3f/
RE_UUID_PATH_COMPONENT = _RE_PATH_COMPONENT_FORMAT.format(
    regex=r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}"
)

# Returns digits between '/' or end of string
FIND_REQEUST_PARAMS = r"(?<=\/)\d+(?=\/|$)"


def get_normalized_uri(path):
    """
    A best-effort to remove client-specific information from the path.

    Example:
    /user/123456/page/12 -> /user/{n}/page/{n}
    """
    result = path

    result = re.sub(RE_DIGITS_PATH_COMPONENT, r"\1{n}", result)
    result = re.sub(RE_HASH_PATH_COMPONENT, r"\1{hash}", result)
    result = re.sub(RE_UUID_PATH_COMPONENT, r"\1{uuid}", result)

    return result


def get_url_parameters(path):
    """
    A best-effort to remove client-specific information from the path.

    Example:
    /user/123456/page/12 -> /user/{n}/page/{n}
    """
    return re.findall(FIND_REQEUST_PARAMS, path)


def build_route(view_func_name, view_func):
    view_func_args = build_args_from_function(view_func)
    return view_func_name + view_func_args


def build_key(route_id, method):
    return "_".join([route_id, method])


def build_args_from_function(func):
    """
    Attempts to grab argument names from the function definition.

    Defaults to () if none exist
    If there is no view function, like in the case of a pure WSGI app, then the func will
    be a string like '/sqli' and we just return that.

    """
    method_arg_names = "()"
    if func is not None and hasattr(func, "__code__"):
        method_arg_names = str(
            func.__code__.co_varnames[0 : func.__code__.co_argcount]
        ).replace("'", "")
    elif isinstance(func, str):
        method_arg_names = func

    return method_arg_names
