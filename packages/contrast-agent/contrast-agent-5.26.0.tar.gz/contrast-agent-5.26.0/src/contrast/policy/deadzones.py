# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_deadzone_nodes


deadzone_nodes = [
    {
        # Prevent recursive propagation when logging in assess
        # We run the risk of recursively logging propagation events inside of log
        # statements. This is because the logging module sometimes uses streams to
        # output logs, and these logging events can inadvertently cause additional
        # log output that we use for debugging within our assess code. We want to
        # prevent this from occurring. Part of the reason for this is that we now
        # instrument stream reads and writes, but we also are aware that StringIO
        # is implemented with a lot of string building under the hood.
        "module": "logging",
        "class_name": "StreamHandler",
        "method_name": "emit",
        "policy_patch": True,
    },
    {
        # Werkzeug's request body parser (used by flask.request.files) causes a lot of
        # propagation. We deadzone this, but we have source nodes / logic for tracking
        # all resulting objects.
        "module": "werkzeug.formparser",
        "class_name": "FormDataParser",
        "method_name": "parse",
    },
    {
        # This method causes potential false positives for unsafe-code-execution.
        # It is presumed safe to deadzone since it is implemented by the framework.
        # The actual issue is caused by the .name attribute but we don't currently
        # support deadzones for properties.
        "module": "werkzeug.exceptions",
        "class_name": "HTTPException",
        "method_name": "get_body",
    },
    {
        # This is django's request body parser. We have source nodes for the objects
        # storing data that is parsed out of the request body here. This deadzone saves
        # us from performing needless propagation without sacrificing any correctness.
        "module": "django.http.request",
        "class_name": "HttpRequest",
        "method_name": "_load_post_and_files",
    },
    {
        # This is DRF's request body parser. See comments for other body parsers.
        "module": "rest_framework.request",
        "class_name": "Request",
        "method_name": "_parse",
    },
    {
        # Built-in request body parser used by at least Bottle and Pyramid. This patch
        # is actually handled explicitly, but the deadzone here is for clarity. We also
        # use cgi.FieldStorage.__init__ as an entrypoint for explicitly patching the
        # relevant attributes of the FieldStorage object itself (as sources).
        "module": "cgi",
        "class_name": "FieldStorage",
        "method_name": "__init__",
        "policy_patch": False,
    },
    {
        # See FieldStorage. It's not essential that we deadzone this, but it keeps
        # MiniFieldStorage and FieldStorage consistent.
        "module": "cgi",
        "class_name": "MiniFieldStorage",
        "method_name": "__init__",
        "policy_patch": False,
    },
    {
        # UUIDs aren't controllable and they're hex encoded. It is essentially
        # impossible for a UUID to trigger a real vulnerability
        "module": "uuid",
        "class_name": "UUID",
        "method_name": "__str__",
    },
    {
        # This currently causes an unvalidated-redirect in the case where the
        # middleware appends a '/' to the request path and redirects
        "module": "django.middleware.common",
        "class_name": "CommonMiddleware",
        "method_name": "process_request",
    },
    {
        # This code is responsible for rendering the django debug page.
        "module": "django.views.debug",
        "class_name": "ExceptionReporter",
        "method_name": "get_traceback_data",
    },
    {
        # Too much propagation / source creation occurs here. It is not necessary for
        # body tracking since we accomplish this with higher-level source nodes
        "module": "quart.wrappers.request",
        "class_name": "Request",
        "method_name": "_load_form_data",
    },
    {
        # Prevents our rewriter from being applied to assertion rewrites in pytest
        "module": "_pytest.assertion.rewrite",
        "class_name": "AssertionRewritingHook",
        "method_name": "exec_module",
    },
]


register_deadzone_nodes(deadzone_nodes)
