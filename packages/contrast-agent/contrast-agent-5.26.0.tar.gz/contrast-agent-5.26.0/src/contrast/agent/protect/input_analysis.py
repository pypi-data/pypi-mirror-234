# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast

import xml.etree.ElementTree
from contrast.utils.loggers.logger import security_log_msg
from contrast.utils.string_utils import ensure_string

from contrast.api.user_input import DocumentType, InputType
from contrast.agent.settings import Settings
from contrast.agent import agent_lib
from contrast_vendor import structlog as logging
from contrast.utils.decorators import fail_quietly

logger = logging.getLogger("contrast")


def _get_enabled_rules():
    """
    This converts our list of enabled rules to an integer value as the bitmask that the
    Agent Library expects.
    """
    rules = 0
    settings = Settings()

    for rule_tuple in settings.protect_rules.items():
        if (
            rule_tuple
            and rule_tuple[1]
            and rule_tuple[1].enabled
            and rule_tuple[1].RULE_NAME in agent_lib.modules.CONSTANTS.RuleType
        ):
            rules |= agent_lib.modules.CONSTANTS.RuleType[rule_tuple[1].RULE_NAME]
    return rules


def get_input_analysis(*, prefer_worth_watching=True):
    """
    Get input analysis from agent-lib. Results are stored on
    context.user_input_analysis, which is reset every time this function is called.

    Some rules have a special "worth watching" analysis mode. In prefilter, we use this
    more liberal mode to ensure we don't miss attacks that should be blocked at trigger
    time. However, if we make it to the end of the request (without raising a
    SecurityException), we redo input analysis with worth watching mode disabled, which
    leads to more accurate PROBED results (fewer PROBED FPs).
    """
    context = contrast.CS__CONTEXT_TRACKER.current()
    if context is None:
        return

    context.user_input_analysis = []
    exclusions = Settings().exclusions

    rules = _get_enabled_rules()

    # Input analysis for all the input_tracing.InputType enum values
    _evaluate_headers(context, rules, prefer_worth_watching, exclusions)
    _evaluate_cookies(context, rules, prefer_worth_watching, exclusions)
    _evaluate_body(context, rules, prefer_worth_watching, exclusions)
    _call_check_method_tampering(context, prefer_worth_watching)
    _evaluate_query_string_params(context, rules, prefer_worth_watching, exclusions)
    _call_agent_lib_evaluate_input(
        agent_lib.modules.CONSTANTS.InputType.get("UriPath"),
        context.request.path,
        rules,
        prefer_worth_watching,
        context,
    )
    _evaluate_path_params(context, rules, prefer_worth_watching, exclusions)
    _evaluate_multipart_request(context, rules, prefer_worth_watching)


def _evaluate_headers(context, rules, prefer_worth_watching, exclusions):
    for header_name, header_value in context.request.headers.items():
        if "cookie" in header_name.lower() or check_param_input_exclusions(
            exclusions, "HEADER", header_name
        ):
            continue

        input_analysis = agent_lib.evaluate_header_input(
            header_name, header_value, rules, prefer_worth_watching
        )

        if input_analysis:
            context.user_input_analysis.extend(input_analysis)
            # Report and block attack if necessary
            _report_and_block_by_rule_list(
                input_analysis,
                ["bot-blocker", "reflected-xss", "unsafe-file-upload"],
                context,
            )


def _evaluate_cookies(context, rules, prefer_worth_watching, exclusions):
    for cookie_name, cookie_value in context.request.cookies.items():
        if check_param_input_exclusions(exclusions, "COOKIE", cookie_name):
            continue

        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("CookieName"),
            cookie_name,
            rules,
            prefer_worth_watching,
            context,
        )
        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("CookieValue"),
            cookie_value,
            rules,
            prefer_worth_watching,
            context,
        )


@fail_quietly("Failed to evaluate body")
def _evaluate_body(context, rules, prefer_worth_watching, exclusions):
    if check_url_input_exclusion(exclusions, "BODY", context.request.url):
        return

    body_type = context.request._get_document_type()
    if body_type == DocumentType.JSON:
        _evaluate_body_json(context, rules, prefer_worth_watching, context.request.json)
    elif body_type == DocumentType.XML:
        data = xml.etree.ElementTree.fromstring(context.request.body)
        text_list = [element.text for element in data]

        for text in text_list:
            if not str(text).startswith("\n"):
                _call_agent_lib_evaluate_input(
                    agent_lib.modules.CONSTANTS.InputType.get("XmlValue"),
                    str(text),
                    rules,
                    prefer_worth_watching,
                    context,
                )
    else:
        _evaluate_key_value_parameters(
            context, rules, prefer_worth_watching, querystring=False
        )


def _evaluate_body_json(context, rules, prefer_worth_watching, body):
    # TODO: PYT-2826
    # Using recursion for now to get all the json values and keys and pass them
    # through agent_lib until agent_lib implements parsing of the body for python
    if isinstance(body, dict):
        for key, value in body.items():
            _call_agent_lib_evaluate_input(
                agent_lib.modules.CONSTANTS.InputType.get("JsonKey"),
                key,
                rules,
                prefer_worth_watching,
                context,
            )
            # This check is to skip a level in the recursion, just a minor optimization
            if isinstance(value, (dict, list)):
                _evaluate_body_json(context, rules, prefer_worth_watching, value)
            else:
                _call_agent_lib_evaluate_input(
                    agent_lib.modules.CONSTANTS.InputType.get("JsonValue"),
                    value,
                    rules,
                    prefer_worth_watching,
                    context,
                )
    elif isinstance(body, list):
        for item in body:
            if isinstance(item, (dict, list)):
                _evaluate_body_json(context, rules, prefer_worth_watching, item)
            else:
                _call_agent_lib_evaluate_input(
                    agent_lib.modules.CONSTANTS.InputType.get("JsonValue"),
                    item,
                    rules,
                    prefer_worth_watching,
                    context,
                )
    else:
        # In theory we shouldn't enter this block but I would like to have it
        # just in case we get a value instead of dict
        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("JsonValue"),
            body,
            rules,
            prefer_worth_watching,
            context,
        )


