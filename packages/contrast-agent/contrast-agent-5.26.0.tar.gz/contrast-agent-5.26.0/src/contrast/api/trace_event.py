# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from enum import Enum, auto

from contrast.api import TypeCheckedProperty
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class TraceEventObject(object):
    tracked = TypeCheckedProperty(bool)
    value = TypeCheckedProperty(str)
    # list of contrast.api.TraceTaintRange
    ranges = TypeCheckedProperty(list)


class TraceEventSignature(object):
    return_type = TypeCheckedProperty(str)
    class_name = TypeCheckedProperty(str)
    method_name = TypeCheckedProperty(str)
    arg_types = TypeCheckedProperty(list)
    constructor = TypeCheckedProperty(bool)
    void_method = TypeCheckedProperty(bool)
    flags = TypeCheckedProperty(int)


class ParentObjectId(object):
    id = TypeCheckedProperty(int)


class TraceEventSource(object):
    type = TypeCheckedProperty(str)
    name = TypeCheckedProperty(str)


class TraceStack(object):
    signature = TypeCheckedProperty(str)
    declaring_class = TypeCheckedProperty(str)
    method_name = TypeCheckedProperty(str)
    file_name = TypeCheckedProperty(str)
    line_number = TypeCheckedProperty(int)
    type = TypeCheckedProperty(str)
    eval = TypeCheckedProperty(str)


class TraceTaintRange(object):
    tag = TypeCheckedProperty(str)
    range = TypeCheckedProperty(str)


class TraceEvent(object):
    class EventType(Enum):
        METHOD = auto()
        PROPAGATION = auto()
        TAG = auto()

    class Action(Enum):
        CREATION = auto()
        PROPAGATION = auto()
        TRIGGER = auto()
        TAG = auto()
        A2A = auto()
        A2P = auto()
        A2O = auto()
        A2R = auto()
        O2A = auto()
        O2P = auto()
        O2O = auto()
        O2R = auto()
        P2A = auto()
        P2P = auto()
        P2O = auto()
        P2R = auto()

    action = TypeCheckedProperty(Action, constructor_arg=Action.CREATION)
    type = TypeCheckedProperty(EventType, constructor_arg=EventType.METHOD)
    timestamp_ms = TypeCheckedProperty(int)
    thread = TypeCheckedProperty(str)
    signature = TypeCheckedProperty(TraceEventSignature)
    field_name = TypeCheckedProperty(str)
    context = TypeCheckedProperty(str)
    code = TypeCheckedProperty(str)
    object = TypeCheckedProperty(TraceEventObject)
    ret = TypeCheckedProperty(TraceEventObject)
    # list of TraceEventObject
    args = TypeCheckedProperty(list)
    # list of TraceStack
    stack = TypeCheckedProperty(list)
    # list of TraceEventSource
    event_sources = TypeCheckedProperty(list)
    tags = TypeCheckedProperty(set)
    source = TypeCheckedProperty(str)
    target = TypeCheckedProperty(str)
    # list of contrast.api.TraceTaintRange
    taint_ranges = TypeCheckedProperty(list)
    object_id = TypeCheckedProperty(int)
    # list of repeated contrast.api.ParentObjectId
    parent_object_ids = TypeCheckedProperty(list)

    def to_json(self):
        return {
            "action": self.action.name,
            "args": [
                {
                    # "hash": 0,  # not required
                    "tracked": arg.tracked,
                    "value": arg.value,
                }
                for arg in self.args
            ],
            # "code": "string",  # currently unused; maybe useful in the future
            "eventSources": [
                {
                    "sourceName": s.name,
                    "sourceType": s.type,
                }
                for s in self.event_sources
            ],
            "fieldName": self.field_name,
            "object": {
                # "hash": 0,  # not required
                "tracked": self.object.tracked,
                "value": self.object.value,
            },
            "objectId": self.object_id,
            "parentObjectIds": [{"id": p.id} for p in self.parent_object_ids],
            # properties not used for dataflow rules
            # "properties": [{"key": "string", "value": "string"}],
            "ret": {
                # "hash": 0,  # not required
                "tracked": self.ret.tracked,
                "value": self.ret.value,
            },
            "signature": {
                "argTypes": list(self.signature.arg_types),
                "className": self.signature.class_name,
                "constructor": self.signature.constructor,
                # not required
                # "expressionType": "MEMBER_EXPRESSION",
                # "flags": 0,  # java only
                "methodName": self.signature.method_name,
                # not required
                # "operator": "string",
                "returnType": self.signature.return_type,
                # "signature": "string",  # deprecated
                "voidMethod": self.signature.void_method,
            },
            "source": self.source,
            "stack": [
                {
                    "eval": s.eval,
                    "file": s.file_name,
                    "lineNumber": s.line_number,
                    "method": s.method_name,
                    "signature": s.signature,
                    "type": s.type,
                }
                for s in self.stack
            ],
            # "tags": "string",  # we don't save this to the object
            "taintRanges": [
                {
                    "tag": t.tag,
                    "range": t.range,
                }
                for t in self.taint_ranges
            ],
            "target": self.target,
            # "thread": "string",  # not required
            "time": self.timestamp_ms,
            "type": self.type.name,
        }
