# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.api import Route
from contrast.agent import agent_state
from contrast.agent.middlewares.route_coverage.common import build_key

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class RoutesMixin(object):
    """
    Class for route coverage work.
    Route coverage is assess only.
    """

    def handle_routes(self, context, request):
        """
        Method that should run for all middlewares immediately after the application
        executes.
        """
        if context and request:
            self.get_routes_on_first_request()
            self.check_for_new_routes(context, request)
            self.append_route_to_findings(context)

    def get_routes_on_first_request(self):
        """
        Attempt to do route discovery on the first request
        """

        # if we already have routes here, we must have populated them from a framework-
        # specific patch. Eventually, `get_routes_on_first_request` will be completely
        # removed, once all frameworks perform route discovery using patches.
        if not agent_state.is_first_request():
            logger.debug("skipping route discovery - not the first request")
            return
        if agent_state.get_routes():
            logger.debug("skipping route discovery - already populated")
            return

        logger.debug("First request so looking for app routes.")

        discovered_routes = self.get_route_coverage()

        if not discovered_routes or not isinstance(discovered_routes, dict):
            logger.debug("Could not find any routes")
            return

        routes = agent_state.get_routes()
        routes.update(discovered_routes)

        routes_to_log = [f"{route.verb}: {route.url}" for route in routes.values()]
        logger.debug("Found the following routes: %s", routes_to_log)

    def check_for_new_routes(self, context, request):
        """
        Check to see if the current request is a new route. If so, add this to the list
        of all discovered routes.
        """
        logger.debug("Checking for new route.")

        if context.view_func is None:
            context.view_func = self.get_view_func(request)
            if context.view_func is None:
                logger.debug(
                    "unable to determine view function for the current request"
                )
                return
        else:
            logger.debug("already have the view function for this request")

        request_method = request.method
        route_id = build_key(str(id(context.view_func)), request_method)

        self.update_route_information(context, route_id, request_method)

    def update_route_information(self, context, route_id, request_method):
        """
        Given a context and route_id, check if the route_id is in middleware (self)
        routes. Store the route as current and observed route for later use.

        :param context: RequestContext instance
        :param route_id: string id for a route
        :param request_method: string such as 'GET'
        :return: no return, side effects only
        """
        routes = agent_state.get_routes()
        if route_id not in routes:
            url = context.request.get_normalized_uri()

            if context.view_func_str is None:
                context.view_func_str = self.build_route(context.view_func, url)

            routes[route_id] = Route(
                verb=request_method, url=url, route=context.view_func_str
            )

        route = routes[route_id]
        logger.debug("Route visited: %s : %s", route.verb, route.url)

        context.current_route = route

        # Currently we do not report an observed route if the route signature is empty.
        # As a team we've decided there isn't a meaningful default signature value
        # we can provide to customers. If a route doesn't show up in Contrast UI,
        # it may be due to its missing signature. In this scenario, we will have to work
        # with the customer directly to understand why the signature was not created.
        if not route.signature:
            logger.debug(
                "No route signature found for %s : %s (id=%s). Not updating observed"
                " route",
                route.verb,
                route.url,
                route_id,
            )
            return

        context.observed_route.signature = route.signature

        context.observed_route.url = route.url
        context.observed_route.verb = route.verb

    def append_route_to_findings(self, context):
        """
        Route discovery and current route is not identified until the handle ensure
        part of the request lifecycle, after assess has analyzed and potentially created
        a finding, so that is why we have to append the now-available current route to
        the existing finding.
        """
        if not context.current_route:
            logger.debug("No current route to append to findings")
            return

        if not context.findings:
            logger.debug("No findings to append route to")
            return

        for finding in context.findings:
            if not finding.routes:
                logger.debug(
                    "Appending route %s:%s to %s",
                    context.current_route.verb,
                    context.current_route.url,
                    finding.rule_id,
                )
                finding.routes.append(context.current_route)

            finding.set_version()

    def get_view_func(self, request):
        return

    def build_route(self, view_func, url):
        return ""
