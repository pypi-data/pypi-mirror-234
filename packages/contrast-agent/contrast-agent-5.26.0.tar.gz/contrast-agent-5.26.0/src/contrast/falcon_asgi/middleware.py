# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.utils.deprecated_middleware import deprecated_asgi


FalconAsyncMiddleware = deprecated_asgi("falcon")
