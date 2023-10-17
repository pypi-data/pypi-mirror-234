# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import re


from enum import Enum, auto

from contrast.utils.decorators import fail_loudly
from contrast.api import TypeCheckedProperty


from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class ExclusionType(Enum):
    URL_EXCLUSION_TYPE = auto()
    INPUT_EXCLUSION_TYPE = auto()


class InputExclusionSourceType(Enum):
    COOKIE = auto()
    PARAMETER = auto()
    HEADER = auto()
    BODY = auto()
    QUERYSTRING = auto()
    UNKNOWN = auto()


class TsExclusion:
    type = TypeCheckedProperty(
        ExclusionType, constructor_arg=ExclusionType.URL_EXCLUSION_TYPE
    )
    input_type = TypeCheckedProperty(
        InputExclusionSourceType, constructor_arg=InputExclusionSourceType.UNKNOWN
    )

    def __init__(
        self,
        exclusion_type,
        name,
        modes,
        match_strategy,
        protection_rules,
        assessment_rules,
        urls=None,
        input_type=None,
        input_name=None,
    ):
        self.type = exclusion_type
        self.name = name
        self.modes = modes
        self.match_strategy = match_strategy
        self.protection_rules = protection_rules
        self.assessment_rules = assessment_rules
        self.urls = urls
        self.input_type = getattr(
            InputExclusionSourceType, input_type or "", InputExclusionSourceType.UNKNOWN
        )
        self.input_name = input_name


def strs_to_regexes(patterns, ignorecase=0):
    """

    :param patterns: list of strings
    :return: list of regular expressions
    """
    if not patterns:
        return []

    regexes = []

    for pattern in patterns:
        try:
            pat = re.compile(pattern, flags=ignorecase)
            regexes.append(pat)
        except Exception as ex:
            logger.warning("Unable to parse pattern %s: %s", pattern, ex)

    return regexes


class Exclusions:
    """
    Container for all exclusions
    """

    @staticmethod
    def init_input_exclusions_container():
        input_exclusions = dict(
            HEADER=[], HEADER_KEY=[], PARAMETER=[], COOKIE=[], BODY=[], QUERYSTRING=[]
        )

        # Aliases for the same source type
        input_exclusions["HEADER"] = input_exclusions["HEADER_KEY"]
        input_exclusions["MULTIPART_FORM_DATA"] = input_exclusions["BODY"]
        input_exclusions["MULTIPART_CONTENT_DATA"] = input_exclusions["BODY"]

        return input_exclusions

    def __init__(self, exclusions):
        self.input_exclusions = self.init_input_exclusions_container()
        self.url_exclusions = []

        has_named_exclusion = False

        for exc in exclusions:
            if exc.type == ExclusionType.INPUT_EXCLUSION_TYPE:
                self.input_exclusions[exc.input_type.name].append(InputExclusion(exc))
                has_named_exclusion = True
            else:
                self.url_exclusions.append(UrlExclusion(exc))

        if not has_named_exclusion:
            self.input_exclusions = None

    def evaluate_assess_trigger_time_exclusions(self, context, finding):
        # returns True if we do not report finding
        if not context.input_exclusions_trigger_time:
            return False

        for exc in context.input_exclusions_trigger_time:
            if exc.match_in_finding(finding):
                return True

        return False

    def evaluate_input_exclusions(self, context, source_type, source_name, mode=None):
        # Evaluate all exclusions against the current source
        if context.input_exclusions is None:
            return False

        exclusions = context.input_exclusions.get(source_type, None)
        if exclusions is None:
            return False

        for exc in exclusions:
            if mode and mode not in exc.modes:
                continue

            if exc.match(
                context,
                source_type=source_type,
                source_name=source_name,
            ):
                logger.debug(
                    "The input exclusion rule named '%s' matched on the input name '%s' for the input type of '%s'",
                    exc.exclusion_name,
                    source_name,
                    exc.input_type,
                )
                return True

        return False

    def evaluate_input_exclusions_url(self, context, source_type, path, mode=None):
        # Evaluate all exclusions against the current source
        if context.input_exclusions is None:
            return False

        exclusions = context.input_exclusions.get(source_type, None)
        if exclusions is None:
            return False

        for exc in exclusions:
            if mode and mode not in exc.modes:
                continue

            if exc.match_type == "ALL":
                logger.debug(
                    "The input url exclusion rule named '%s' matched on the path '%s' for the input type of '%s'",
                    exc.exclusion_name,
                    path,
                    exc.input_type,
                )
                return True

            for url_regex in exc.url_regexes:
                if url_regex.search(path):
                    logger.debug(
                        "The input url exclusion rule named '%s' matched on the path '%s' for the input type of '%s'",
                        exc.exclusion_name,
                        path,
                        exc.input_type,
                    )
                    return True

        return False

    def evaluate_url_exclusions(self, context, target):
        """
        This function evaluates all exclusions depending on the request URL and updates the request context to contain
        the list of disabled assess and protect rules to be evaluated at trigger time for url exclusions

        @param context: request context we are evaluating exclusions in
        @param target: The target string to be matched against
        @type target:
        @return: boolean indicating whether or not request should not be analyzed
        @rtype: bool
        """
        has_match = False

        for exc in self.url_exclusions:
            if exc.match(context, target):
                has_match = True

        if has_match:
            from contrast.agent.settings import Settings

            if Settings().is_assess_enabled() and context.excluded_assess_rules is None:
                return True

            if (
                Settings().is_protect_enabled()
                and context.excluded_protect_rules is None
            ):
                return True

        return False

    def set_input_exclusions_by_url(self, context, path):
        """
        Evaluates the set of input exclusions that apply to this path. Update request
        context with input exclusions to apply
        """
        context.input_exclusions = self.init_input_exclusions_container()
        context.input_exclusions_trigger_time = []

        has_match = False

        # pylint: disable=too-many-nested-blocks
        for input_type, exclusions in self.input_exclusions.items():
            for exc in exclusions:
                if exc.url_regexes:
                    for pattern in exc.url_regexes:
                        if pattern.fullmatch(path):
                            has_match = True

                            if exc.protect_rules or exc.assess_rules:
                                context.input_exclusions_trigger_time.append(exc)
                            else:
                                context.input_exclusions[input_type].append(exc)

                            logger.debug(
                                "Path %s matched on input exclusion pattern %s",
                                path,
                                pattern,
                            )

                else:
                    if exc.protect_rules or exc.assess_rules:
                        context.input_exclusions_trigger_time.append(exc)
                    else:
                        context.input_exclusions[input_type].append(exc)

                    has_match = True

        if not has_match:
            # No exclusions for this request
            context.input_exclusions = None


