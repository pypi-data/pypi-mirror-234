# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Implements patches for the operator module

Our propagation rewrites are implemented in terms of these patches, so they
must always be enabled when Assess is enabled.
"""
import sys

from contrast_vendor.wrapt import register_post_import_hook

from contrast.agent import scope
from contrast.agent.assess.utils import is_trackable
from contrast.agent.assess.policy import string_propagation
from contrast.agent.policy import patch_manager
from contrast.patches.utils import analyze_policy, get_propagation_node
from contrast.utils.decorators import fail_quietly
from contrast.utils.patch_utils import build_and_apply_patch, wrap_and_watermark


@fail_quietly("failed to propagate through modulo in contrast__cformat__modulo")
def _propagate_cformat(result, format_str, args):
    propagation_func = None

    if isinstance(result, str):
        propagation_func = string_propagation.propagate_unicode_cformat
    elif isinstance(result, bytes):
        propagation_func = string_propagation.propagate_bytes_cformat
    elif isinstance(result, bytearray):
        # TODO: PYT-2709 - Update tests to verify bytearray is supported with and without funchook
        propagation_func = string_propagation.propagate_bytearray_cformat

    if propagation_func is None:
        return

    with scope.contrast_scope(), scope.propagation_scope():
        propagation_func(result, format_str, result, args, None)


def build_add_hook(original_func, patch_policy):
    policy_node = get_propagation_node(patch_policy)

    def add(wrapped, instance, args, kwargs):
        del instance

        with scope.contrast_scope():
            result = wrapped(*args, **kwargs)
        if not is_trackable(result) or scope.in_scope():
            return result

        analyze_policy(policy_node.name, result, args, kwargs)

        return result

    return wrap_and_watermark(original_func, add)


def build_mod_hook(original_func, patch_policy):
    # cformat is a bit of a special case so we don't use policy here
    del patch_policy

    def mod(wrapped, instance, args, kwargs):
        del instance

        with scope.contrast_scope():
            result = wrapped(*args, **kwargs)
        if not is_trackable(result) or scope.in_scope():
            return result

        _propagate_cformat(result, *args)

        return result

    return wrap_and_watermark(original_func, mod)


def patch_operator(operator_module):
    build_and_apply_patch(operator_module, "add", build_add_hook)
    build_and_apply_patch(operator_module, "iadd", build_add_hook)
    build_and_apply_patch(operator_module, "mod", build_mod_hook)


def register_patches():
    register_post_import_hook(patch_operator, "operator")


def reverse_patches():
    operator_module = sys.modules.get("operator")
    if not operator_module:
        return

    patch_manager.reverse_patches_by_owner(operator_module)
