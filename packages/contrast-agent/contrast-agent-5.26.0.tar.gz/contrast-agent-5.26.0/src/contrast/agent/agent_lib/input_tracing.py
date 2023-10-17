# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import ctypes
import functools
from enum import IntEnum

from contrast.agent import agent_lib
from contrast.api import TypeCheckedProperty
from contrast.api.user_input import InputType
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

# These are rules we do not have an implementation for yet
# Other rule IDs where added directly into the protect rule class
SSJS_INJECTION_RULE_ID = 1 << 7

# This should not be used directly. It's used to construct INPUT_TYPE_LOOKUP below.
_AGENT_LIB_TO_TS_INPUT_TYPE = {
    "CookieName": InputType.COOKIE_NAME,
    "CookieValue": InputType.COOKIE_VALUE,
    "HeaderKey": InputType.HEADER,
    "HeaderValue": InputType.HEADER,
    "JsonKey": InputType.JSON_VALUE,  # there is no such thing as InputType.JSON_KEY
    "JsonValue": InputType.JSON_VALUE,
    "Method": InputType.METHOD,
    "ParameterKey": InputType.PARAMETER_NAME,
    "ParameterValue": InputType.PARAMETER_VALUE,
    "UriPath": InputType.URI,
    "UrlParameter": InputType.URL_PARAMETER,
    "MultipartName": InputType.MULTIPART_NAME,
    "XmlValue": InputType.XML_VALUE,
}


class DBType(IntEnum):
    DB2 = 1
    MYSQL = 2
    ORACLE = 3
    POSTGRES = 4
    SQLITE = 5
    SQL_SERVER = 6
    UNKNOWN = 7

    @staticmethod
    def from_str(label):
        label = label.upper()
        try:
            return DBType[label]
        except KeyError:
            if label == "SQLITE3":
                return DBType.SQLITE
            if label == "POSTGRESQL":
                return DBType.POSTGRES
            if label in ("SQL SERVER", "SQL_SERVER", "SQLSERVER"):
                return DBType.SQL_SERVER

            return DBType.UNKNOWN


class CCheckQuerySinkResult(ctypes.Structure):
    _fields_ = [
        ("start_index", ctypes.c_ulonglong),
        ("end_index", ctypes.c_ulonglong),
        ("boundary_overrun_index", ctypes.c_ulonglong),
        ("input_boundary_index", ctypes.c_ulonglong),
    ]


@functools.lru_cache(maxsize=1)
def rule_id_lookup():
    """
    we'd like this to be a module-level dict, but we need to load this after agent_lib
    initialization
    """
    return {
        rule_int: rule_str
        for rule_str, rule_int in agent_lib.modules.CONSTANTS.RuleType.items()
    }


@functools.lru_cache(maxsize=1)
def input_type_lookup():
    """
    agent lib input type int -> InputType enum (TS representation)

    we'd like this to be a module-level dict, but we need to load this after agent_lib
    initialization
    """
    return {
        input_type_int: _AGENT_LIB_TO_TS_INPUT_TYPE.get(
            input_type_str, InputType.UNKNOWN
        )
        for input_type_str, input_type_int in agent_lib.modules.CONSTANTS.InputType.items()
    }


class InputAnalysisResult:
    rule_id = TypeCheckedProperty(str)
    input_type = TypeCheckedProperty(InputType, constructor_arg=InputType.UNKNOWN)
    score = TypeCheckedProperty(float)
    key = TypeCheckedProperty(str)
    value = TypeCheckedProperty(str)
    path = TypeCheckedProperty(str)
    ids = TypeCheckedProperty(list)
    attack_count = TypeCheckedProperty(int)
    prefer_worth_watching = TypeCheckedProperty(bool)

    def __init__(self, input_value, value, ceval_results, prefer_worth_watching):
        if (
            isinstance(ceval_results, agent_lib.modules.CONSTANTS.CEvalResult)
            and input_value is not None
            and isinstance(value, str)
        ):
            self.rule_id = rule_id_lookup()[ceval_results.rule_id]
            self.input_type = input_type_lookup()[ceval_results.input_type]

            self.score = ceval_results.score

            if isinstance(input_value, str):
                self.key = input_value
            elif isinstance(input_value, bytes):
                self.key = input_value.decode()
            else:
                # c_char_p
                self.key = input_value.value.decode()

            self.value = value
            self.prefer_worth_watching = prefer_worth_watching


