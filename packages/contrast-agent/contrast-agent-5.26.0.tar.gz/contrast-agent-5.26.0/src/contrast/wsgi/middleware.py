# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import functools
from contrast_vendor.webob import Request

import contrast
from contrast.agent import agent_state, scope
from contrast.agent.policy.trigger_node import TriggerNode
from contrast.agent.middlewares.base_middleware import BaseMiddleware
from contrast.agent.middlewares.environ_tracker import track_environ_sources
from contrast.utils.decorators import cached_property, fail_quietly
from contrast.utils.safe_import import safe_import_list
from contrast.utils.assess.duck_utils import safe_getattr_list

from contrast_vendor import structlog as logging
from contrast.utils import Profiler

logger = logging.getLogger("contrast")
DEFAULT_WSGI_NAME = "wsgi_app"


@functools.lru_cache(maxsize=1)
def _get_flask_types():
    return tuple(safe_import_list("flask.Flask"))


class WSGIMiddleware(BaseMiddleware):
    """
    Contrast middleware; PEP-333(3) WSGI-compliant
    """

    @scope.with_contrast_scope
    def __init__(
        self, wsgi_app, app_name=None, original_app=None, orig_pyramid_registry=None
    ):
        # We need to keep the `original_app` `orig_pyramid_registry` kwarg for now to prevent a breaking API
        # change
        del original_app
        del orig_pyramid_registry

        # TODO: PYT-2852 Revisit application name detection
        self.app_name = (
            app_name
            if app_name is not None
            else safe_getattr_list(
                wsgi_app,
                [
                    "__name__",
                    "name",
                ],
                DEFAULT_WSGI_NAME,
            )
        )

        super().__init__()

        if not agent_state.in_automatic_middleware() and isinstance(
            wsgi_app, _get_flask_types()
        ):
            # we need this to prevent a breaking API change when wrapping Flask apps
            wsgi_app = wsgi_app.wsgi_app

        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        if contrast.CS__CONTEXT_TRACKER.current():
            # This can happen if a single app is wrapped by multiple instances of the
            # middleware (usually caused by automatic instrumentation)
            logger.debug("Detected preexisting request context")
            return self.wsgi_app(environ, start_response)

        self.request_path = environ.get("PATH_INFO", "")

        with Profiler(self.request_path):
            context = self.should_analyze_request(environ)
            if context:
                with contrast.CS__CONTEXT_TRACKER.lifespan(context):
                    return self.call_with_agent(context, environ, start_response)

            return self.call_without_agent(environ, start_response)

    def call_with_agent(self, context, environ, start_response):
        self.log_start_request_analysis()

        track_environ_sources("wsgi", context, environ)

        try:
            self.prefilter()

            response = Request(environ).get_response(self.wsgi_app)

            context.extract_response_to_context(response)

            self.postfilter(context)
            self.check_for_blocked(context)
            self.swap_environ_path(environ)  # should not be moved to finally

            return response(environ, start_response)

        finally:
            self.handle_ensure(context, context.request)
            self.log_end_request_analysis()
            if self.settings.is_assess_enabled():
                contrast.STRING_TRACKER.ageoff()

    def swap_environ_path(self, environ):
        """
        See PYT-1742.

        Special behavior required for bottle+django to account for an unfortunate
        encoding behavior.

        In bottle, it occurs here:
        bottle.py:
        def _handle(self, environ):
            ...
            environ['PATH_INFO'] = path.encode('latin1').decode('utf8')
            ...

        This casing occurs after the application code is called, and will result in a
        `UnicodeEncodeError` when the agent attempts to access request.path.
        As a workaround, we store the original PATH_INFO - before bottle changed it
        during calling app code - and use it for agent purposes.
        """
        environ["PATH_INFO"] = self.request_path

    def call_without_agent(self, environ, start_response):
        """
        Normal without middleware call
        """
        super().call_without_agent()
        with scope.contrast_scope():
            return self.wsgi_app(environ, start_response)

    def get_route_coverage(self):
        """
        Unlike frameworks, WSGI is a spec, so it does not have a way to register routes.
        As such, there is no way to discover routes. Instead, routes will be added as
        they are visited via check for new routes.

        :return: empty dict
        """
        return {}

    @cached_property
    def trigger_node(self):
        """
        WSGI-specific trigger node used by reflected xss postfilter rule

        The rule itself is implemented in the base middleware but we need to
        provide a WSGI-specific trigger node for reporting purposes.
        """
        method_name = self.app_name

        module, class_name, args, instance_method = self._process_trigger_handler(
            self.wsgi_app
        )

        return (
            TriggerNode(module, class_name, instance_method, method_name, "RETURN"),
            args,
        )

    @fail_quietly("Unable to get WSGI view func")
    def get_view_func(self, _):
        """
        While most frameworks define view functions, WSGI doesn't so we will rely
        on the path information for reporting.
        If there is no path information, return an empty string

        :param request: RequestContext instance
        :return: string of path information for this request
        """
        return self.request_path or None

    @fail_quietly("Unable to build route", return_value="")
    def build_route(self, view_func, url):
        return url.replace("/", "")

    @cached_property
    def name(self):
        return "wsgi"
