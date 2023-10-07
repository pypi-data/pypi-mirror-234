#
# Copyright (c) 2012-2022 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

import datetime
import decimal
import uuid
from array import array
from functools import reduce
from logging import getLogger
from threading import RLock
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union

from trino.dbapi import Connection
from trino.exceptions import ProgrammingError

from pystarburst._internal.analyzer.analyzer import Analyzer
from pystarburst._internal.analyzer.analyzer_utils import quote_name
from pystarburst._internal.analyzer.expression.general import Attribute, Literal
from pystarburst._internal.analyzer.plan.logical_plan.leaf import (
    Query,
    Range,
    TrinoValues,
)
from pystarburst._internal.analyzer.plan.logical_plan.table_function import (
    TableFunctionRelation,
)
from pystarburst._internal.error_message import PyStarburstClientExceptionMessages
from pystarburst._internal.server_connection import ServerConnection
from pystarburst._internal.type_utils import ColumnOrName, infer_schema, merge_type
from pystarburst._internal.utils import (
    TRINO_CATALOG_SCHEMA_PATTERN,
    get_connector_version,
    get_os_name,
    get_python_version,
    get_version,
    validate_catalog_schema_name,
    validate_identifier_name,
    validate_object_name,
)
from pystarburst.dataframe import DataFrame
from pystarburst.functions import column
from pystarburst.query_history import QueryHistory
from pystarburst.row import Row
from pystarburst.table import Table
from pystarburst.table_function import (
    TableFunctionCall,
    _create_table_function_expression,
)
from pystarburst.types import (
    ArrayType,
    DateType,
    DecimalType,
    JsonType,
    MapType,
    StringType,
    StructType,
    TimeNTZType,
    TimestampNTZType,
    TimestampType,
    TimeType,
    _AtomicType,
)

_logger = getLogger(__name__)

_session_management_lock = RLock()
_active_sessions: Set["Session"] = set()


def _get_active_session() -> Optional["Session"]:
    with _session_management_lock:
        if len(_active_sessions) == 1:
            return next(iter(_active_sessions))
        elif len(_active_sessions) > 1:
            raise PyStarburstClientExceptionMessages.MORE_THAN_ONE_ACTIVE_SESSIONS()
        else:
            raise PyStarburstClientExceptionMessages.SERVER_NO_DEFAULT_SESSION()


def _add_session(session: "Session") -> None:
    with _session_management_lock:
        _active_sessions.add(session)


def _remove_session(session: "Session") -> None:
    with _session_management_lock:
        _active_sessions.remove(session)


