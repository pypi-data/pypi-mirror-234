# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.providers.hardcoded_key import HardcodedKey
from contrast.agent.assess.rules.providers.hardcoded_password import HardcodedPassword
from contrast.utils.patch_utils import get_loaded_modules

PROVIDER_CLASSES = [HardcodedKey, HardcodedPassword]


def enable_providers():
    """
    Providers are non-dataflow rules that analyze the contents of a module.
    """
    for _, module in get_loaded_modules(use_for_patching=True).items():
        for provider_cls in PROVIDER_CLASSES:
            provider = provider_cls()
            if provider.applies_to(module):
                provider.analyze(module)
