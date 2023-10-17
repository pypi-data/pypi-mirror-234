# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from enum import Enum, auto


class ProtectionRule(Enum):
    OFF = auto()
    MONITOR = auto()
    BLOCK = auto()
    BLOCK_AT_PERIMETER = auto()
    PERMIT = auto()
