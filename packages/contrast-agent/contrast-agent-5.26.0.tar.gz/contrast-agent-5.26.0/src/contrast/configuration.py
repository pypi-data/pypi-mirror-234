# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import re
from collections import namedtuple
import os

from contrast import AGENT_CURR_WORKING_DIR
import contrast.utils.configuration_utils as utils

from contrast.utils.decorators import cached_property
from contrast.utils.loggers import (
    DEFAULT_PROGNAME,
    DEFAULT_SECURITY_LOG_PATH,
    DEFAULT_SECURITY_LOG_LEVEL,
)
from contrast_vendor import structlog as logging
from contrast.utils.singleton import Singleton

logger = logging.getLogger("contrast")

SPLIT_CWD = AGENT_CURR_WORKING_DIR.split(os.sep)
APP_NAME = SPLIT_CWD[len(SPLIT_CWD) - 1]
ENV_PREFIX = "CONTRAST"


DEFAULT_TEAMSERVER_TYPE = "EOP"
PUBLIC_SASS_TEAMSERVER_TYPES = {
    "app.contrastsecurity.com": "SAAS_DEFAULT",
    "eval.contrastsecurity.com": "SAAS_POV",
    "ce.contrastsecurity.com": "SAAS_CE",
    "app.contrastsecurity.jp": "SAAS_TOKYO",
    "cs": "SAAS_",
}

PRIVATE_SASS_TEAMSERVER_TYPE = "SAAS_CUSTOM"
PRIVATE_SASS_DOMAIN = ["contrastsecurity.com", "contrastsecurity.jp"]

TESTING_TEAMSERVER_TYPE = "TESTING"
TESTING_TEAMSERVER_NAMES = [
    "darpa",
    "alpha.contrastsecurity.com",
    "apptwo.contrastsecurity.com",
    "teamserver-staging.contsec.jp",
    "teamserver-staging.contsec.com",
    "security-research.contrastsecurity.com",
    "teamserver-ops.contsec.com",
]


ConfigOption = namedtuple(
    "ConfigOption", ["canonical_name", "default_value", "type_cast"]
)
ConfigOptionSrc = namedtuple("ConfigOptionSrc", ["name", "source"])

ENVIRONMENT_VARIABLE_SRC = "ENVIRONMENT_VARIABLE"
USER_CONFIGURATION_FILE_SRC = "USER_CONFIGURATION_FILE"
DEFAULT_VALUE_SRC = "DEFAULT_VALUE"
CONTRAST_UI_SRC = "CONTRAST_UI"
ASSESS_DISABLED_RULE_CONFIG_KEY = "assess.rules.disabled_rules"


