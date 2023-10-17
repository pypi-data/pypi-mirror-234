# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from urllib.parse import parse_qs, urlencode, unquote

from contrast.agent.settings import Settings
from contrast.api.attack import ProtectResponse
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

MASK = "contrast-redacted-{}"
BODY_MASK = "contrast-redacted-body".encode("UTF-8")
SEMICOLON_URL_ENCODE_VAL = "%25"


class ActivityMasker:
    def __init__(self, ctx):
        self.ctx = ctx

        direct_ts_app_settings = getattr(Settings(), "direct_ts_app_settings", None)
        self.http_request = self.ctx.request
        if direct_ts_app_settings:
            self.mask_rules = direct_ts_app_settings.sensitive_data_masking_policy
        else:
            self.mask_rules = None

    def mask_sensitive_data(self):
        # Check if request is present and return if not
        if not self.http_request or not self.mask_rules:
            return

        logger.debug("Masker: masking sensitive data")

        self.mask_body()
        self.mask_query_string()
        self.mask_request_params()
        self.mask_request_cookies()
        self.mask_request_headers()

    def mask_body(self):
        # Check if mask_http_body is set to False or is None and skip if true
        if not self.mask_rules.get("mask_http_body"):
            return

        # Checks if body is not empty or null
        if self.http_request.body:
            self.http_request._masked_body = BODY_MASK

    def mask_query_string(self):
        query_string = self.http_request.query_string
        if query_string:
            self.http_request._masked_query_string = self.mask_raw_query(query_string)

    def mask_raw_query(self, query_string):
        qs_dict = parse_qs(query_string)
        self.mask_dictionary(qs_dict)
        return urlencode(qs_dict, doseq=True)

    def mask_request_params(self):
        params = self.http_request.params
        if not params:
            return

        self.http_request._masked_params = self.mask_dictionary(params)

    def mask_request_cookies(self):
        cookies = self.http_request.cookies
        if not cookies:
            return

        self.http_request._masked_cookies = self.mask_dictionary(cookies)

    def mask_request_headers(self):
        headers = self.http_request.headers
        if not headers:
            return

        self.http_request._masked_headers = self.mask_dictionary(headers)

    def mask_dictionary(self, d):
        if not d:
            return None

        d_copy = dict(d).copy()

        for k, v in d_copy.items():
            if self.find_value_index_in_rules(k.lower()) == -1:
                continue

            if isinstance(v, list):
                self.mask_values(k, v, d_copy, self.ctx.attacks)
            else:
                self.mask_hash(k, v, d_copy, self.ctx.attacks)
        return d_copy

    def mask_values(self, k, v, d, attacks):
        for idx, item in enumerate(v):
            if self.mask_rules.get("mask_attack_vector") and self.is_value_vector(
                attacks, item
            ):
                d[k][idx] = MASK.format(k.lower())
            if not self.is_value_vector(attacks, item):
                d[k][idx] = MASK.format(k.lower())

    def mask_hash(self, k, v, d, attacks):
        if self.mask_rules.get("mask_attack_vector") and self.is_value_vector(
            attacks, v
        ):
            d[k] = MASK.format(k.lower())
        if not self.is_value_vector(attacks, v):
            d[k] = MASK.format(k.lower())

    def mask_pair(self, k, v, d, attacks):
        for idx, item in enumerate(v):
            if self.mask_rules.get("mask_attack_vector") and self.is_value_vector(
                attacks, item
            ):
                d[k].values[idx] = MASK.format(k.lower())
            if not self.is_value_vector(attacks, item):
                d[k].values[idx] = MASK.format(k.lower())

    def is_value_vector(self, attacks, value):
        if not attacks or not value:
            return False

        for attack in attacks:
            if self.is_value_in_sample(attack.samples, value):
                return attack.response != ProtectResponse.NO_ACTION

        return False

    def is_value_in_sample(self, samples, value):
        if not samples:
            return False

        # Setting this to remove url encoding of header and cookie values
        value = unquote(value)

        for sample in samples:
            if sample.user_input.value == value:
                return True
        return False

    def find_value_index_in_rules(self, s):
        index = -1
        # When looking for header it replaces '_' with '-' and I don't want to risk not
        # properly matching to the rules
        s = s.replace("-", "_")
        for rule in self.mask_rules.get("rules"):
            try:
                index = rule.get("keywords").index(s)
                break
            except ValueError:
                index = -1

        return index