class BaseExclusion:
    def __init__(self, exclusion):
        self.protect_rules = None
        self.assess_rules = None
        self.url_regexes = []
        self.exclusion_name = exclusion.name

        if exclusion.urls:
            self.url_regexes = strs_to_regexes(exclusion.urls)

        self.protect_rules = exclusion.protection_rules
        self.assess_rules = exclusion.assessment_rules

        # TODO: PYT-2613 remove?
        # old comment:
        # This will add the needed match strategy for direct TS requests and leave it compatible with SR
        if hasattr(exclusion, "match_strategy"):
            self.match_type = exclusion.match_strategy
        if hasattr(exclusion, "modes"):
            self.modes = exclusion.modes

    def match(self, context, **kwargs):
        raise NotImplementedError


class InputExclusion(BaseExclusion):
    def __init__(self, exclusion):
        super().__init__(exclusion)

        self.input_name_regex = None

        self.input_type = exclusion.input_type

        if self.input_type == InputExclusionSourceType.UNKNOWN:
            logger.error("Invalid input exclusion type for the exclusion %s", exclusion)

        if exclusion.input_name:
            # Adding a check for type cookie to ignore case as per requirements
            # https://github.com/Contrast-Security-Inc/platform-specifications/blob/main/exclusions/EXCLUSIONS_INPUT.md
            if exclusion.input_type == InputExclusionSourceType.COOKIE:
                self.input_name_regex = strs_to_regexes(
                    [exclusion.input_name], re.IGNORECASE
                )[0]
            else:
                self.input_name_regex = strs_to_regexes([exclusion.input_name])[0]

    def is_body_input_type(self, source_type):
        return self.input_type == InputExclusionSourceType.BODY or source_type in [
            "BODY",
            "MULTIPART_FORM_DATA",
            "MULTIPART_CONTENT_DATA",
        ]

    def is_querystring_input_type(self, source_type):
        return (
            self.input_type == InputExclusionSourceType.QUERYSTRING
            or source_type == "QUERYSTRING"
        )

    def match_in_finding(self, finding):
        creation_action = 0

        # pylint: disable=too-many-nested-blocks
        if finding.rule_id in self.assess_rules:
            for event in finding.events:
                if event.action == creation_action:
                    for trace_event in event.event_sources:
                        event_type = trace_event.type
                        event_src_name = trace_event.name

                        if event_type == self.input_type.name:
                            exclude = False

                            if (
                                self.input_name_regex is not None
                                and self.input_name_regex.fullmatch(event_src_name)
                            ):
                                exclude = True

                            if self.input_type in [
                                InputExclusionSourceType.QUERYSTRING,
                                InputExclusionSourceType.BODY,
                            ]:
                                exclude = True

                            if exclude:
                                logger.debug(
                                    "The input exclusion rule named '%s' matched on the input name '%s' for the input type of '%s' for the rule '%s'",
                                    self.exclusion_name,
                                    event_src_name,
                                    event_type,
                                    finding.rule_id,
                                )
                                return exclude

        return False

    def match(self, context, source_type=None, source_name=None):
        if source_name is None and self.input_type not in [
            InputExclusionSourceType.QUERYSTRING,
            InputExclusionSourceType.BODY,
        ]:
            return False

        if self.is_body_input_type(source_type) or self.is_querystring_input_type(
            source_type
        ):
            return True

        return self.input_name_regex.fullmatch(source_name) is not None


class UrlExclusion(BaseExclusion):
    @fail_loudly("Unable to ignore request", return_value=False)
    def match(self, context, path=None):
        """
        Determine if the given path exactly matches any of the
        configured urls for this exclusion rule. This function modifies the
        request context to notify rules if they should be disabled for this url.

        @param context: request context
        @param path: path for current request
        @return This function returns True if a match was found
        @rtype: bool
        """
        has_match = False

        if path is None:
            return False

        for pattern in self.url_regexes:
            if pattern.fullmatch(path):
                logger.debug("Path %s matched on pattern %s", path, pattern)

                self.update_disabled_rules(context)

                has_match = True

        return has_match

    def update_disabled_rules(self, request_ctx):
        if request_ctx is not None:
            # The spec states that if either assess_rules or protect_rules is None
            # we ignore the full request so set the disabled rules to None to ignore everything
            if request_ctx.excluded_assess_rules is not None and self.assess_rules:
                request_ctx.excluded_assess_rules.extend(self.assess_rules)
            elif not self.assess_rules:
                request_ctx.excluded_assess_rules = None

            if request_ctx.excluded_protect_rules is not None and self.protect_rules:
                request_ctx.excluded_protect_rules.extend(self.protect_rules)
            elif not self.protect_rules:
                request_ctx.excluded_protect_rules = None
