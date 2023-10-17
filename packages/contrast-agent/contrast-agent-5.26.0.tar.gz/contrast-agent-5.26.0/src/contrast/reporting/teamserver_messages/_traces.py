# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import requests

from .base_ts_message import BaseTsAppMessage
from contrast.utils.decorators import fail_loudly
from contrast.utils.timer import now_ms
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class _Traces(BaseTsAppMessage):
    """This class should only be instantiated by Preflight's response handler"""

    def __init__(self, finding, reportable_request):
        super().__init__()

        self.headers.update({"Report-Hash": finding.preflight.split(",")[-1]})

        self.body = self._build_body(finding, reportable_request)

    @property
    def name(self) -> str:
        return "traces"

    @property
    def path(self) -> str:
        return "traces"

    @property
    def request_method(self) -> str:
        return requests.put

    @fail_loudly("Failed to process Traces response")
    def process_response(self, response, reporting_client):
        self.process_response_code(response, reporting_client)

    def _build_body(self, finding, reportable_request):
        base_body = {
            "created": (
                finding.events[-1].timestamp_ms if len(finding.events) > 0 else now_ms()
            ),
            "events": [event.to_json() for event in finding.events],
            "properties": finding.properties,
            "routes": [route.to_json_traces() for route in finding.routes],
            "ruleId": finding.rule_id,
            "session_id": self.settings.config.session_id,
            "tags": self.settings.config.assess_tags,
            "version": finding.version,
        }
        if reportable_request is not None:
            base_body["request"] = reportable_request

        return base_body
