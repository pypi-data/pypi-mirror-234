# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.policy.trigger_actions.default_action import DefaultAction


class FromstringAction(DefaultAction):
    """
    Custom trigger action that implements XXE fromstring rule logic.

    For lxml.etree.fromstring(), if the parser has resolve_entities disabled, then
    `fromstring` is not vulnerable to XXE.
    """

    def is_violated(
        self, source_properties, required_tags, disallowed_tags, orig_args=None
    ) -> bool:
        if not super().is_violated(source_properties, required_tags, disallowed_tags):
            return False

        if orig_args is None or len(orig_args) < 2:
            return True

        parser = orig_args[1]
        if hasattr(parser, "resolve_entities") and parser.resolve_entities is False:
            return False

        return True