class SQLInjectionResult:
    def __init__(self, sql_query, input_index, input_len, ccheck_query_sink_result):
        self.boundary_overrun_index = None
        self.end_index = None
        self.input_boundary_index = None
        self.start_index = None
        self.input_query = None
        self.input_index = None
        self.input_len = None

        if (
            isinstance(ccheck_query_sink_result, CCheckQuerySinkResult)
            and isinstance(sql_query, str)
            and isinstance(input_index, int)
            and isinstance(input_len, int)
        ):
            self.boundary_overrun_index = (
                ccheck_query_sink_result.boundary_overrun_index
            )
            self.end_index = ccheck_query_sink_result.end_index
            self.input_boundary_index = ccheck_query_sink_result.input_boundary_index
            self.start_index = ccheck_query_sink_result.start_index
            self.input_query = sql_query
            self.input_index = input_index
            self.input_len = input_len


def initialize_input_tracing():
    """
    This function is necessary because we only import agent_lib.modules.LIB_CONTRAST if
    we need to initialize agent-lib.
    """
    if not agent_lib.modules.is_initialized():
        return

    agent_lib.modules.LIB_CONTRAST.evaluate_header_input.argtypes = (
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_longlong,
        ctypes.c_longlong,
        ctypes.POINTER(ctypes.c_size_t),
        ctypes.POINTER(ctypes.POINTER(agent_lib.modules.CONSTANTS.CEvalResult)),
    )

    agent_lib.modules.LIB_CONTRAST.check_sql_injection_query.argtypes = (
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.POINTER(CCheckQuerySinkResult)),
    )

    agent_lib.modules.LIB_CONTRAST.evaluate_header_input.restype = ctypes.c_int
    agent_lib.modules.LIB_CONTRAST.check_sql_injection_query.restype = ctypes.c_int


def evaluate_header_input(header_name, header_value, rules, prefer_worth_watching):
    evaluations = []

    if not agent_lib.modules.is_initialized():
        return evaluations

    if rules == 0:
        return evaluations

    def is_valid_return(code):
        return code == 0

    name = ctypes.c_char_p(bytes(str(header_name), "utf8"))
    value = ctypes.c_char_p(bytes(str(header_value), "utf8"))
    results_len = ctypes.c_size_t()
    results = ctypes.POINTER(agent_lib.modules.CONSTANTS.CEvalResult)()

    ret = agent_lib.call(
        agent_lib.modules.LIB_CONTRAST.evaluate_header_input,
        is_valid_return,
        name,
        value,
        rules,
        prefer_worth_watching,
        ctypes.byref(results_len),
        ctypes.byref(results),
    )

    map_result_and_free_eval_result(
        ret,
        results,
        results_len,
        header_name,
        header_value,
        is_valid_return,
        evaluations,
        prefer_worth_watching,
    )
    return evaluations


def evaluate_input_by_type(input_type, input_value, rules, prefer_worth_watching):
    evaluations = []

    if not agent_lib.modules.is_initialized():
        return evaluations

    if rules == 0:
        return evaluations

    def is_valid_return(code):
        return code == 0

    # TODO: PYT-2826
    if not isinstance(input_value, str):
        name = ctypes.c_char_p(bytes(str(input_value), "utf8"))
    else:
        name = ctypes.c_char_p(bytes(input_value, "utf8"))
    value = ctypes.c_long(input_type)
    results_len = ctypes.c_size_t()
    results = ctypes.POINTER(agent_lib.modules.CONSTANTS.CEvalResult)()

    ret = agent_lib.call(
        agent_lib.modules.LIB_CONTRAST.evaluate_input,
        is_valid_return,
        name,
        value,
        rules,
        prefer_worth_watching,
        ctypes.byref(results_len),
        ctypes.byref(results),
    )

    map_result_and_free_eval_result(
        ret,
        results,
        results_len,
        name,
        input_value,
        is_valid_return,
        evaluations,
        prefer_worth_watching,
    )
    return evaluations


