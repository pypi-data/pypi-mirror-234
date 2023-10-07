#
# Copyright (c) 2012-2022 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from logging import getLogger
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

from trino.dbapi import Connection, Cursor, connect

from pystarburst._internal.analyzer.analyzer_utils import (
    convert_value_to_sql_option,
    escape_quotes,
    quote_name,
)
from pystarburst._internal.analyzer.expression.general import Attribute
from pystarburst._internal.analyzer.plan.trino_plan import TrinoPlan
from pystarburst._internal.error_message import PyStarburstClientExceptionMessages
from pystarburst._internal.utils import (
    convert_result_meta_to_named_tuple,
    result_set_to_iter,
    result_set_to_rows,
)
from pystarburst.query_history import QueryHistory, QueryRecord
from pystarburst.row import Row

logger = getLogger(__name__)


class ServerConnection:
    class _Decorator:
        @classmethod
        def wrap_exception(cls, func):
            def wrap(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    raise ex

            return wrap

    def __init__(
        self,
        options: Dict[str, Union[int, str]],
        conn: Optional[Connection] = None,
    ) -> None:
        self._lower_case_parameters = {k.lower(): v for k, v in options.items()}
        self._conn = conn if conn else connect(**self._lower_case_parameters)
        if "auth" in self._lower_case_parameters:
            self._lower_case_parameters["auth"] = None
        self._cursor = self._conn.cursor()
        self._query_listener: Set[QueryHistory] = set()
        # The session in this case refers to a Trino session, not a pystarburst session

    def add_query_listener(self, listener: QueryHistory) -> None:
        self._query_listener.add(listener)

    def remove_query_listener(self, listener: QueryHistory) -> None:
        self._query_listener.remove(listener)

    def close(self) -> None:
        if self._conn:
            self._conn.close()

    def is_closed(self) -> bool:
        # TODO: This should check if any queries are running
        return True

    @_Decorator.wrap_exception
    def _get_current_parameter(self, param: str, quoted: bool = True) -> Optional[str]:
        name = self._get_string_datum(f"SELECT CURRENT_{param.upper()}")
        return (quote_name(name) if quoted else escape_quotes(name)) if name else None

    def _get_string_datum(self, query: str) -> Optional[str]:
        rows = result_set_to_rows(self.run_query(query)["data"])
        return rows[0][0] if len(rows) > 0 else None

    def notify_query_listeners(self, query_record: QueryRecord) -> None:
        for listener in self._query_listener:
            listener._add_query(query_record)

    @_Decorator.wrap_exception
    def run_query(
        self,
        query: str,
        to_iter: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        try:
            query = query.strip()
            results_cursor = self._cursor.execute(query, **kwargs)
            self.notify_query_listeners(QueryRecord(results_cursor.query_id, query))
            logger.debug(f"Execute query [queryID: {results_cursor.query_id}] {query}")
        except Exception as ex:
            query_id_log = f" [queryID: {ex.query_id}]" if hasattr(ex, "query_id") else ""
            logger.error(f"Failed to execute query{query_id_log} {query}\n{ex}")
            raise ex

        return self._to_data_or_iter(results_cursor=results_cursor, to_iter=to_iter)

    def _to_data_or_iter(
        self,
        results_cursor: Cursor,
        to_iter: bool = False,
    ) -> Dict[str, Any]:
        data_or_iter = iter(results_cursor) if to_iter else list(results_cursor)
        return {"data": data_or_iter, "query_id": results_cursor.query_id}

    def execute(
        self,
        plan: TrinoPlan,
        to_iter: bool = False,
        **kwargs,
    ) -> Union[List[Row], Iterator[Row]]:
        result_set, result_meta = self.get_result_set(plan, to_iter, **kwargs)
        if to_iter:
            return result_set_to_iter(result_set["data"], result_meta)
        else:
            return result_set_to_rows(result_set["data"], result_meta)

    @TrinoPlan.Decorator.wrap_exception
    def get_result_set(
        self,
        trino_plan: TrinoPlan,
        to_iter: bool = False,
        **kwargs,
    ) -> Tuple[Dict[str, Union[List[Any], Cursor, str]], List[Any]]:
        plan = trino_plan

        result, result_meta = None, None
        statement_properties = None
        if "statement_properties" in kwargs:
            statement_properties = kwargs["statement_properties"]
            del kwargs["statement_properties"]
        try:
            # set session properties
            if statement_properties is not None:
                for key, value in statement_properties.items():
                    self.run_query(f"SET SESSION {key}={convert_value_to_sql_option(value)}")

            for i, query in enumerate(plan.queries):
                result = self.run_query(
                    query,
                    to_iter and (i == len(plan.queries) - 1),
                    **kwargs,
                )
                result_meta = convert_result_meta_to_named_tuple(self._cursor.description)

        finally:
            # reset session properties
            if statement_properties is not None:
                for key, value in statement_properties.items():
                    self.run_query(f"RESET SESSION {key}")

            # delete created tmp object
            if plan.post_actions is not None:
                for action in plan.post_actions:
                    self.run_query(
                        action,
                        **kwargs,
                    )

        if result is None:
            raise PyStarburstClientExceptionMessages.SQL_LAST_QUERY_RETURN_RESULTSET()

        return result, result_meta

    def get_result_and_metadata(self, plan: TrinoPlan, **kwargs) -> Tuple[List[Row], List[Attribute]]:
        result_set, result_meta = self.get_result_set(plan, **kwargs)
        result = result_set_to_rows(result_set["data"])
        return result, plan.output

    def get_result_query_id(self, plan: TrinoPlan, **kwargs) -> str:
        # get the iterator such that the data is not fetched
        result_set, _ = self.get_result_set(plan, to_iter=True, **kwargs)
        return result_set["query_id"]

    @_Decorator.wrap_exception
    def run_batch_insert(self, query: str, rows: List[Row], **kwargs) -> None:
        params = [list(row) for row in rows]
        result = self._cursor.executemany(query, params)
        self.notify_query_listeners(QueryRecord(result.query_id, query))
        logger.debug("Execute batch insertion query %s", query)