class AgentConfig(object):
    def __init__(self):
        self.yaml_filename = None
        self.config_status = None
        self._config_source = {}
        self._config = utils.load_yaml_config()

        if not self._config:
            logger.info("No YAML config found; using default settings")
            self._config = {}

        self.yaml_filename = self._config.get("loaded_configuration_filename", None)
        if self.yaml_filename is not None:
            del self._config["loaded_configuration_filename"]

        self._config = utils.flatten_config(self._config)

        self.override_configs()

        self.check_for_api_config()

        # This stores the session ID sent from TS. We have to separate this value from the value set in the yaml config
        # because the value sent from TS always takes precedence. This value is only sent from TS
        # in response to ApplicationStartup
        self._ts_session_id = None

    def get_src(self, key, default_value=None):
        return self._config_source.get(key, default_value)

    def get(self, key, default_value=None):
        return self._config.get(key, default_value)

    def put(self, key, value, src=None):
        if not key or key not in self._config:
            return

        if src is not None:
            self._config_source[key] = src

        self._config[key] = value

    def get_redacted_config(self):
        """
        The purpose of this function is to return a copy of the config with redacted values
        """
        sensitive_keys = [
            "api.service_key",
            "api.user_name",
            "api.api_key",
            "api.proxy.url",
        ]

        redacted_config = self._config.copy()
        for key in sensitive_keys:
            if redacted_config[key]:
                redacted_config[key] = "**REDACTED**"

        return redacted_config

    def log_config(self):
        """
        Log configuration values.

        Config values deemed sensitive are logged as **REDACTED** unless unassigned.
        """
        redacted_config = self.get_redacted_config()

        logger.info("Current Configuration", **redacted_config)

    def _validate_agent_config(self):
        """
        At this point in configuration initialization every item in self._config should have an
        associated source in self._config_source (e.g set by DEFAULT VALUE or ENVIRONMENT VARIABLE)

        If it does not have a source than the assumption is made that the key does not have an entry in
        any of the default_options set in each of the top level configs.

        If that is the case this is either: A new configuration option that should be
        added to default_options OR a misconfiguration by the user
        """
        for k in self._config.keys():
            if self._config_source.get(k, None) is None:
                if self.config_status is None:
                    self.config_status = f"Invalid {self._config[k]} on {k}"
                    return

    def override_configs(self):
        """
        For each class representing different parts of the config (Agent, etc),
        take the current config and apply any overriding logic such as overriding with
        environment keys/values.

        At this time the order of precedence is:
            os.env > Config yaml

        Meaning that a config value defined in os.environ must be used instead of
        the same config defined in contrast_security.yaml

        Note that CLI args (sys.argv) are not supported. This may change if the
        agent becomes a runner.
        """
        builders = [Api, Agent, Application, Assess, Inventory, Protect, Root, Server]

        for builder in builders:
            status = builder().build(self._config, self._config_source)
            if status:
                # An error here indicates a failure with the type cast of the value
                self.config_status = status
                return

        self._validate_agent_config()

    def check_for_api_config(self):
        """
        Validate api configurations were set.

        If any api configs are missing, log at ERROR and disable the agent.

        Returns the missing values or an empty list if none were missing.
        """

        api_keys = [
            "api.url",
            "api.service_key",
            "api.api_key",
            "api.user_name",
        ]

        missing_values = []
        for key in api_keys:
            val = self.get(key)
            if not val:
                missing_values.append(key)

        if missing_values:
            msg = (
                f"Missing a required connection value for: {', '.join(missing_values)}"
            )
            logger.error(msg)
            self.put("enable", False)

        return missing_values

    @property
    def session_id(self):
        return (
            self._ts_session_id
            if self._ts_session_id is not None
            else self.get("application.session_id", "")
        )

    @session_id.setter
    def session_id(self, session_id):
        self._ts_session_id = session_id
        self._config_source["application.session_id"] = ConfigOptionSrc(
            name="contrast.application.session_id", source=CONTRAST_UI_SRC
        )
        logger.debug("Set session_id to %s", session_id, direct_to_teamserver=1)

    def get_session_metadata(self):
        return self.get("application.session_metadata", "")

    @property
    def app_code(self):
        return self.get("application.code", "")

    @property
    def app_metadata(self):
        return self.get("application.metadata", "")

    @property
    def app_group(self):
        return self.get("application.group", "")

    @property
    def app_tags(self):
        return self.get("application.tags", "")

    @property
    def assess_tags(self):
        return self.get("assess.tags", "")

    @cached_property
    def is_request_audit_enabled(self):
        return self.get("api.request_audit.enable")

    @cached_property
    def assess_enabled(self):
        return self.get("assess.enable")

    @cached_property
    def should_rewrite(self):
        return self.assess_enabled and self.get("agent.python.rewrite")

    @cached_property
    def should_apply_policy_rewrites(self):
        return self.should_rewrite and self.get("agent.python.enable_policy_rewrites")

    @cached_property
    def enable_automatic_middleware(self) -> bool:
        return self.get("agent.python.enable_automatic_middleware", True)

    @cached_property
    def application_activity_polling_interval(self):
        return self.get("agent.polling.app_activity_ms", 30_000)

    @cached_property
    def server_settings_poll_interval(self):
        return self.get("agent.polling.server_settings_ms", 30_000)

    @cached_property
    def teamserver_type(self):
        url = self.get("api.url")

        if url is None:
            return ""

        for name, ts_type in PUBLIC_SASS_TEAMSERVER_TYPES.items():
            if name in url:
                # This regex matches https://cs001.contrastsecurity.com
                r_url = re.match(r".*(cs\d{3})\..*", url)
                if r_url:
                    # and gets the second group which is the matched in brackets cs001
                    # adds it to the SAAS_ type and becomes SAAS_CS001
                    numbers = r_url.group(1).upper()

                    return ts_type + numbers

                return ts_type

        for name in TESTING_TEAMSERVER_NAMES:
            if name in url:
                return TESTING_TEAMSERVER_TYPE

        for name in PRIVATE_SASS_DOMAIN:
            if name in url:
                return PRIVATE_SASS_TEAMSERVER_TYPE

        return DEFAULT_TEAMSERVER_TYPE


