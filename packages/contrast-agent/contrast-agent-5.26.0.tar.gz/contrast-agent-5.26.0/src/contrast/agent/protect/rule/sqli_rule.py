# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import re

from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.agent.protect.rule.sql_injection.default_sql_scanner import (
    DefaultSqlScanner,
)
from contrast.agent.protect.rule.sql_injection.mysql_sql_scanner import MysqlSqlScanner
from contrast.agent.protect.rule.sql_injection.postgres_sql_scanner import (
    PostgresSqlScanner,
)
from contrast.agent.protect.rule.sql_injection.sqlite_sql_scanner import (
    SqliteSqlScanner,
)


class SqlInjection(BaseRule):
    """
    SQL Injection Protection rule
    """

    RULE_NAME = "sql-injection"

    def build_attack_with_match(
        self, candidate_string, evaluation=None, attack=None, **kwargs
    ):
        scanner = kwargs.get("scanner", None)
        if scanner is None:
            scanner = self.get_database_scanner(kwargs.get("database"))

        for match in re.finditer(
            re.compile(re.escape(evaluation.value)), candidate_string
        ):
            # TODO: PYT-2847
            # - use the agent-lib implementation here instead of the scanners
            #   - see the ticket for the previous implementation - paste it here
            #   - something about that implementation isn't exactly right, but it's close
            # - remove everything related to `scanner` (including the scanners themselves)
            # - make sure the third arg to `check_sql_injection_query` is right

            # TODO: PYT-2847 remove this call
            last_boundary, boundary = scanner.crosses_boundary(
                candidate_string, match.start(), evaluation.value
            )

            if scanner.NO_BOUNDARY in [last_boundary, boundary]:
                break

            evaluation.attack_count += 1

            kwargs["start_idx"] = match.start()
            kwargs["end_idx"] = match.end()
            kwargs["boundary_overrun_idx"] = boundary
            kwargs["input_boundary_idx"] = last_boundary
            attack = self.build_or_append_attack(
                evaluation, attack, candidate_string, **kwargs
            )

        if attack is not None:
            attack.set_response(self.response_from_mode(self.mode))
            self.log_rule_matched(evaluation, attack.response, candidate_string)

        return attack

    def build_sample(self, evaluation, query, **kwargs):
        sample = self.build_base_sample(evaluation)
        if query is not None:
            sample.details["query"] = query

        if "start_idx" in kwargs:
            sample.details["start"] = int(kwargs["start_idx"])

        if "end_idx" in kwargs:
            sample.details["end"] = int(kwargs["end_idx"])

        if "boundary_overrun_idx" in kwargs:
            sample.details["boundaryOverrunIndex"] = int(kwargs["boundary_overrun_idx"])

        if "input_boundary_idx" in kwargs:
            sample.details["inputBoundaryIndex"] = int(kwargs["input_boundary_idx"])

        return sample

    def get_database_scanner(self, database):
        scanner = DefaultSqlScanner()

        if database == "MySQL":
            scanner = MysqlSqlScanner()
        elif database == "PostgreSQL":
            scanner = PostgresSqlScanner()
        elif database == "SQLite3":
            scanner = SqliteSqlScanner()

        return scanner

    def infilter_kwargs(self, user_input, patch_policy):
        return dict(database=patch_policy.module)

    def skip_protect_analysis(self, user_input, args, kwargs):
        """
        Some sql libraries use special objects (see from sqlalchemy import text)
        so we cannot just check if user_input is falsy.
        """
        if user_input is None:
            return True

        return False

    def convert_input(self, user_input):
        if not isinstance(user_input, (str, bytes)):
            user_input = str(user_input)

        return user_input
