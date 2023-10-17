# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.api import Route
from contrast.agent.middlewares.route_coverage.common import (
    DEFAULT_ROUTE_METHODS,
    get_normalized_uri,
    build_key,
)
from contrast.agent.middlewares.route_coverage.common import build_route

DEFAULT_ROUTE_METHODS = DEFAULT_ROUTE_METHODS + ("HEAD",)


def create_starlette_routes(starlette_router):
    """
    Returns all the routes registered to a Starlette router as a dict.
    :param starlette_app: Starlette router instance (starlette.routing.Router)
    :return: dict {route_id:  api.Route}
    """
    from starlette.routing import Mount

    routes = {}

    for app_route in starlette_router.routes:
        if isinstance(app_route, Mount):
            mnt_routes = create_starlette_routes(app_route)
            routes.update(mnt_routes)
            continue

        view_func = app_route.endpoint

        route = build_route(app_route.name, view_func)
        route_id = str(id(view_func))
        methods = app_route.methods or DEFAULT_ROUTE_METHODS

        for method_type in methods:
            key = build_key(route_id, method_type)
            routes[key] = Route(
                verb=method_type,
                url=get_normalized_uri(str(app_route.name)),
                route=route,
            )

    return routes