class ConfigBuilder(object):
    TOP_LEVEL = ""

    def __init__(self):
        self.default_options = []

    def build(self, config, config_src):
        """
        Given a dict config, iterate over the default_options and check if
        the corresponding config key/value should be either :
        1. replaced by an existing env var
        2. keep existing config key/val but type-cast the value
        3. add a new key/default_value to the config

        :param config: dict config
        :param config_src: dict where each config option is a key that maps to a ConfigOptionSrc
        :return: str if error was set, config dict is updated pass by reference
        """
        sampling_lock_config = None
        if isinstance(self, Assess):
            sampling_lock_config = SamplingLockConfig()

        for option_name, default_val, type_cast in self.default_options:
            dot_alt = self._dot_alternative(option_name)
            underscore_alt = self._underscore_alternative(option_name)

            env_override = utils.get_env_key(underscore_alt)
            if env_override:
                try:
                    # replace the config value with the os.env value and apply type-cast
                    env_override = type_cast(env_override)
                except Exception as e:
                    logger.exception("Failed to initialize config")
                    return f"Invalid value on {dot_alt} - {e}"

                config[dot_alt] = env_override
                config_src[dot_alt] = ConfigOptionSrc(
                    name=underscore_alt, source=ENVIRONMENT_VARIABLE_SRC
                )
                continue

            if "sampling" in option_name and config.get(dot_alt):
                sampling_lock_config.set_sampling_config(option_name.split(".")[-1])

            if dot_alt in config:
                # update the config value with a type-cast value
                val = config[dot_alt]

                try:
                    val = type_cast(val)
                except Exception as e:
                    logger.exception("Failed to initialize config")
                    return f"Invalid value on {dot_alt} - {e}"

                config[dot_alt] = val
                config_src[dot_alt] = ConfigOptionSrc(
                    name=dot_alt, source=USER_CONFIGURATION_FILE_SRC
                )
                continue

            # add a new key/default_value to config
            config[dot_alt] = default_val
            config_src[dot_alt] = ConfigOptionSrc(
                name=dot_alt, source=DEFAULT_VALUE_SRC
            )

        return None

    def _underscore_alternative(self, key):
        return "__".join(
            [x for x in [ENV_PREFIX, self.TOP_LEVEL, key.replace(".", "__")] if x]
        ).upper()

    def _dot_alternative(self, key):
        return ".".join([self.TOP_LEVEL, key]) if self.TOP_LEVEL else key