def check_method_tampering(input_value, prefer_worth_watching):
    evaluations = []

    if not agent_lib.modules.is_initialized():
        return evaluations

    def is_valid_return(code):
        return 1 >= code >= 0

    name = ctypes.c_char_p(bytes(input_value, "utf8"))

    ret = agent_lib.call(
        agent_lib.modules.LIB_CONTRAST.is_method_tampering,
        is_valid_return,
        name,
    )

    if ret != 1:
        return []

    c_eval_res = agent_lib.modules.CONSTANTS.CEvalResult()
    c_eval_res.rule_id = agent_lib.modules.CONSTANTS.RuleType.get("method-tampering")
    c_eval_res.input_type = agent_lib.modules.CONSTANTS.InputType.get("Method")
    c_eval_res.score = 100

    return [
        InputAnalysisResult(input_value, input_value, c_eval_res, prefer_worth_watching)
    ]


def check_sql_injection_query(
    user_input_start_index, user_input_len, db_type, built_sql_query
):
    if not agent_lib.modules.is_initialized():
        return None

    def is_valid_return(code):
        return -1 <= code <= 0

    input_index = ctypes.c_uint32(user_input_start_index)
    input_len = ctypes.c_uint32(user_input_len)
    db_type = ctypes.c_uint32(db_type)
    sql_query = ctypes.c_char_p(bytes(built_sql_query, "utf8"))
    results = ctypes.POINTER(CCheckQuerySinkResult)()

    ret = agent_lib.call(
        agent_lib.modules.LIB_CONTRAST.check_sql_injection_query,
        is_valid_return,
        input_index,
        input_len,
        db_type,
        sql_query,
        ctypes.byref(results),
    )

    evaluation = map_result_and_free_check_query_sink_result(
        ret,
        results,
        built_sql_query,
        user_input_start_index,
        user_input_len,
        is_valid_return,
    )
    return evaluation


def check_cmd_injection_query(user_input_start_index, user_input_len, user_input_txt):
    if not agent_lib.modules.is_initialized():
        return None

    def is_valid_return(code):
        return -1 <= code <= 0

    input_index = ctypes.c_uint32(user_input_start_index)
    input_len = ctypes.c_uint32(user_input_len)
    cmd_text = ctypes.c_char_p(bytes(user_input_txt, "utf8"))
    results = ctypes.POINTER(CCheckQuerySinkResult)()

    ret = agent_lib.call(
        agent_lib.modules.LIB_CONTRAST.check_cmd_injection_query,
        is_valid_return,
        input_index,
        input_len,
        cmd_text,
        ctypes.byref(results),
    )

    evaluation = map_result_and_free_check_query_sink_result(
        ret,
        results,
        user_input_txt,
        user_input_start_index,
        user_input_len,
        is_valid_return,
    )
    return evaluation


def map_result_and_free_eval_result(
    ret,
    results,
    results_len,
    name,
    value,
    is_valid_return,
    evaluations,
    prefer_worth_watching,
):
    if ret == 0 and bool(results) and results_len.value > 0:
        for i in range(results_len.value):
            evaluations.append(
                InputAnalysisResult(name, value, results[i], prefer_worth_watching)
            )

        # ctypes does not have OOR (original object return), it constructs a new,
        # equivalent object each time you retrieve an attribute.
        # So we can free right after we create our list
        agent_lib.call(
            agent_lib.modules.LIB_CONTRAST.free_eval_result,
            is_valid_return,
            results,
        )


def map_result_and_free_check_query_sink_result(
    ret, results, sql_query, input_index, input_len, is_valid_return
):
    if ret == 0 and bool(results):
        evaluation = SQLInjectionResult(
            sql_query, input_index, input_len, results.contents
        )

        # ctypes does not have OOR (original object return), it constructs a new,
        # equivalent object each time you retrieve an attribute.
        # So we can free right after we create our list
        agent_lib.call(
            agent_lib.modules.LIB_CONTRAST.free_check_query_sink_result,
            is_valid_return,
            results,
        )

        return evaluation
    return None
