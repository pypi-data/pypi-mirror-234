# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os

from contrast_rewriter import rewrite_for_pytest
from contrast.agent.patch_controller import enable_assess_patches
from contrast.agent.policy.rewriter import apply_rewrite_policy
from contrast.configuration import AgentConfig
from contrast.patches import register_middleware_patches
from contrast_vendor import structlog as logging

from contrast.scripts.runner import USING_RUNNER_ENV_VAR

logger = logging.getLogger("contrast")


def is_runner_in_use() -> bool:
    return os.environ.get(USING_RUNNER_ENV_VAR, "false") == "true"


def start_runner():
    if rewrite_for_pytest():
        if bool(os.environ.get("__POLICY_REWRITES_WHILE_TESTING", False)):
            apply_rewrite_policy(override_config=True)
        return

    config = AgentConfig()

    # Policy-based rewrites need to be applied prior to any policy patches.
    # Policy patches can be layered on top of rewritten functions. So that
    # means we need to make sure that the "original" function called by the
    # policy patch is the *rewritten* one.
    if config.should_apply_policy_rewrites:
        apply_rewrite_policy()

    if config.enable_automatic_middleware:
        register_middleware_patches()

    if config.assess_enabled:
        # NOTE: policy is currently loaded/registered upon import
        from contrast import policy  # pylint: disable=unused-import

        enable_assess_patches()
