# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import requests

from .base_ts_message import BaseTsServerMessage
from contrast import get_canonical_version


class ServerStartup(BaseTsServerMessage):
    def __init__(self):
        super().__init__()

        self.body = {
            "environment": self.settings.config.get("server.environment"),
            "tags": self.settings.config.get("server.tags"),
            "version": get_canonical_version(),
        }

    @property
    def name(self):
        return "server-startup"

    @property
    def path(self):
        return "servers/"

    @property
    def expected_response_codes(self):
        return [200]

    @property
    def request_method(self):
        return requests.put

    @property
    def disable_agent_on_401_and_408(self):
        return True
