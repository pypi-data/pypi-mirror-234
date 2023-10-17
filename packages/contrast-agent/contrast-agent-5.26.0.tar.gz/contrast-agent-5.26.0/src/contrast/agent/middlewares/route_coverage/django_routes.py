# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import ast
import textwrap
import functools

from collections import deque
from copy import copy
from importlib import import_module
from types import FunctionType, MethodType
from inspect import isclass, getsource
from django.urls.exceptions import Resolver404

from django.utils.regex_helper import normalize

try:
    from django.urls import get_resolver
except ImportError:
    from django.core.urlresolvers import get_resolver

from contrast.agent.middlewares.route_coverage.common import (
    DEFAULT_ROUTE_METHODS,
    build_args_from_function,
    build_key,
)
from contrast.api import Route
from contrast.agent.settings import Settings
from functools import lru_cache

from contrast_vendor import structlog as logging
from contrast.utils.decorators import fail_quietly

logger = logging.getLogger("contrast")


@lru_cache(maxsize=1)
def is_django_1():
    settings = Settings(framework_name="django")
    return settings.framework.version.major == "1"


def check_for_http_decorator(func):
    """
    Grabs the require_http_methods decorator from a view function call via inspect

    NOTE: this only works for require_http_methods; it does not currently work for require_GET,
    require_POST, require_safe
    """
    method_types = {}

    if isinstance(func, functools.partial):
        func = getattr(func, "func", None)

    if func is None:
        return method_types

    def visit_function_def(node):
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                # decorator name which should be require_http_methods
                if getattr(decorator.func, "id", "") == "require_http_methods":
                    name = (
                        decorator.func.attr
                        if isinstance(decorator.func, ast.Attribute)
                        else decorator.func.id
                    )
                    method_list = decorator.args[0] if len(decorator.args) > 0 else []
                    method_str_list = list(
                        filter(
                            None,
                            [
                                getattr(s, "s", "")  # py37: change "s" to "value"
                                for s in getattr(method_list, "elts", [])
                            ],
                        )
                    )
                    if not method_str_list:
                        continue
                    method_types[name] = method_str_list
                    return

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_function_def
    node_source = textwrap.dedent(getsource(func))
    node_iter.visit(ast.parse(node_source))

    return method_types


def get_lowest_function_call(func):
    if isclass(func) or func.__closure__ is None:
        return func
    closure = (c.cell_contents for c in func.__closure__)
    return next((c for c in closure if isinstance(c, (FunctionType, MethodType))), None)


def create_url(pattern_or_resolver):
    if is_django_1():
        pattern = pattern_or_resolver.regex.pattern
    else:
        pattern = pattern_or_resolver.pattern.regex.pattern

    try:
        normalized = normalize(pattern)[0][0]
        url = normalized.replace("%(", "{").replace(")", "}")
    except Exception:
        url = pattern_or_resolver.name

    return url


def get_method_info(pattern_or_resolver):
    method_types = []
    method_arg_names = "()"

    lowest_function = get_lowest_function_call(pattern_or_resolver.callback)

    if lowest_function is not None:
        method_arg_names = build_args_from_function(lowest_function)

        # this method returns a dict because it uses one to store state in the recursive function
        method_types_dict = check_for_http_decorator(lowest_function)
        method_types = method_types_dict.get("require_http_methods", [])

        if not isinstance(method_types, list):
            method_types = [method_types]

    return method_types or DEFAULT_ROUTE_METHODS, method_arg_names


def create_one_route(routes, method_type, method_arg_names, pattern_or_resolver):
    """
    Create a new api.Route object and adds it to routes dict

    :param routes: dict of routes
    :param method_type:
    :param method_arg_names:
    :param pattern_or_resolver:
    :return: None, adds to routes dict which is updated through pass-by-reference
    """
    route = build_django_route(pattern_or_resolver, method_arg_names)

    route_id = str(id(pattern_or_resolver.callback))

    key = build_key(route_id, method_type)

    routes[key] = Route(
        verb=method_type, url=create_url(pattern_or_resolver), route=route
    )


def create_routes(urlpatterns):
    if is_django_1():
        try:
            # Django 1.10 and above
            from django.urls.resolvers import RegexURLPattern, RegexURLResolver
        except ImportError:
            # Django 1.9 and below
            from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
    else:
        from django.urls.resolvers import (
            URLPattern as RegexURLPattern,
            URLResolver as RegexURLResolver,
        )

    routes = {}

    urlpatterns_deque = deque(urlpatterns)

    while urlpatterns_deque:
        url_pattern = urlpatterns_deque.popleft()

        if isinstance(url_pattern, RegexURLResolver):
            urlpatterns_deque.extend(url_pattern.url_patterns)

        elif isinstance(url_pattern, RegexURLPattern):
            method_types, method_arg_names = get_method_info(url_pattern)
            for method_type in method_types:
                create_one_route(routes, method_type, method_arg_names, url_pattern)
    return routes


def create_django_routes():
    """
    Grabs all URL's from the root settings and searches for possible required_method decorators

    In Django there is no implicit declaration of GET or POST. Often times decorators are used to fix this.

    Returns a dict of key = id, value = api.Route.
    """

    from django.conf import settings

    if not settings.ROOT_URLCONF:
        logger.info("Application does not define settings.ROOT_URLCONF")
        logger.debug("Skipping enumeration of urlpatterns")
        return None

    try:
        root_urlconf = import_module(settings.ROOT_URLCONF)
    except Exception as exception:
        logger.debug("Failed to import ROOT_URLCONF: %s", exception)
        return None

    try:
        urlpatterns = root_urlconf.urlpatterns or []
    except Exception as exception:
        logger.debug("Failed to get urlpatterns: %s", exception)
        return None

    url_patterns = copy(urlpatterns)
    return create_routes(url_patterns)


def _function_loc(func):
    """Return the function's module and name"""
    return f"{func.__module__}.{func.__name__}"


def build_django_route(obj, method_arg_names=None):
    if hasattr(obj, "lookup_str"):
        route = obj.lookup_str
    elif hasattr(obj, "callback"):
        cb = obj.callback
        route = _function_loc(cb)
    elif callable(obj):
        route = _function_loc(obj)
    else:
        logger.debug("WARNING: can't build django route for object type %s", type(obj))
        return ""

    if method_arg_names is None:
        method_arg_names = build_args_from_function(obj)

    route += method_arg_names
    return route


@fail_quietly("Failed to get view function for django application")
def get_view_func(path):
    from django.conf import settings

    try:
        result = get_resolver().resolve(path or "/")
    except Resolver404:
        return None

    if (
        result is None
        and not path.endswith("/")
        and "django.middleware.common.CommonMiddleware" in settings.MIDDLEWARE
        and settings.APPEND_SLASH
    ):
        result = get_view_func(f"{path}/")
    if result is None:
        return None

    return result.func


class DjangoRoutesMixin:
    @fail_quietly("Unable to get route coverage", return_value={})
    def get_route_coverage(self):
        """
        Route Coverage is the Assess feature that looks for routes generally defined
        in Django apps in a file like urls.py
        """
        return create_django_routes()

    @fail_quietly("Unable to get Django view func")
    def get_view_func(self, request):
        return get_view_func(self.request_path)

    @fail_quietly("Unable to build route", return_value="")
    def build_route(self, view_func, url):
        return build_django_route(view_func)
