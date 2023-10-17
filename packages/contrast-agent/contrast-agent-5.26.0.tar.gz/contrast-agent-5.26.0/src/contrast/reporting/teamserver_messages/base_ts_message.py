# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import base64
import requests.models
from datetime import timedelta

import contrast
from contrast.agent.disable_reaction import DisableReaction
from contrast.agent.settings import Settings
from contrast.utils.object_utils import NOTIMPLEMENTED_MSG
from contrast.utils.decorators import fail_loudly
from contrast.utils.timer import now_ms, sleep

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


PYTHON = "Python"
SLEEP_TIME_SECS = timedelta(minutes=15).seconds


def _b64url_stripped(header_str):
    """
    For some headers, TS expects a value that
    - is base64 encoded using URL-safe characters
    - has any padding (= or ==) stripped

    This follows RFC-4648 - base64 with URL and filename safe alphabet
    """
    return base64.urlsafe_b64encode(header_str.encode()).rstrip(b"=").decode("utf-8")


class BaseTsMessage:
    def __init__(self):
        self._sent_count = 0
        self.settings = Settings()

        self.base_url = f"{self.settings.api_url}/api/ng/"
        self.proxy = (
            self.settings.build_proxy_url() if self.settings.is_proxy_enabled else {}
        )

        self.server_name_b64 = _b64url_stripped(self.settings.get_server_name())
        self.server_path_b64 = _b64url_stripped(self.settings.get_server_path())
        self.server_type_b64 = _b64url_stripped(self.settings.get_server_type())
        auth_header = f"{self.settings.api_user_name}:{self.settings.api_service_key}"

        self.headers = {
            # the Authorization header must not have its padding stripped
            "Authorization": base64.urlsafe_b64encode(auth_header.encode()).decode(),
            "API-Key": self.settings.api_key,
            "Server-Name": self.server_name_b64,
            "Server-Path": self.server_path_b64,
            "Server-Type": self.server_type_b64,
            "X-Contrast-Agent": f"{PYTHON} {contrast.__version__}",
            "X-Contrast-Header-Encoding": "base64",
        }

        self.body = ""

    @property
    def class_name(self):
        return type(self).__name__.lstrip("_")

    @property
    def name(self) -> str:
        """
        Used for request audit filename
        """
        raise NotImplementedError(NOTIMPLEMENTED_MSG)

    @property
    def path(self) -> str:
        """
        URL path for teamserver; used for formatting as "/api/ng/{path}"
        """
        raise NotImplementedError(NOTIMPLEMENTED_MSG)

    @property
    def request_method(self) -> str:
        raise NotImplementedError(NOTIMPLEMENTED_MSG)

    @property
    def expected_response_codes(self):
        return [204]

    @property
    def disable_agent_on_401_and_408(self):
        return False

    @property
    def sent_count(self):
        return self._sent_count

    def sent(self):
        self._sent_count += 1

    @fail_loudly("Failed to process TS response")
    def process_response(
        self, response: requests.models.Response, reporting_client
    ) -> None:
        del response, reporting_client
        raise NotImplementedError(NOTIMPLEMENTED_MSG)

    def should_shutdown(self, response: requests.models.Response) -> bool:
        """
        Validate 404 NotFoundApplication or NotFoundServer response

        From the spec:

        "Note that the agent should only consider this a valid response if the body
        is present and matches the schema defined for `ResponseMessage`.  Specifically,
        an agent should parse this response and check for a `success` value of `false`
        before disabling."

        https://github.com/Contrast-Security-Inc/contrast-agent-api-spec/blob/master/agent-endpoints.yml
        """
        try:
            body = response.json()
            return body.get("success") == False
        except Exception:
            pass

        return False

    def process_response_code(
        self, response, reporting_client
    ):  # pylint: disable=too-many-return-statements
        """
        Return True if response code is expected response code
        """
        if not isinstance(response, requests.models.Response):
            return False

        logger.debug(
            "%s: received %s response code from Teamserver",
            self.class_name,
            response.status_code,
        )

        if response.status_code in (204, 304):
            # Both of these codes indicate no content, meaning there is no
            # action for us to take. Nothing has changed on TeamServer for
            # us to process.
            return False

        if response.status_code == 404:
            if self.should_shutdown(response):
                DisableReaction.run(self.settings)
            return False

        if response.status_code in (409, 410, 412, 502):
            # 409: app is archived, 502 app is locked in TS
            # 410: app is not registered. We could send App startup for not we won't
            # 412: API key no longer valid. While spec may say to resend msg in 15 mins,
            #  in reality the app server and agent should simply be restarted.
            DisableReaction.run(self.settings)
            return False

        if response.status_code in (401, 408):
            # 401: Access forbidden because credentials failed to authenticate.
            # 408: TS Could not create settings in time.
            if self.disable_agent_on_401_and_408:
                DisableReaction.run(self.settings)
            else:
                logger.debug("Sleeping for 15 minutes")

                sleep(SLEEP_TIME_SECS)

                reporting_client.retry_message(self)

            return False

        if response.status_code == 429:
            sleep_time = int(response.headers.get("Retry-After", SLEEP_TIME_SECS))

            logger.debug("Sleeping for %s seconds", sleep_time)

            sleep(sleep_time)

            reporting_client.retry_message(self)

        if response.status_code not in self.expected_response_codes:
            logger.debug(
                "Unexpected %s response from TS: %s",
                self.class_name,
                response.status_code,
            )
            return False

        return True


class BaseTsServerMessage(BaseTsMessage):
    @fail_loudly(f"Failed to process server settings response")
    def process_response(self, response, reporting_client):
        settings = Settings()
        if not self.process_response_code(response, reporting_client):
            return

        body = response.json()

        settings.apply_ts_feature_settings(body)
        settings.process_ts_reactions(body)


class BaseTsAppMessage(BaseTsMessage):
    def __init__(self):
        super().__init__()

        # App language should only be encoded for url paths, not for headers.
        self.app_language_b64 = _b64url_stripped(PYTHON)
        self.app_name_b64 = _b64url_stripped(self.settings.app_name)

        self.headers.update(
            {
                "Application-Language": PYTHON,
                "Application-Name": self.app_name_b64,
                "Application-Path": _b64url_stripped(self.settings.app_path),
            }
        )

    @property
    def since_last_update(self):
        """
        Time in ms since app settings have been updated.
        If never updated, then it's been 0ms since then.
        """
        if self.settings.last_app_update_time_ms == 0:
            return 0
        return now_ms() - self.settings.last_app_update_time_ms
