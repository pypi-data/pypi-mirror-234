# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

import contrast
from contrast_vendor.wrapt import register_post_import_hook
from contrast.agent.assess.policy.analysis import analyze
from contrast.agent.policy import patch_manager
from contrast.agent.policy.applicator import apply_assess_patch
from contrast.agent.policy import registry
from contrast.patches import urllib_patch
from contrast.utils.decorators import fail_quietly
from contrast.utils.patch_utils import build_and_apply_patch, wrap_and_watermark
from contrast.agent import scope

from contrast_vendor import structlog as logging


logger = logging.getLogger("contrast")

PYRAMID_SESSION_MODULE = "pyramid.session"
PYRAMID_ROUTER_MODULE = "pyramid.router"


@fail_quietly("Failed to apply policy to new session class")
def _apply_policy(session_cls):
    for patch_policy in registry.get_policy_by_module(PYRAMID_SESSION_MODULE):
        if patch_policy.class_name == "CookieSession":
            apply_assess_patch(session_cls, patch_policy)


@fail_quietly("Failed to apply assess policy for BaseCookieSessionFactory")
def _apply_assess(result, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    patch_policy = registry.get_policy_by_name(
        "pyramid.session.BaseCookieSessionFactory"
    )

    analyze(context, patch_policy, result, args, kwargs)


def build_base_cookie_session_factory_patch(orig_func, _):
    def base_cookie_session_factory(wrapped, instance, args, kwargs):
        """
        base_cookie_session_factory is a function that returns a new CookieSession class

        Since we can't instrument the new class directly using normal policy machinery,
        we instead apply our policy on-demand to the newly created class.
        """
        del instance

        session_cls = None
        try:
            session_cls = wrapped(*args, **kwargs)
            _apply_policy(session_cls)
        finally:
            _apply_assess(session_cls, args, kwargs)

        return session_cls

    return wrap_and_watermark(orig_func, base_cookie_session_factory)


def patch_session_pyramid(pyramid_session_module):
    build_and_apply_patch(
        pyramid_session_module,
        "BaseCookieSessionFactory",
        build_base_cookie_session_factory_patch,
    )


def patch_encode_pyramid(pyramid_encode_module):
    # We go ahead and apply all urllib patches here (even though policy
    # patches will happen later on) because we MUST have some urllib policy patches
    # already applied for these non-policy patches to work.
    # This would not be necessary if in _enable_patches policy_patches were applied
    # first.
    urllib_patch.register_patches()

    import urllib.parse

    # Make sure that we use patched versions of these functions. This is
    # probably handled by repatching in most circumstances but this change was
    # necessary in order to get the pyramid patch tests to pass in the full
    # test suite.
    pyramid_encode_module.quote_plus = urllib.parse.quote_plus
    pyramid_encode_module._url_quote = urllib.parse.quote

    # We can reuse the urllib.parse.urlencode patch since it's exactly the same
    # as the pyramid.encode.urlencode patch
    build_and_apply_patch(
        pyramid_encode_module, "urlencode", urllib_patch.build_urlencode_patch
    )


def build_call_patch(orig_func, patch_policy):
    """
    Patch for pyramid.router.Router.__call__

    This is how we perform route discovery and observation for Pyramid.
    """
    del patch_policy

    def call_patch(wrapped, instance, args, kwargs):
        try:
            result = wrapped(*args, **kwargs)
        finally:
            do_pyramid_routes_discovery(instance)
            do_pyramid_routes_observation(instance, args)
        return result

    return wrap_and_watermark(orig_func, call_patch)


@fail_quietly("unable to perform Pyramid routes discovery")
@scope.with_contrast_scope
def do_pyramid_routes_discovery(pyramid_router_instance):
    from contrast.agent.middlewares.route_coverage.pyramid_routes import (
        create_pyramid_routes,
    )

    from contrast.agent import agent_state

    if not agent_state.is_first_request():
        return

    discovered_routes = create_pyramid_routes(pyramid_router_instance.registry)
    agent_state.update_routes(discovered_routes)

    logger.debug(
        "Discovered the following Pyramid routes: %s",
        [f"{route.verb} {route.url}" for route in discovered_routes.values()],
    )


@fail_quietly("unable to perform Pyramid route observation")
@scope.with_contrast_scope
def do_pyramid_routes_observation(pyramid_router_instance, request_path_arg):
    from contrast.agent.middlewares.route_coverage.pyramid_routes import (
        get_view_func,
        build_route,
    )

    request_path = request_path_arg[0]["PATH_INFO"]
    view_func = get_view_func(
        request_path,
        pyramid_router_instance.routes_mapper.routelist,
        pyramid_router_instance.registry,
    )

    context = contrast.CS__CONTEXT_TRACKER.current()
    if context is None:
        return

    context.view_func = view_func
    context.view_func_str = build_route(
        context.view_func,
        context.request.get_normalized_uri(),
    )
    logger.debug("Observed Pyramid route: %s", context.view_func_str)


def patch_pyramid(pyramid_router_module):
    build_and_apply_patch(pyramid_router_module.Router, "__call__", build_call_patch)


def register_patches():
    register_post_import_hook(patch_pyramid, PYRAMID_ROUTER_MODULE)
    register_post_import_hook(patch_session_pyramid, PYRAMID_SESSION_MODULE)
    register_post_import_hook(patch_encode_pyramid, "pyramid.encode")


def reverse_patches():
    pyramid_router_module = sys.modules.get(PYRAMID_ROUTER_MODULE)
    pyramid_session = sys.modules.get(PYRAMID_SESSION_MODULE)
    pyramid_encode = sys.modules.get("pyramid.encode")

    if pyramid_session:
        patch_manager.reverse_patches_by_owner(pyramid_session)
    if pyramid_encode:
        patch_manager.reverse_patches_by_owner(pyramid_encode)
        urllib_patch.reverse_patches()
    if pyramid_router_module:
        patch_manager.reverse_patches_by_owner(pyramid_router_module.Router)
