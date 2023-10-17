# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.api import Route
from contrast.agent.middlewares.route_coverage.common import (
    build_route,
    DEFAULT_ROUTE_METHODS,
    get_normalized_uri,
    build_key,
)


def create_routes(app):
    """
    Returns all the routes registered to an app as a dict
    :param app: {Quart or Flask} app
    :return: dict {route_id:  api.Route}
    """
    routes = {}

    for rule in list(app.url_map.iter_rules()):
        view_func = app.view_functions[rule.endpoint]

        route = build_route(rule.endpoint, view_func)

        route_id = str(id(view_func))

        methods = rule.methods or DEFAULT_ROUTE_METHODS

        for method_type in methods:
            key = build_key(route_id, method_type)
            routes[key] = Route(
                verb=method_type,
                url=get_normalized_uri(str(rule)),
                route=route,
            )

    return routes


def get_view_func_for_request(request, app):
    """
    Find the view function for the current request in the app.
    :param request: current request
    :param app: {Quart or Flask} app
    :return: function
    """
    from werkzeug.exceptions import NotFound, MethodNotAllowed

    adapter = app.url_map.bind("empty")

    if None in (request, adapter):
        return None

    try:
        match = adapter.match(request.path, method=request.method)
    except (NotFound, MethodNotAllowed):
        match = None

    func = None
    if match is not None:
        func = app.view_functions[match[0]]

    return func