class Agent(ConfigBuilder):
    TOP_LEVEL = "agent"

    def __init__(self):
        super().__init__()

        self.default_options = [
            # Some logger default values are handled by the logger
            ConfigOption(
                canonical_name="logger.level",
                default_value="",
                type_cast=str,
            ),
            ConfigOption(canonical_name="logger.path", default_value="", type_cast=str),
            ConfigOption(
                canonical_name="logger.progname",
                default_value=DEFAULT_PROGNAME,
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="security_logger.path",
                default_value=DEFAULT_SECURITY_LOG_PATH,
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="security_logger.level",
                default_value=DEFAULT_SECURITY_LOG_LEVEL,
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="python.rewrite",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="python.disable_policy_rewrites",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="python.enable_automatic_middleware",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="python.enable_drf_response_analysis",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="python.enable_rep",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="python.enable_profiler",
                default_value=False,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="python.assess.use_pure_python_hooks",
                default_value=False,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="polling.app_activity_ms",
                default_value=30000,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="polling.server_settings_ms",
                default_value=30_000,
                type_cast=int,
            ),
        ]


class Api(ConfigBuilder):
    TOP_LEVEL = "api"

    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(canonical_name="url", default_value="", type_cast=str),
            ConfigOption(canonical_name="service_key", default_value="", type_cast=str),
            ConfigOption(canonical_name="api_key", default_value="", type_cast=str),
            ConfigOption(canonical_name="user_name", default_value="", type_cast=str),
            ConfigOption(
                canonical_name="request_audit.enable",
                default_value=False,
                type_cast=bool,
            ),
            ConfigOption(
                canonical_name="request_audit.path",
                default_value=AGENT_CURR_WORKING_DIR,
                type_cast=str,
            ),
            ConfigOption(
                canonical_name="request_audit.requests",
                default_value=False,
                type_cast=bool,
            ),
            ConfigOption(
                canonical_name="request_audit.responses",
                default_value=False,
                type_cast=bool,
            ),
            ConfigOption(
                canonical_name="certificate.enable", default_value=False, type_cast=bool
            ),
            ConfigOption(
                canonical_name="certificate.ignore_cert_errors",
                default_value=False,
                type_cast=bool,
            ),
            ConfigOption(
                canonical_name="certificate.ca_file", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="certificate.cert_file", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="certificate.key_file", default_value="", type_cast=str
            ),
            ConfigOption(
                canonical_name="proxy.enable", default_value=False, type_cast=bool
            ),
            ConfigOption(canonical_name="proxy.url", default_value="", type_cast=str),
        ]


class Application(ConfigBuilder):
    TOP_LEVEL = "application"

    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(canonical_name="code", default_value="", type_cast=str),
            ConfigOption(canonical_name="group", default_value="", type_cast=str),
            ConfigOption(canonical_name="metadata", default_value="", type_cast=str),
            ConfigOption(
                # TODO: PYT-2852 Revisit application name detection
                canonical_name="name",
                default_value=os.path.basename(AGENT_CURR_WORKING_DIR),
                type_cast=str,
            ),
            ConfigOption(canonical_name="path", default_value="", type_cast=str),
            ConfigOption(canonical_name="tags", default_value="", type_cast=str),
            ConfigOption(canonical_name="version", default_value="", type_cast=str),
            ConfigOption(canonical_name="session_id", default_value="", type_cast=str),
            ConfigOption(
                canonical_name="session_metadata", default_value="", type_cast=str
            ),
        ]


class Assess(ConfigBuilder):
    TOP_LEVEL = "assess"

    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="enable", default_value=None, type_cast=utils.str_to_bool
            ),
            ConfigOption(
                canonical_name="enable_scan_response",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="sampling.enable",
                default_value=False,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="sampling.baseline", default_value=5, type_cast=int
            ),
            ConfigOption(
                canonical_name="sampling.request_frequency",
                default_value=10,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="sampling.window_ms",
                default_value=180_000,
                type_cast=int,
            ),
            ConfigOption(canonical_name="tags", default_value="", type_cast=str),
            ConfigOption(
                canonical_name="rules.disabled_rules",
                default_value=[],
                type_cast=utils.parse_disabled_rules,
            ),
            ConfigOption(
                canonical_name="stacktraces",
                default_value="ALL",
                type_cast=utils.parse_stacktraces_options,
            ),
            ConfigOption(
                canonical_name="max_context_source_events",
                default_value=100,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="max_propagation_events",
                default_value=1000,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="time_limit_threshold",
                default_value=300000,  # 5 minutes in ms
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="max_rule_reported",
                default_value=100,
                type_cast=int,
            ),
        ]


