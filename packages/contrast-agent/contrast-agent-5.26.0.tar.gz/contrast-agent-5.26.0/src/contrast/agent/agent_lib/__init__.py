# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

# we need this to ensure `agent_lib.modules.*` is available when importing `agent_lib`
import contrast.agent.agent_lib.modules
from contrast.agent.agent_lib.main import call, initialize, update_log_options
from contrast.agent.agent_lib.semantic_analysis import get_index_of_chained_cmd
from contrast.agent.agent_lib.semantic_analysis import does_file_path_bypass_security
from contrast.agent.agent_lib.semantic_analysis import initialize_semantic_analysis
from contrast.agent.agent_lib.semantic_analysis import (
    does_command_contain_dangerous_path,
)
from contrast.agent.agent_lib.input_tracing import (
    evaluate_header_input,
    evaluate_input_by_type,
    initialize_input_tracing,
    check_sql_injection_query,
    check_cmd_injection_query,
    check_method_tampering,
    map_result_and_free_eval_result,
    map_result_and_free_check_query_sink_result,
    DBType,
)
