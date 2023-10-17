# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Instrumentation for exec/eval.

This was defined outside of policy.json because we need to pass globals/locals from the
frame in which function was originally called
"""
import ast
import copy
from sys import _getframe as getframe

from contrast_vendor.wrapt import register_post_import_hook

import builtins
import contrast
from contrast.agent import scope
from contrast.agent.policy import registry
from contrast.agent.assess.policy import trigger_policy
from contrast.utils.patch_utils import build_and_apply_patch
from contrast.applies.assess.unsafe_code_execution import (
    apply_rule as apply_unsafe_code_exec_rule,
)
from contrast.utils.decorators import fail_quietly
from contrast.utils.patch_utils import wrap_and_watermark
from contrast_rewriter import PropagationRewriter, populate_operator_module


INSTRUMENTED_FRAME_DEPTH = 1

orig_compile = builtins.compile


@fail_quietly("Error applying rule for exec/eval patch")
def apply_rule(rule_applicator, orig_func, result, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()
    if not (context and context.propagate_assess):
        return

    with scope.contrast_scope():
        rule_applicator("BUILTIN", orig_func.__name__, result, args, kwargs)


@fail_quietly("Error running path traversal assess rule")
def apply_pt_rule(module, method, result, args, kwargs):
    trigger_rule = registry.get_triggers_by_rule("path-traversal")

    trigger_nodes = trigger_rule.find_trigger_nodes(module, method)

    trigger_policy.apply(trigger_rule, trigger_nodes, result, args, kwargs)


def rewrite(mode, code):
    rewriter = PropagationRewriter()
    return ast.fix_missing_locations(rewriter.visit(ast.parse(code, mode=mode)))


@fail_quietly("Error when applying rewriter to eval/exec/compiled input")
def apply_rewriter(mode, code):
    if not isinstance(code, str):
        return None

    with scope.contrast_scope():
        return orig_compile(
            rewrite(mode, code),
            filename="<internal>",
            mode=mode,
        )


def build_exec_eval_patch(orig_func, _, rule_applicator, mode):
    def exec_eval_patch(code, globs=None, locs=None):
        """
        Run exec/eval call with proper context to adjust for current frame

        Code ported from six module
        See https://github.com/benjaminp/six/blob/master/six.py#L694

        Reapplying the context from the 3rd frame (from top of stack) is necessary
        because the globals and locals in that frame are used in the original call to
        exec/eval. The exception to this is if the caller passes custom globals/locals
        to the function.

        If we fail provide this context we will see a number of errors due to things
        not defined in the scope of this function upon calling the original function
        definition.
        """
        result = None

        if globs is None:
            frame = getframe(INSTRUMENTED_FRAME_DEPTH)

            globs = frame.f_globals
            if locs is None:
                locs = frame.f_locals
            del frame
        elif locs is None:
            locs = globs

        # Ensure our rewriter patches are in (global) scope for the code about to be executed
        populate_operator_module(globs)

        try:
            code_to_run = apply_rewriter(mode, code) or code
            result = orig_func(code_to_run, globs, locs)
        except Exception:
            result = None
            raise
        finally:
            apply_rule(rule_applicator, orig_func, result, (code,), {})

        return result

    # NOTE: do not wrap since it will potentially affect stack level
    return exec_eval_patch


# NOTE: maybe this should be moved to a utility module
def find_arg(args, kwargs, idx, kw=None, default=None, pop=False):
    if kw and kw in kwargs:
        return kwargs.pop(kw) if pop else kwargs[kw]

    if len(args) <= idx:
        return default

    return args[idx]


def build_compile_patch(orig_func, _, rule_applicator):
    def compile_patch(wrapped, instance, args, kwargs):
        del instance

        if scope.in_contrast_scope():
            return wrapped(*args, **kwargs)

        result = None
        orig_kwargs = copy.copy(kwargs)

        try:
            code = find_arg(args, kwargs, 0, kw="source", pop=True)
            mode = find_arg(args, kwargs, 2, kw="mode", default="exec")

            with scope.contrast_scope():
                code_to_compile = rewrite(mode, code)
                result = orig_compile(code_to_compile, *args[1:], **kwargs)
        except Exception:
            result = None
            raise
        finally:
            apply_rule(rule_applicator, orig_func, result, args, orig_kwargs)

        return result

    return wrap_and_watermark(orig_func, compile_patch)


def patch_exec_and_eval(builtins_module):
    build_and_apply_patch(
        builtins_module,
        "eval",
        build_exec_eval_patch,
        (apply_unsafe_code_exec_rule, "eval"),
    )

    build_and_apply_patch(
        builtins_module,
        "exec",
        build_exec_eval_patch,
        (apply_unsafe_code_exec_rule, "exec"),
    )

    build_and_apply_patch(
        builtins_module, "compile", build_compile_patch, (apply_unsafe_code_exec_rule,)
    )


def register_patches():
    register_post_import_hook(patch_exec_and_eval, builtins.__name__)
