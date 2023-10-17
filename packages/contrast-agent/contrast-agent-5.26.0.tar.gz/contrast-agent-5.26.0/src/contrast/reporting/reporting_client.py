# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import threading
import queue

from .teamserver_messages import BaseTsMessage
from contrast.agent import scope
from contrast.agent.disable_reaction import DisableReaction
from contrast.agent.settings import Settings
from contrast.reporting import RequestAudit
from contrast_vendor import structlog as logging
from contrast.utils.singleton import Singleton

logger = logging.getLogger("contrast")

REPORTING_CLIENT_THREAD_NAME = "ContrastReportingClient"

MAX_ATTEMPTS = 2
ERROR_STATUS_CODE = -1


class ReportingClient(Singleton, threading.Thread):
    def init(self):
        self.stopped = False
        self.message_q = queue.Queue(maxsize=128)
        self.settings = Settings()
        self.request_audit = (
            RequestAudit(self.settings.config)
            if self.settings.config.is_request_audit_enabled
            else None
        )

        if self.request_audit:
            self.request_audit.prepare_dirs()

        super().__init__()
        # A thread must have had __init__ called, but not start, to set daemon
        self.daemon = True
        self.name = REPORTING_CLIENT_THREAD_NAME

    def start(self):
        self.stopped = False
        super().start()

    def run(self):
        with scope.contrast_scope():
            logger.debug("Starting reporting thread")

            while not self.stopped and self.settings.is_agent_config_enabled():
                try:
                    msg = self.message_q.get(block=True, timeout=5)
                    response = self.send_message(msg)
                    msg.process_response(response, self)
                except queue.Empty:
                    pass
                except Exception as e:
                    logger.debug(
                        "WARNING: reporting client failed to send message", exc_info=e
                    )

    def send_message(self, msg):
        status_code = ERROR_STATUS_CODE
        msg_name = msg.class_name

        try:
            logger.debug("Sending %s message to Teamserver", msg_name)

            cert = None
            url = msg.base_url + msg.path

            if (
                self.settings.is_cert_verification_enabled
                and not self.settings.ignore_cert_errors
            ):
                if (
                    not self.settings.ca_file
                    or not self.settings.client_cert_file
                    or not self.settings.client_private_key
                ):
                    logger.error(
                        "Unable to communicate with Contrast. "
                        "Certificate configuration is not set properly."
                    )
                    DisableReaction.run(self.settings)
                    return None

                cert = (
                    self.settings.client_cert_file,
                    self.settings.client_private_key,
                )

            response = msg.request_method(
                url,
                json=msg.body,
                proxies=msg.proxy,
                headers=msg.headers,
                allow_redirects=False,
                verify=False
                if self.settings.ignore_cert_errors
                else (self.settings.ca_file or True),
                cert=cert,
            )

            try:
                status_code = response.status_code
                msg_success_status = response.json().get("success")
                messages = response.json().get("messages")
                if not msg_success_status:
                    logger.error(
                        "Failure on Contrast UI processing request reason - (%s): %s",
                        messages,
                        status_code,
                    )
            except Exception as e:
                if status_code == ERROR_STATUS_CODE:
                    logger.debug(
                        "Failed to receive response from Contrast UI: %s ",
                        e,
                    )

            logger.debug("Contrast UI response (%s): %s", msg_name, status_code)

            if self.request_audit:
                self.request_audit.audit(msg, response)

            msg.sent()
            return response

        except Exception as e:
            logger.exception("Failed to send %s message to Contrast: %s", msg_name, e)

        return None

    def add_message(self, msg):
        if msg is None or not isinstance(msg, BaseTsMessage):
            return

        logger.debug("Adding msg to reporting queue: %s", msg.class_name)

        self.message_q.put(msg)

    def retry_message(self, msg):
        # Never send a message more than twice (original time plus one retry)
        # To prevent queue from filling up or causing memory issues.
        if msg.sent_count < MAX_ATTEMPTS:
            logger.debug("Re-enqueuing %s message", msg.class_name)
            self.add_message(msg)
