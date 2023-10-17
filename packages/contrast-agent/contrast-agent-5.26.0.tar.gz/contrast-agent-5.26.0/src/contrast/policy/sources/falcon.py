# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_source_nodes
from contrast.agent.policy.utils import CompositeNode


falcon_sources = [
    CompositeNode(
        {
            "module": "falcon.request",
            "class_name": "Request",
        },
        [
            {
                "method_name": ["get_param", "params"],
                "node_type": "QUERYSTRING",
                "tags": ["NO_NEWLINES", "CROSS_SITE"],
            },
            {
                "method_name": "get_media",
                "node_type": "BODY",
                "tags": ["NO_NEWLINES", "CROSS_SITE"],
            },
        ],
    ),
    CompositeNode(
        {
            "module": "falcon.asgi.request",
            "class_name": "Request",
        },
        [
            {
                "method_name": "get_param",
                "node_type": "QUERYSTRING",
                "tags": ["NO_NEWLINES", "CROSS_SITE"],
            },
            {
                "method_name": "get_media",
                "node_type": "BODY",
                "tags": ["NO_NEWLINES", "CROSS_SITE"],
            },
        ],
    ),
    {
        "module": "falcon.asgi.stream",
        "class_name": "BoundedStream",
        "method_name": "read",
        "node_type": "BODY",
        "tags": ["NO_NEWLINES", "CROSS_SITE"],
    },
    {
        "module": "falcon.asgi.reader",
        "class_name": "BufferedReader",
        "method_name": "read",
        "node_type": "BODY",
        "tags": ["NO_NEWLINES", "CROSS_SITE"],
    },
]


register_source_nodes(falcon_sources)
