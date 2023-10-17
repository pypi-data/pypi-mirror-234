# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import requests

from .base_ts_message import BaseTsAppMessage
from contrast.reporting.activity_masker import ActivityMasker
from contrast.utils.decorators import fail_loudly
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class ApplicationActivity(BaseTsAppMessage):
    def __init__(self, context):
        super().__init__()
        ActivityMasker(context).mask_sensitive_data()

        self.body = {"lastUpdate": self.since_last_update}

        self.body["inventory"] = {
            # Used by TeamServer to aggregate counts across a given time period, for
            # Protect and attacker activity.
            "activityDuration": 0,
            "components": [],
        }
        if context.request and context.request.user_agent:
            self.body["inventory"]["browsers"] = [context.request.user_agent]
        if context.database_info:
            for db_info in context.database_info:
                self.body["inventory"]["components"].append(db_info)

        if context.attacks:
            self.body["defend"] = {"attackers": []}

            for attack in context.attacks:
                self.body["defend"]["attackers"].append(
                    {
                        "protectionRules": {
                            attack.rule_id: attack.to_json(context.request)
                        },
                        "source": {
                            "ip": context.request.client_addr or "",
                            "xForwardedFor": context.request.headers.get(
                                "X-Forwarded-For"
                            )
                            or "",
                        },
                    }
                )

    @property
    def name(self):
        return "application-activity"

    @property
    def path(self):
        return "activity/application"

    @property
    def request_method(self):
        return requests.put

    @property
    def expected_response_codes(self):
        return [200, 204]

    @fail_loudly("Failed to process Activity response")
    def process_response(self, response, reporting_client):
        self.process_response_code(response, reporting_client)