class Session:
    """
    Establishes a connection with a Trino cluster and provides methods for creating DataFrames.

    When you create a :class:`Session` object, you provide connection parameters to establish a
    connection with a Trino cluster (e.g. an hostname, a user name, etc.). You can
    specify these settings in a dict that associates connection parameters names with values.
    The pystarburst library uses `the Trino Python Client <https://github.com/trinodb/trino-python-client>`_
    to connect to Trino.

    To create a :class:`Session` object from a ``dict`` of connection parameters::

        >>> connection_parameters = {
        ...     "host": "<host_name>",
        ...     "port": "<host_name>",
        ...     "user": "<user_name>",
        ...     "roles": {"system": "ROLE{analyst}"},
        ...     "catalog": "<catalog_name>",
        ...     "schema": "<schema1_name>",
        ... }
        >>> session = Session.builder.configs(connection_parameters).create() # doctest: +SKIP

    :class:`Session` contains functions to construct a :class:`DataFrame` like :meth:`table`,
    :meth:`sql` and :attr:`read`.

    A :class:`Session` object is not thread-safe.
    """

    class SessionBuilder:
        """
        Provides methods to set connection parameters and create a :class:`Session`.
        """

        def __init__(self) -> None:
            self._options = {}

        def _remove_config(self, key: str) -> "Session.SessionBuilder":
            """Only used in test."""
            self._options.pop(key, None)
            return self

        def config(self, key: str, value: Union[int, str]) -> "Session.SessionBuilder":
            """
            Adds the specified connection parameter to the :class:`SessionBuilder` configuration.
            """
            self._options[key] = value
            return self

        def configs(self, options: Dict[str, Union[int, str]]) -> "Session.SessionBuilder":
            """
            Adds the specified :class:`dict` of connection parameters to
            the :class:`SessionBuilder` configuration.

            Note:
                Calling this method overwrites any existing connection parameters
                that you have already set in the SessionBuilder.
            """
            self._options = {**self._options, **options, "source": "PyStarburst"}
            return self

        def create(self) -> "Session":
            """Creates a new Session."""
            if "connection" in self._options:
                return self._create_internal(self._options["connection"])
            return self._create_internal(conn=None)

        def _create_internal(self, conn: Optional[Connection] = None) -> "Session":
            use_endpoint = self._options.get("use_endpoint")
            self._options.pop("use_endpoint", None)
            if use_endpoint:
                new_session = Session(ServerConnection({}, conn) if conn else ServerConnection(self._options), True)
            else:
                new_session = Session(ServerConnection({}, conn) if conn else ServerConnection(self._options))
            if "password" in self._options:
                self._options["password"] = None
            _add_session(new_session)
            return new_session

        def __get__(self, obj, objtype=None):
            return Session.SessionBuilder()

    #: Returns a builder you can use to set configuration properties
    #: and create a :class:`Session` object.
    builder: SessionBuilder = SessionBuilder()

    def __init__(self, conn: ServerConnection, use_endpoint: Optional[bool] = False) -> None:
        self._session_id = uuid.uuid4()
        self._conn = conn
        self._session_info = f"""
"version" : {get_version()},
"python.version" : {get_python_version()},
"trino.version" : {get_connector_version()},
"os.name" : {get_os_name()}
"""
        self._last_action_id = 0
        self._last_canceled_id = 0
        self.use_endpoint = use_endpoint

        self._analyzer = Analyzer(self)
        _logger.info("pystarburst Session information: %s", self._session_info)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __str__(self):
        return (
            f"<{self.__class__.__module__}.{self.__class__.__name__}: "
            f"catalog={self.get_current_catalog()}, "
            f"schema={self.get_current_schema()}>"
        )

    def _generate_new_action_id(self) -> int:
        self._last_action_id += 1
        return self._last_action_id

    def close(self) -> None:
        """Close this session."""
        try:
            if self._conn.is_closed():
                _logger.debug(
                    "No-op because session %s had been previously closed.",
                    self._session_id,
                )
            else:
                _logger.info("Closing session: %s", self._session_id)
                self.cancel_all()
        except Exception as ex:
            raise PyStarburstClientExceptionMessages.SERVER_FAILED_CLOSE_SESSION(str(ex))
        finally:
            try:
                self._conn.close()
                _logger.info("Closed session: %s", self._session_id)
            finally:
                _remove_session(self)

    def cancel_all(self) -> None:
        """
        Cancel all action methods that are running currently.
        This does not affect any action methods called in the future.
        """
        _logger.info("Canceling all running queries")
        self._last_canceled_id = self._last_action_id
        self._conn.run_query(f"select system$cancel_all_queries({self._session_id})")

    def table(self, name: Union[str, Iterable[str]]) -> Table:
        """
        Returns a Table that points the specified table.

        Args:
            name: A string or list of strings that specify the table name or
                fully-qualified object identifier (database name, schema name, and table name).

            Note:
                If your table name contains special characters, use double quotes to mark it like this, ``session.table('"my table"')``.
                For fully qualified names, you need to use double quotes separately like this, ``session.table('"my db"."my schema"."my.table"')``.

        Examples::

            >>> df1 = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
            >>> df1.write.save_as_table("my_table", mode="overwrite")
            >>> session.table("my_table").collect()
            [Row(A=1, B=2), Row(A=3, B=4)]
            >>> current_db = session.get_current_catalog()
            >>> current_schema = session.get_current_schema()
            >>> session.table([current_db, current_schema, "my_table"]).collect()
            [Row(A=1, B=2), Row(A=3, B=4)]
        """

        if not isinstance(name, str) and isinstance(name, Iterable):
            name = ".".join(name)
        validate_object_name(name)
        t = Table(name, self)
        return t

    def table_function(
        self,
        func_name: Union[str, List[str], TableFunctionCall],
        *func_arguments: ColumnOrName,
        **func_named_arguments: ColumnOrName,
    ) -> DataFrame:
        """Creates a new DataFrame from the given Trino SQL table function.

        References: `Trino SQL functions <https://trino.io/docs/current/functions/table.html>`_.

        Example 1
            Query a table function by function name:

            >>> from pystarburst.functions import lit
            >>> session.table_function("split_to_table", lit("split words to table"), lit(" ")).collect()
            [Row(SEQ=1, INDEX=1, VALUE='split'), Row(SEQ=1, INDEX=2, VALUE='words'), Row(SEQ=1, INDEX=3, VALUE='to'), Row(SEQ=1, INDEX=4, VALUE='table')]

        Example 2
            Define a table function variable and query it:

            >>> from pystarburst.functions import table_function, lit
            >>> split_to_table = table_function("split_to_table")
            >>> session.table_function(split_to_table(lit("split words to table"), lit(" "))).collect()
            [Row(SEQ=1, INDEX=1, VALUE='split'), Row(SEQ=1, INDEX=2, VALUE='words'), Row(SEQ=1, INDEX=3, VALUE='to'), Row(SEQ=1, INDEX=4, VALUE='table')]

        Args:
            func_name: The SQL function name.
            func_arguments: The positional arguments for the SQL function.
            func_named_arguments: The named arguments for the SQL function, if it accepts named arguments.

        Returns:
            A new :class:`DataFrame` with data from calling the table function.

        See Also:
            - :meth:`DataFrame.join_table_function`, which lateral joins an existing :class:`DataFrame` and a SQL function.
        """
        func_expr = _create_table_function_expression(func_name, *func_arguments, **func_named_arguments)

        d = DataFrame(
            self,
            self._analyzer.resolve(TableFunctionRelation(func_expr)),
        )
        return d

    def sql(self, query: str) -> DataFrame:
        """
        Returns a new DataFrame representing the results of a SQL query.
        You can use this method to execute a SQL statement. Note that you still
        need to call :func:`DataFrame.collect` to execute this query in Trino.

        Args:
            query: The SQL statement to execute.

        Example::

            >>> # create a dataframe from a SQL query
            >>> df = session.sql("select 1/2")
            >>> # execute the query
            >>> df.collect()
            [Row(1/2=Decimal('0.500000'))]
        """

        d = DataFrame(self, self._analyzer.resolve(Query(sql=query)))

        return d

    def _run_query(self, query: str) -> List[Any]:
        return self._conn.run_query(query)["data"]

    def create_dataframe(
        self,
        data: Union[List, Tuple],
        schema: Optional[Union[StructType, List[str]]] = None,
    ) -> DataFrame:
        """Creates a new DataFrame containing the specified values from the local data.

        Args:
            data: The local data for building a :class:`DataFrame`. ``data`` can only
                be a :class:`list` or :class:`tuple`. Every element in
                ``data`` will constitute a row in the DataFrame.
            schema: A :class:`~pystarburst.types.StructType` containing names and
                data types of columns, or a list of column names, or ``None``.
                When ``schema`` is a list of column names or ``None``, the schema of the
                DataFrame will be inferred from the data across all rows. To improve
                performance, provide a schema. This avoids the need to infer data types
                with large data sets.

        Examples::

            >>> # create a dataframe with a schema
            >>> from pystarburst.types import IntegerType, StringType, StructField
            >>> schema = StructType([StructField("a", IntegerType()), StructField("b", StringType())])
            >>> session.create_dataframe([[1, "py"], [3, "trino"]], schema).collect()
            [Row(A=1, B='py'), Row(A=3, B='trino')]

            >>> # create a dataframe by inferring a schema from the data
            >>> from pystarburst import Row
            >>> # infer schema
            >>> session.create_dataframe([1, 2, 3, 4], schema=["a"]).collect()
            [Row(A=1), Row(A=2), Row(A=3), Row(A=4)]
            >>> session.create_dataframe([[1, 2, 3, 4]], schema=["a", "b", "c", "d"]).collect()
            [Row(A=1, B=2, C=3, D=4)]
            >>> session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"]).collect()
            [Row(A=1, B=2), Row(A=3, B=4)]
            >>> session.create_dataframe([Row(a=1, b=2, c=3, d=4)]).collect()
            [Row(A=1, B=2, C=3, D=4)]
            >>> session.create_dataframe([{"a": 1}, {"b": 2}]).collect()
            [Row(A=1, B=None), Row(A=None, B=2)]
        """

        if data is None:
            raise ValueError("data cannot be None.")

        # check the type of data
        if isinstance(data, Row):
            raise TypeError("create_dataframe() function does not accept a Row object.")

        if not isinstance(data, (list, tuple)):
            raise TypeError("create_dataframe() function only accepts data as a list or tuple.")

        # infer the schema based on the data
        names = None
        if isinstance(schema, StructType):
            new_schema = schema
        else:
            if not data:
                raise ValueError("Cannot infer schema from empty data")
            if isinstance(schema, list):
                names = schema
            new_schema = reduce(
                merge_type,
                (infer_schema(row, names) for row in data),
            )
        if len(new_schema.fields) == 0:
            raise ValueError("The provided schema or inferred schema cannot be None or empty")

        def convert_row_to_list(row: Union[Iterable[Any], Any], names: List[str]) -> List:
            row_dict = None
            if row is None:
                row = [None]
            elif isinstance(row, (tuple, list)):
                if not row:
                    row = [None]
                elif getattr(row, "_fields", None):  # Row or namedtuple
                    row_dict = row.as_dict() if isinstance(row, Row) else row._asdict()
            elif isinstance(row, dict):
                row_dict = row.copy()
            else:
                row = [row]

            if row_dict:
                # fill None if the key doesn't exist
                row_dict = {quote_name(k): v for k, v in row_dict.items()}
                return [row_dict.get(name) for name in names]
            else:
                # check the length of every row, which should be same across data
                if len(row) != len(names):
                    raise ValueError(
                        f"{len(names)} fields are required by schema "
                        f"but {len(row)} values are provided. This might be because "
                        f"data consists of rows with different lengths, or mixed rows "
                        f"with column names or without column names"
                    )
                return list(row)

        # always overwrite the column names if they are provided via schema
        if not names:
            names = [f.name for f in new_schema.fields]
        quoted_names = [quote_name(name) for name in names]
        rows = [convert_row_to_list(row, quoted_names) for row in data]

        # get attributes and data types
        attrs, data_types = [], []
        for field, quoted_name in zip(new_schema.fields, quoted_names):
            attrs.append(Attribute(name=quoted_name, dataType=field.datatype, nullable=field.nullable))
            data_types.append(field.datatype)

        converted = []
        for row in rows:
            converted_row = []
            for value, data_type in zip(row, data_types):
                if value is None:
                    converted_row.append(None)
                elif isinstance(value, decimal.Decimal) and isinstance(data_type, DecimalType):
                    converted_row.append(value)
                elif isinstance(value, datetime.datetime) and isinstance(data_type, TimestampNTZType):
                    converted_row.append(value)
                elif isinstance(value, datetime.datetime) and isinstance(data_type, TimestampType):
                    converted_row.append(value)
                elif isinstance(value, datetime.time) and isinstance(data_type, TimeNTZType):
                    converted_row.append(value)
                elif isinstance(value, datetime.time) and isinstance(data_type, TimeType):
                    converted_row.append(value)
                elif isinstance(value, datetime.date) and isinstance(data_type, DateType):
                    converted_row.append(value)
                elif isinstance(data_type, _AtomicType):  # consider inheritance
                    converted_row.append(value)
                elif isinstance(value, (list, tuple)) and isinstance(data_type, ArrayType):
                    converted_row.append(value)
                elif isinstance(value, array) and isinstance(data_type, ArrayType):
                    converted_row.append(value.tolist())
                elif isinstance(value, tuple) and isinstance(data_type, StructType):
                    converted_row.append(value)
                elif isinstance(value, dict) and isinstance(data_type, MapType):
                    converted_row.append(value)
                elif isinstance(data_type, JsonType):
                    converted_row.append(value)
                else:
                    raise TypeError(f"Cannot cast {type(value)}({value}) to {str(data_type)}.")
            converted.append(Row(*converted_row))

        # construct a project statement to convert string value back to variant
        project_columns = []
        for field, name in zip(new_schema.fields, names):
            project_columns.append(column(name))

        df = DataFrame(
            self,
            self._analyzer.resolve(
                TrinoValues(
                    attributes=attrs, data=[[Literal(value=value) for value in row] for row in converted] if rows else None
                )
            ),
        ).select(project_columns)
        return df

    def range(self, start: int, end: Optional[int] = None, step: int = 1) -> DataFrame:
        """
        Creates a new DataFrame from a range of numbers. The resulting DataFrame has
        single column named ``ID``, containing elements in a range from ``start`` to
        ``end`` (exclusive) with the step value ``step``.

        Args:
            start: The start of the range. If ``end`` is not specified,
                ``start`` will be used as the value of ``end``.
            end: The end of the range.
            step: The step of the range.

        Examples::

            >>> session.range(10).collect()
            [Row(ID=0), Row(ID=1), Row(ID=2), Row(ID=3), Row(ID=4), Row(ID=5), Row(ID=6), Row(ID=7), Row(ID=8), Row(ID=9)]
            >>> session.range(1, 10).collect()
            [Row(ID=1), Row(ID=2), Row(ID=3), Row(ID=4), Row(ID=5), Row(ID=6), Row(ID=7), Row(ID=8), Row(ID=9)]
            >>> session.range(1, 10, 2).collect()
            [Row(ID=1), Row(ID=3), Row(ID=5), Row(ID=7), Row(ID=9)]
        """
        range_plan = Range(start=0, end=start, step=step) if end is None else Range(start=start, end=end, step=step)
        df = DataFrame(
            self,
            self._analyzer.resolve(range_plan),
        )
        return df

    def get_current_catalog(self) -> Optional[str]:
        """
        Returns the name of the current catalog for the Trino session attached
        to this session. See the example in :meth:`table`.
        """
        return self._conn._get_current_parameter("catalog")

    def get_current_schema(self) -> Optional[str]:
        """
        Returns the name of the current schema for the Python connector session attached
        to this session. See the example in :meth:`table`.
        """
        return self._conn._get_current_parameter("schema")

    def get_fully_qualified_current_schema(self) -> str:
        """Returns the fully qualified name of the current schema for the session."""
        catalog = self.get_current_catalog()
        schema = self.get_current_schema()
        if catalog is None or schema is None:
            missing_item = "CATALOG" if not catalog else "SCHEMA"
            raise PyStarburstClientExceptionMessages.SERVER_CANNOT_FIND_CURRENT_CATALOG_OR_SCHEMA(
                missing_item, missing_item, missing_item
            )
        return catalog + "." + schema

    def get_current_roles(self) -> Optional[Dict[str, str]]:
        """
        Returns the name of the roles in use for the current session.
        """
        return self._conn._conn._client_session.roles

    def use(self, catalog_schema: str) -> None:
        """Specifies the active/current schema for the session.

        Args:
            catalog_schema: The catalog and/or schema name.
        """
        if catalog_schema:
            validate_catalog_schema_name(catalog_schema)
            matches = TRINO_CATALOG_SCHEMA_PATTERN.match(catalog_schema)
            [catalog, _] = matches.groups()
            if catalog is None and self.get_current_catalog() is None:
                raise ValueError("No current catalog is set.")
            self._run_query(f"use {catalog_schema}")
        else:
            raise ValueError("Catalog and/or schema must not be empty or None.")

    def set_role(self, role: str, catalog: str = "system") -> None:
        """Specifies the active/current role for the session.

        Args:
            role: the role name.
            catalog: the catalog name (defaults to 'system')
        """
        if role:
            validate_identifier_name(role)
            validate_identifier_name(catalog)
            self._run_query(f"set role {role} in catalog {catalog}")
        else:
            raise ValueError("role must not be empty or None.")

    def query_history(self) -> QueryHistory:
        """Create an instance of :class:`QueryHistory` as a context manager to record queries that are pushed down to the Trino cluster.

        >>> with session.query_history() as query_history:
        ...     df = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
        ...     df = df.filter(df.a == 1)
        ...     res = df.collect()
        >>> assert len(query_history.queries) == 1
        """
        query_listener = QueryHistory(self)
        self._conn.add_query_listener(query_listener)
        return query_listener

    def _table_exists(self, table_name: str):
        validate_object_name(table_name)
        # note: object name could have dots, e.g, a table could be created via: create table "abc.abc" (id int)
        # currently validate_object_name does not allow it, but if in the future we want to support the case, we need to
        # update the implementation accordingly in this method
        qualified_table_name = table_name.split(".")
        if len(qualified_table_name) == 1:
            # name in the form of "table"
            tables = self._run_query(f"show tables like '{table_name}'")
        elif len(qualified_table_name) == 2:
            # name in the form of "schema.table" omitting database
            # schema: qualified_table_name[0]
            # table: qualified_table_name[1]
            tables = self._run_query(f"show tables from {qualified_table_name[0]} like '{qualified_table_name[1]}'")
        elif len(qualified_table_name) == 3:
            # name in the form of "catalog.schema.table"
            # database: qualified_table_name[0]
            # schema: qualified_table_name[1]
            # table: qualified_table_name[2]
            tables = self._run_query(
                f"show tables from {qualified_table_name[0]}.{qualified_table_name[1]} like '{qualified_table_name[2]}'"
            )
        else:
            # we do not support len(qualified_table_name) > 3 for now
            raise PyStarburstClientExceptionMessages.GENERAL_INVALID_OBJECT_NAME(table_name)

        return tables is not None and len(tables) > 0

    def _explain_query(self, query: str) -> Optional[str]:
        try:
            return self._run_query(f"explain analyze {query}")[0][0]
        # return None for queries which can't be explained
        except ProgrammingError:
            _logger.warning("query '%s' cannot be explained")
            return None

    createDataFrame = create_dataframe