class Inventory(ConfigBuilder):
    TOP_LEVEL = "inventory"

    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="analyze_libraries",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="enable", default_value=True, type_cast=utils.str_to_bool
            ),
            ConfigOption(canonical_name="tags", default_value="", type_cast=str),
        ]


class Protect(ConfigBuilder):
    TOP_LEVEL = "protect"

    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="enable", default_value=None, type_cast=utils.str_to_bool
            ),
            ConfigOption(
                canonical_name="samples.probed", default_value=50, type_cast=int
            ),
            ConfigOption(
                canonical_name="samples.blocked", default_value=25, type_cast=int
            ),
            ConfigOption(
                canonical_name="samples.exploited", default_value=100, type_cast=int
            ),
            ConfigOption(
                canonical_name="samples.blocked_at_perimeter",
                default_value=25,
                type_cast=int,
            ),
            ConfigOption(
                canonical_name="rules.bot-blocker.enable",
                default_value=False,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="rules.cmd-injection.detect_chained_commands",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="rules.cmd-injection.detect_parameter_command_backdoors",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="rules.cmd-injection.mode",
                default_value=None,
                type_cast=utils.str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="rules.disabled_rules",
                default_value=[],
                type_cast=utils.parse_disabled_rules,
            ),
            ConfigOption(
                canonical_name="rules.method-tampering.mode",
                default_value=None,
                type_cast=utils.str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="rules.nosql-injection.mode",
                default_value=None,
                type_cast=utils.str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="rules.path-traversal.detect_common_file_exploits",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="rules.path-traversal.detect_custom_code_accessing_system_files",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="rules.path-traversal.mode",
                default_value=None,
                type_cast=utils.str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="rules.reflected-xss.mode",
                default_value=None,
                type_cast=utils.str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="rules.sql-injection.detect_chained_queries",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="rules.sql-injection.detect_dangerous_functions",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="rules.sql-injection.detect_suspicious_unions",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="rules.sql-injection.detect_tautologies",
                default_value=True,
                type_cast=utils.str_to_bool,
            ),
            ConfigOption(
                canonical_name="rules.sql-injection.mode",
                default_value=None,
                type_cast=utils.str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="rules.ssrf.mode",
                default_value=None,
                type_cast=utils.str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="rules.unsafe-file-upload.mode",
                default_value=None,
                type_cast=utils.str_to_protect_mode_enum,
            ),
            ConfigOption(
                canonical_name="rules.xxe.mode",
                default_value=None,
                type_cast=utils.str_to_protect_mode_enum,
            ),
        ]


class Server(ConfigBuilder):
    TOP_LEVEL = "server"

    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="name", default_value=utils.get_hostname(), type_cast=str
            ),
            ConfigOption(canonical_name="path", default_value="/", type_cast=str),
            ConfigOption(canonical_name="type", default_value="", type_cast=str),
            ConfigOption(canonical_name="version", default_value="", type_cast=str),
            ConfigOption(canonical_name="environment", default_value="", type_cast=str),
            ConfigOption(canonical_name="tags", default_value="", type_cast=str),
        ]


class Root(ConfigBuilder):
    TOP_LEVEL = None

    def __init__(self):
        super().__init__()

        self.default_options = [
            ConfigOption(
                canonical_name="enable", default_value=True, type_cast=utils.str_to_bool
            )
        ]


class SamplingLockConfig(Singleton):
    def init(self):
        self.lock_enable = False
        self.lock_baseline = False
        self.lock_frequency = False
        self.lock_window = False

    def set_sampling_config(self, value):
        if value == "enable":
            self.lock_enable = True
        if value == "baseline":
            self.lock_baseline = True
        if value == "request_frequency":
            self.lock_frequency = True
        if value == "window_ms":
            self.lock_window = True
