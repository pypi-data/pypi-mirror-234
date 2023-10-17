# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
agent_lib.initialize() will initialize the module references here. This guarantees that
we handle the `contrast_agent_lib` import safely by restricting it to that function.
"""
LIB_CONTRAST = None
CONSTANTS = None


def is_initialized():
    return LIB_CONTRAST is not None