def _evaluate_query_string_params(context, rules, prefer_worth_watching, exclusions):
    """
    Get agent-lib input analysis for all query parameters. This information is stored on
    request context.
    """
    if check_url_input_exclusion(exclusions, "QUERYSTRING", context.request.url):
        return

    _evaluate_key_value_parameters(
        context, rules, prefer_worth_watching, querystring=True
    )


def _evaluate_key_value_parameters(
    context, rules, prefer_worth_watching, *, querystring: bool
) -> None:
    """
    Used for both form parameters (from the request body) and query string parameters
    """
    if querystring:
        param_dict = context.request.GET
    else:
        param_dict = context.request.POST

    for param_key, param_value in param_dict.items():
        if not isinstance(param_value, str):
            continue

        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("ParameterKey"),
            param_key,
            rules,
            prefer_worth_watching,
            context,
            is_querystring=querystring,
        )
        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("ParameterValue"),
            param_value,
            rules,
            prefer_worth_watching,
            context,
            is_querystring=querystring,
        )


def _evaluate_path_params(context, rules, prefer_worth_watching, exclusions):
    """
    Get agent-lib input analysis for all path parameters. This information is
    stored on request context.
    """
    for param in context.request.get_url_parameters():
        if check_param_input_exclusions(exclusions, "PARAMETER", param):
            continue

        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("UrlParameter"),
            param,
            rules,
            prefer_worth_watching,
            context,
        )


def _evaluate_multipart_request(context, rules, prefer_worth_watching):
    """
    This is refering to Content-Type: multipart/form-data and checking the file_name for every
    multipart request if there is none it checks the name
    """
    for key, value in context.request.get_multipart_headers().items():
        if value is None and key is None:
            continue

        multipart_name = value if value is not None else key
        _call_agent_lib_evaluate_input(
            agent_lib.modules.CONSTANTS.InputType.get("MultipartName"),
            multipart_name,
            rules,
            prefer_worth_watching,
            context,
        )


def _call_check_method_tampering(context, prefer_worth_watching):
    input_analysis_value = agent_lib.check_method_tampering(
        context.request.method, prefer_worth_watching
    )

    if input_analysis_value:
        context.user_input_analysis.extend(input_analysis_value)
        _report_and_block_by_rule_list(
            input_analysis_value, ["reflected-xss", "unsafe-file-upload"], context
        )


def _call_agent_lib_evaluate_input(
    input_type,
    input_value,
    rule_set,
    prefer_worth_watching,
    context,
    *,
    is_querystring=False,
):
    input_analysis_value = agent_lib.evaluate_input_by_type(
        input_type, input_value, rule_set, prefer_worth_watching
    )

    if input_analysis_value:
        # This check is specific for querystring because agent-lib doesn't have a way to distinguish
        # url parameter and querystring and TS is expecting it as QUERYSTRING in attack samples
        if is_querystring:
            for input_analysis in input_analysis_value:
                input_analysis.input_type = InputType.QUERYSTRING

        context.user_input_analysis.extend(input_analysis_value)
        _report_and_block_by_rule_list(
            input_analysis_value, ["reflected-xss", "unsafe-file-upload"], context
        )


def _report_and_block_by_rule_list(input_analysis, rule_names, context):
    """
    Checks a list of rules and reports if it finds a score(int with value 0-100 indicating percentage
    of certainty of attack) higher than 90 and blocks if the agent is configured in block mode.
    :param input_analysis: list the response from agent_lib
    :param rule_names: list of names of rules that need to be checked and reported and blocked
    :return: doesn't return anything as it just needs to report and block if needed
    """
    settings = Settings()
    for input_row in input_analysis:
        for rule_name in rule_names:
            rule = settings.protect_rules.get(rule_name)
            # Bot blocker rule is valid only when the input_row.name/header name is "user-agent"
            bot_blocker_header_check = (
                lambda a, rule_name_val: a.lower() == "user-agent"
                if rule_name_val == "bot-blocker"
                else True
            )

            if rule_name == input_row.rule_id:
                attack = rule.build_attack_with_match(input_row.value, input_row, None)
                context.attacks.append(attack)

            if (
                bot_blocker_header_check(input_row.key, rule_name)
                and input_row.score >= 90
                and rule is not None
                and rule_name == input_row.rule_id
            ):
                logger.debug(
                    f"Input analysis found a value '{input_row.value}' "
                    f"that violated {rule_name} rule!"
                )

                if input_row.rule_id == rule.RULE_NAME and rule.is_blocked():
                    rule_message = f"{rule_name} - {ensure_string(input_row.value, errors='replace')}"

                    msg = (
                        f"The {input_row.input_type.name} {input_row.value} "
                        "had a value that successfully exploited "
                        f"{ensure_string(rule_message, errors='replace')}"
                    )

                    security_log_msg(msg, Settings().app_name, rule_name, "EXPLOITED")

                    raise contrast.SecurityException(rule_name=rule_name)


def check_url_input_exclusion(exclusions, input_type, param):
    if not exclusions:
        return False

    return exclusions.evaluate_input_exclusions_url(
        exclusions, input_type, param, "defend"
    )


def check_param_input_exclusions(exclusions, input_type, param):
    if not exclusions:
        return False

    return exclusions.evaluate_input_exclusions(exclusions, input_type, param, "defend")
