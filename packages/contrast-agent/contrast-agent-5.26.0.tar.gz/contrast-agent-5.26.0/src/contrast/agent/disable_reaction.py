# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast_vendor import structlog as logging
from contrast.configuration import CONTRAST_UI_SRC, ConfigOptionSrc

logger = logging.getLogger("contrast")


class DisableReaction(object):
    NAME = "DISABLE"
    ENABLE = "enable"
    MESSAGE = "Contrast received instructions to disable itself - Disabling now"

    @staticmethod
    def run(settings):
        logger.warning(DisableReaction.MESSAGE)

        if settings.config:
            src = ConfigOptionSrc(
                name=f"contrast.{DisableReaction.ENABLE}", source=CONTRAST_UI_SRC
            )
            settings.config.put(DisableReaction.ENABLE, False, src=src)
