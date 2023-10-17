# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import requests

from .base_ts_message import BaseTsServerMessage
from contrast.agent.settings import Settings
from contrast.utils.decorators import fail_loudly
from contrast.utils.timer import now_ms


class ServerActivity(BaseTsServerMessage):
    def __init__(self):
        super().__init__()

        self.body = {"lastUpdate": self.since_last_update}

    @property
    def name(self):
        return "server-activity"

    @property
    def path(self):
        return "activity/server"

    @property
    def request_method(self):
        return requests.put

    @property
    def expected_response_codes(self):
        return [200, 304]

    @property
    def since_last_update(self):
        """
        Time in ms since server have been updated.
        If never updated, then it's been 0ms since then.
        """
        if self.settings.last_server_update_time_ms == 0:
            return 0
        return now_ms() - self.settings.last_server_update_time_ms

    @fail_loudly("Failed to process ServerActivity response")
    def process_response(self, response, reporting_client):
        settings = Settings()

        # TS will not send server settings unless lastUpdate is >= 5 mins (300_000 ms)
        # The response in those cases is 304.
        if (
            not self.process_response_code(response, reporting_client)
            or response.status_code == 304
        ):
            return

        body = response.json()

        settings.apply_ts_feature_settings(body)
        settings.process_ts_reactions(body)
