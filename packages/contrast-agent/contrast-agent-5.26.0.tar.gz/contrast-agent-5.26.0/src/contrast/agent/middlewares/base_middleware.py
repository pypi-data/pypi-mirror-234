# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import threading

import contrast
from contrast.reporting import teamserver_messages
from contrast.agent import (
    agent_state,
    scope,
    thread_watcher,
)
from contrast.agent.protect import input_analysis
from contrast.agent.request_context import RequestContext
from contrast.agent.assess.rules.response.xss import analyze_xss
from contrast.agent.assess.rules.response.analyze import analyze_response_rules
from contrast.agent.assess.preflight import update_preflight_hashes
from contrast.agent.middlewares.route_coverage.routes_mixin import RoutesMixin
from contrast.api.attack import ProtectResponse
from contrast.utils.decorators import cached_property
from contrast.utils.loggers.logger import (
    setup_basic_agent_logger,
)
from contrast.utils import timer
from contrast.utils.decorators import fail_loudly, fail_quietly

# initialize a basic logger until config is parsed
logger = setup_basic_agent_logger()


class BaseMiddleware(RoutesMixin):
    """
    BaseMiddleware contains all the initial setup for the framework middlewares

    Requirements:

        1. It's callable
        2. It has call_with_agent
        3. It has call_without_agent

    Pre and post filter calls should not block the flow that this class has.

    Pre -> get_response -> post
    """

    # TODO: PYT-2869 this should be removed. This sort of thing is agent_state's job.
    _loaded = False

    # TODO: PYT-2852 Revisit application name detection
    app_name = ""  # This should be overridden by child classes

    DIAGNOSTIC_ENDPOINT = "/save-contrast-security-config"
    DIAGNOSTIC_ALLOWED_SERVER = "localhost"
    DIAGNOSTIC_ALLOWED_IP = "127.0.0.1"

    @scope.with_contrast_scope
    def __init__(self):
        """
        Most agent initialization is now done by the agent state module

        This method calls agent state initialization if it hasn't been done
        already and then loads the settings and reporting client.

        Config scanning still happens here since the behavior is framework-specific.
        """
        # id will be different across processes but also for multiple middlewares
        # within the same process
        self.id = id(self)
        self.settings = None
        self.request_start_time = None
        self.request_path = None

        if BaseMiddleware._loaded:
            logger.warning(
                "Contrast Agent middleware initialized more than once per process."
            )

        agent_state.initialize()

        self.settings = agent_state.get_settings()
        if not self.is_agent_enabled():
            return

        self.reporting_client = agent_state.get_reporting_client()

        if self.settings.is_assess_enabled() and not BaseMiddleware._loaded:
            BaseMiddleware._loaded = True
            self.scan_configs_in_thread()

        BaseMiddleware._loaded = True

    @cached_property
    def name(self):
        raise NotImplementedError("Must implement name")

    def is_agent_enabled(self):
        """
        Agent is considered enabled if the config value for 'enable' is True (or empty,
        defaults to True). Errors during initialization or runtime will set this value
        to False.
        """
        if self.settings is None:
            return False

        if not self.settings.is_agent_config_enabled():
            return False

        return True

    def call_with_agent(self, *args):
        raise NotImplementedError("Must implement call_with_agent")

    def call_without_agent(self, *args):
        """
        The agent does not set context when this function is called so all other patches
        (e.g propagators) that check context shouldn't run.
        """
        logger.debug("Contrast Agent did not analyze request %s", self.request_path)

    def should_analyze_request(self, environ):
        """
        Determine if request should be analyzed based on configured settings.

        While returning different types of objects based on logic is not a good
        pattern, in this case it's an optimization that allows us to create
        the request context obj when we need it.

        :return: False or RequestContext instance
        """
        if not self.is_agent_enabled():
            logger.debug("Will not analyze request: agent disabled.")
            return False

        context = RequestContext(environ)

        path = environ.get("PATH_INFO")

        if self.settings.evaluate_exclusions(context, path):
            logger.debug("Will not analyze request: request meets exclusions.")
            return False

        from contrast.agent.assess import sampling

        if sampling.enabled() and sampling.meets_criteria(context):
            logger.debug("Will not analyze request: request meets sampling.")
            return False

        return context  # equivalent to returning True

    @fail_loudly("Unable to do handle_ensure")
    def handle_ensure(self, context, request):
        """
        Method that should run for all middlewares AFTER every request is made.
        """
        if context is None:
            logger.error("Context not defined in middleware ensure")
            return

        with scope.contrast_scope():
            thread_watcher.ensure_running(self)

            if self.settings.is_assess_enabled():
                # route discovery and storage needs to occur before sending messages
                self.handle_routes(context, request)

                logger.debug("Updating preflight hashes with route info")
                update_preflight_hashes(context)

            logger.debug("Sending final messages for reporting.")

            for msg in self.final_ts_messages(context):
                self.reporting_client.add_message(msg)

        agent_state.set_first_request(False)

    def final_ts_messages(self, context):
        if context is None:
            return []

        messages = [
            teamserver_messages.ApplicationActivity(context),
        ]

        if (
            self.settings.is_assess_enabled()
            and context.findings is not None
            and len(context.findings) > 0
        ):
            messages.append(
                teamserver_messages.Preflight(context.findings, context.request)
            )

        # Per the spec, we do not report an observed route if the route signature or URL is empty.
        if (
            self.settings.is_assess_enabled()
            and context.observed_route.signature
            and context.observed_route.url
        ):
            messages.append(teamserver_messages.ObservedRoute(context.observed_route))

        # ApplicationUpdate message only sent at first request once we have routes
        if agent_state.is_first_request() and self.settings.is_inventory_enabled():
            messages.append(
                teamserver_messages.ApplicationInventory(agent_state.get_routes())
            )

        # Not every request will have a new dependency loaded, so we can skip sending empty messages.
        if context.observed_library_usage is not None:
            messages.append(context.observed_library_usage)

        return messages

    @fail_loudly("Unable to do prefilter protect")
    def prefilter(self):
        """
        Prefilter - AKA input analysis - is performed mostly with agent-lib but partly
        in the agent.

        This is PROTECT only.

        In this method we call on agent-lib to do input analysis, which can result in:
        1. agent-lib finds an attack in which case we block the request
        2. agent-lib returns input analysis to use for later sink / infilter analysis,
            in which case we store it here in the request context.
        """
        if not self.settings.is_protect_enabled():
            return

        input_analysis.get_input_analysis(prefer_worth_watching=True)
        self.agent_prefilter()

    def agent_prefilter(self):
        """
        Prefilter for any rules that do not yet use agent-lib
        """
        with scope.contrast_scope():
            self.prefilter_protect()

    @fail_quietly("Failed to run prefilter protect.")
    def prefilter_protect(self):
        logger.debug("PROTECT: Running Agent prefilter.")

        for rule in self.settings.protect_rules.values():
            if rule.is_prefilter():
                rule.prefilter()

    @fail_loudly("Unable to do postfilter")
    def postfilter(self, context):
        """
        For all postfilter enabled rules.
        """
        if self.settings.is_protect_enabled():
            self.postfilter_protect(context)

        if self.settings.is_assess_enabled():
            with scope.contrast_scope():
                self.response_analysis(context)

    def _process_trigger_handler(self, handler):
        """
        Gather metadata about response handler callback for xss trigger node

        We need to check whether the response handler callback is an instance method or
        not. This affects the way that our policy machinery works, and it also affects
        reporting, so we need to make sure to account for the possibility that handler
        is a method of some class rather than a standalone function.

        This should be called by the `trigger_node` method in child classes.
        """
        module = handler.__module__
        class_name = ""

        if hasattr(handler, "__self__"):
            class_name = handler.__self__.__class__.__name__
            args = (handler.__self__,)
            instance_method = True
        else:
            args = ()
            instance_method = False

        return module, class_name, args, instance_method

    @cached_property
    def trigger_node(self):
        """
        Trigger node property used by assess reflected xss postfilter rule

        This must be overridden by child classes that make use of the reflected
        xss postfilter rule.
        """
        raise NotImplementedError("Children must define trigger_node property")

    @fail_loudly("Unable to do assess response analysis")
    def response_analysis(self, context):
        """
        Run postfilter for any assess rules. Reflected xss rule runs by default.
        May be overridden in child classes.

        If the response content type matches a allowed content type, do not run
        assess xss response analysis. This is because the security team
        considers reflected xss within these content types to be a false positive.
        """
        logger.debug("ASSESS: Running response analysis")

        analyze_xss(context, self.trigger_node)

        if not self.settings.response_scanning_enabled:
            return

        analyze_response_rules(context)

    @fail_quietly("Failed to run postfilter protect.")
    def postfilter_protect(self, context):
        logger.debug("PROTECT: Running Agent postfilter.")

        input_analysis.get_input_analysis(prefer_worth_watching=False)

        for rule in self.settings.protect_rules.values():
            if rule.is_postfilter():
                rule.postfilter()

    @fail_loudly("Unable to do check_for_blocked")
    def check_for_blocked(self, context: RequestContext):
        """
        Checks for BLOCK events in case SecurityException was caught by app code

        This should be called by each middleware after the view is generated
        but before returning the response (it can be before or after
        postfilter).

        If we make it to this call, it implies that either no SecurityException
        occurred, or if one did occur, it was caught by the application. If we
        find a BLOCK here, it necessarily implies that an attack was detected
        in the application, but the application caught our exception. If the
        application hadn't caught our exception, we never would have made it
        this far because the exception would have already bubbled up to the
        middleware exception handler. So this is really our first and our last
        opportunity to check for this particular edge case.
        """
        for attack in context.attacks:
            if attack.response == ProtectResponse.BLOCKED:
                raise contrast.SecurityException(rule_name=attack.rule_id)

    def log_start_request_analysis(self):
        self.request_start_time = timer.now_ms_float()

        logger.debug("Beginning request analysis", request_path=self.request_path)

    @fail_loudly("Unable to do log_end_request_analysis")
    def log_end_request_analysis(self):
        request_end_time = timer.now_ms_float()

        logger.debug(
            "Ending request analysis",
            request_path=self.request_path,
        )

        elapsed_time = request_end_time - self.request_start_time

        logger.debug(
            "elapsed time request analysis ms",
            elapsed_time=elapsed_time,
            request_path=self.request_path,
        )

    def scan_configs_in_thread(self):
        """
        Run config scanning rules for assess in a separate thread.

        Not all frameworks we support will necessarily have config scanning rules.
        These frameworks should not start a thread.
        """
        if hasattr(self, "_scan_configs"):
            logger.debug("Will start a thread to scan config rules.")
            scanner = threading.Thread(target=self._scan_configs)
            scanner.daemon = True
            scanner.start()
        else:
            logger.debug(f"No config scanning rules for {self.__class__.__name__}")
