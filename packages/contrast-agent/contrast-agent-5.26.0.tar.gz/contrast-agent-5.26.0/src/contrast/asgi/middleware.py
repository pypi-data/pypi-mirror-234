# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import functools

import contrast
from contrast.agent import agent_state, scope as scope_
from contrast.agent.policy.trigger_node import TriggerNode
from contrast.agent.middlewares.base_middleware import BaseMiddleware
from contrast.agent.asgi import (
    track_scope_sources,
    ASGIRequest,
    ASGIResponse,
)
from contrast.utils.decorators import cached_property
from contrast.utils.safe_import import safe_import_list
from contrast.utils.assess.duck_utils import safe_getattr_list

from contrast.utils import Profiler
from contrast_vendor import structlog as logging


logger = logging.getLogger("contrast")

DEFAULT_ASGI_NAME = "asgi_app"


@functools.lru_cache(maxsize=1)
def _get_quart_types():
    return tuple(safe_import_list("quart.Quart"))


class ASGIMiddleware(BaseMiddleware):
    @scope_.with_contrast_scope
    def __init__(self, app, app_name=None, original_app=None):
        """
        Contrast middleware - ASGI 3.0

        The `app` argument here must be named "app" exactly to support FastAPI's
        middleware system, which uses the kwarg when calling this method.

        We need to keep the `original_app` kwarg for now to prevent a breaking API
        change.
        """
        del original_app

        # TODO: PYT-2852 Revisit application name detection
        self.app_name = (
            app_name
            if app_name is not None
            else safe_getattr_list(
                app,
                [
                    "__name__",
                    "name",
                    "title",
                ],
                DEFAULT_ASGI_NAME,
            )
        )

        super().__init__()

        if not agent_state.in_automatic_middleware() and isinstance(
            app, _get_quart_types()
        ):
            # we need this to prevent a breaking API change when wrapping Quart apps
            app = app.asgi_app

        self.asgi_app = app

    async def __call__(self, scope, receive, send) -> None:
        if contrast.CS__CONTEXT_TRACKER.current():
            # This can happen if a single app is wrapped by multiple instances of the
            # middleware (usually caused by automatic instrumentation)
            logger.debug("Detected preexisting request context")
            await self.asgi_app(scope, receive, send)
            return

        if scope.get("type") != "http":
            await self.call_without_agent_async(scope, receive, send)
        else:
            self.request_path = scope.get("path", "")
            with Profiler(self.request_path):
                request = ASGIRequest(scope, receive)
                environ = await request.to_wsgi_environ()

                context = self.should_analyze_request(environ)
                if context:
                    with contrast.CS__CONTEXT_TRACKER.lifespan(context):
                        await self.call_with_agent(context, request, send)
                        return

                await self.call_without_agent_async(scope, receive, send)

    async def call_with_agent(self, context, request, send) -> None:
        self.log_start_request_analysis()
        track_scope_sources(context, request.scope)

        try:
            self.prefilter()

            response = ASGIResponse(send)
            await self.asgi_app(
                request.scope, request.contrast__receive, response.contrast__send
            )

            context.extract_response_to_context(response)

            self.postfilter(context)
            self.check_for_blocked(context)

            await response.call_send()

        finally:
            self.handle_ensure(context, context.request)
            self.log_end_request_analysis()
            if self.settings.is_assess_enabled():
                contrast.STRING_TRACKER.ageoff()

    async def call_without_agent_async(self, scope, receive, send) -> None:
        super().call_without_agent()
        with scope_.contrast_scope():
            await self.asgi_app(scope, receive, send)

    @cached_property
    def trigger_node(self):
        """
        trigger node used by reflected xss postfilter rule
        """
        method_name = self.app_name

        module, class_name, args, instance_method = self._process_trigger_handler(
            self.asgi_app
        )

        return (
            TriggerNode(module, class_name, instance_method, method_name, "RETURN"),
            args,
        )

    @cached_property
    def name(self):
        return "asgi"

    def get_route_coverage(self):
        """
        ASGI has no concept of "routes", so we can't perform route discovery without a
        framework
        """
        return {}
