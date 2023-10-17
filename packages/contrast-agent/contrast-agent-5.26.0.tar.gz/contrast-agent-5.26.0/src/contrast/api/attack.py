# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from enum import Enum, auto

import contrast
from contrast.agent.request import Request
from contrast.utils.timer import now_ms
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class ProtectResponse(Enum):
    NO_ACTION = auto()
    BLOCKED = auto()
    MONITORED = auto()
    PROBED = auto()
    BLOCKED_AT_PERIMETER = auto()
    SUSPICIOUS = auto()


_RESPONSE_TO_TS_NAME = {
    ProtectResponse.MONITORED: "exploited",
    ProtectResponse.BLOCKED: "blocked",
    ProtectResponse.PROBED: "ineffective",
    ProtectResponse.SUSPICIOUS: "suspicious",
}


class Attack:
    """
    Class storing all data necessary to report a protect attack.
    """

    def __init__(self, rule_id):
        self.rule_id = rule_id
        self.samples = []
        self.response = None
        self.start_time_ms = contrast.CS__CONTEXT_TRACKER.current().request.timestamp_ms
        self.response = None

    @property
    def blocked(self):
        return self.response == ProtectResponse.BLOCKED

    def add_sample(self, sample):
        self.samples.append(sample)

    def set_response(self, response):
        self.response = response

    def _convert_samples(self, request: Request):
        if request is not None:
            reportable_request = request.reportable_format
        else:
            reportable_request = {}

        return [
            {
                "blocked": self.blocked,
                "input": {
                    "documentPath": sample.user_input.path,
                    "documentType": sample.user_input.document_type.name,
                    "filters": sample.user_input.matcher_ids,
                    "name": sample.user_input.key,
                    "time": sample.timestamp_ms,
                    "type": sample.user_input.input_type.name,
                    "value": sample.user_input.value,
                },
                "details": sample.details,
                "request": reportable_request,
                "stack": [
                    {
                        "declaringClass": stack.declaring_class,
                        "methodName": stack.method_name,
                        "fileName": stack.file_name,
                        "lineNumber": stack.line_number,
                    }
                    for stack in sample.stack_trace_elements
                ],
                "timestamp": {
                    "start": sample.timestamp_ms,  # in ms
                    "elapsed": (
                        now_ms() - sample.timestamp_ms
                    ),  # in ms which is the format TS accepts
                },
            }
            for sample in self.samples
        ]

    def to_json(self, request: Request):
        common_fields = {
            "startTime": 0,
            "total": 0,
        }
        json = {
            "startTime": self.start_time_ms,
            "blocked": common_fields,
            "exploited": common_fields,
            "ineffective": common_fields,
            "suspicious": common_fields,
        }

        relevant_mode = _RESPONSE_TO_TS_NAME.get(self.response)
        if relevant_mode is None:
            # Don't know what response is so just report default info so we can debug.
            return json

        samples = self._convert_samples(request)

        json[relevant_mode] = {
            "total": 1,  # always 1 until batching happens
            "startTime": self.start_time_ms,
            "samples": samples,
        }

        return json
