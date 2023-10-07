#
# Copyright (c) 2012-2022 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

import trino.exceptions

from pystarburst.exceptions import (
    PyStarburstColumnException,
    PyStarburstDataframeException,
    PyStarburstInvalidObjectNameException,
    PyStarburstJoinException,
    PyStarburstMissingDbOrSchemaException,
    PyStarburstPlanException,
    PyStarburstSessionException,
    PyStarburstSQLException,
    PyStarburstTableException,
)


class PyStarburstClientExceptionMessages:
    """Holds all of the error messages that could be used in the PyStarburstClientException Class.

    IMPORTANT: keep this file in numerical order of the error-code."""

    # DataFrame Error Messages 01XX

    @staticmethod
    def DF_CANNOT_DROP_COLUMN_NAME(col_name: str) -> PyStarburstColumnException:
        return PyStarburstColumnException(
            f"Unable to drop the column {col_name}. You must specify the column by name " f'(e.g. df.drop(col("a"))).'
        )

    @staticmethod
    def DF_CANNOT_DROP_ALL_COLUMNS() -> PyStarburstColumnException:
        return PyStarburstColumnException("Cannot drop all columns")

    @staticmethod
    def DF_CANNOT_RESOLVE_COLUMN_NAME_AMONG(col_name: str, all_columns: str) -> PyStarburstColumnException:
        return PyStarburstColumnException(
            f'Cannot combine the DataFrames by column names. The column "{col_name}" is '
            f"not a column in the other DataFrame ({all_columns})."
        )

    @staticmethod
    def DF_CANNOT_RENAME_COLUMN_BECAUSE_MULTIPLE_EXIST(old_name: str, new_name: str, times: int) -> PyStarburstColumnException:
        return PyStarburstColumnException(
            f"Unable to rename the column {old_name} as {new_name} because this DataFrame has {times} columns named {old_name}."
        )

    @staticmethod
    def DF_SELF_JOIN_NOT_SUPPORTED() -> PyStarburstJoinException:
        return PyStarburstJoinException(
            "You cannot join a DataFrame with itself because the column references cannot "
            "be resolved correctly. Instead, create a copy of the DataFrame with copy.copy(), "
            "and join the DataFrame with this copy."
        )

    def DF_JOIN_INVALID_JOIN_TYPE(type1: str, types: str) -> PyStarburstJoinException:
        return PyStarburstJoinException(
            f"Unsupported join type '{type1}'. Supported join types include: {types}.",
        )

    @staticmethod
    def DF_CANNOT_RESOLVE_COLUMN_NAME(col_name: str) -> PyStarburstColumnException:
        return PyStarburstColumnException(f"The DataFrame does not contain the column named {col_name}.")

    @staticmethod
    def DF_CROSS_TAB_COUNT_TOO_LARGE(count: int, max_count: int) -> PyStarburstDataframeException:
        return PyStarburstDataframeException(
            f"The number of distinct values in the second input column ({count}) exceeds "
            f"the maximum number of distinct values allowed ({max_count})."
        )

    @staticmethod
    def MERGE_TABLE_ACTION_ALREADY_SPECIFIED(action: str, clause: str) -> PyStarburstTableException:
        return PyStarburstTableException(f"{action} has been specified for {clause} to merge table")

    # Plan Analysis error codes 02XX

    @staticmethod
    def PLAN_ANALYZER_INVALID_IDENTIFIER(name: str) -> PyStarburstPlanException:
        return PyStarburstPlanException(f"Invalid identifier {name}")

    @staticmethod
    def PLAN_CANNOT_CREATE_LITERAL(type: str) -> PyStarburstPlanException:
        return PyStarburstPlanException(f"Cannot create a Literal for {type}")

    # SQL Execution error codes 03XX

    @staticmethod
    def SQL_LAST_QUERY_RETURN_RESULTSET() -> PyStarburstSQLException:
        return PyStarburstSQLException(
            "Internal error: The execution for the last query " "in the Trino plan doesn't return a ResultSet.",
        )

    @staticmethod
    def SQL_EXCEPTION_FROM_PROGRAMMING_ERROR(
        pe: trino.exceptions.TrinoUserError,
    ) -> PyStarburstSQLException:
        return PyStarburstSQLException(pe.message, pe.query_id)

    @staticmethod
    def SQL_EXCEPTION_FROM_OPERATIONAL_ERROR(
        oe: trino.exceptions.TrinoExternalError,
    ) -> PyStarburstSQLException:
        return PyStarburstSQLException(oe.message, oe.query_id)

    # Server Error Messages 04XX

    @staticmethod
    def SERVER_CANNOT_FIND_CURRENT_CATALOG_OR_SCHEMA(v1: str, v2: str, v3: str) -> PyStarburstMissingDbOrSchemaException:
        return PyStarburstMissingDbOrSchemaException(
            f"The {v1} is not set for the current session. To set this, either run "
            f'session.sql("USE {v2}").collect() or set the {v3} connection property in '
            f"the dict or properties file that you specify when creating a session.",
        )

    @staticmethod
    def SERVER_NO_DEFAULT_SESSION() -> PyStarburstSessionException:
        return PyStarburstSessionException(
            "No default Session is found.",
        )

    @staticmethod
    def SERVER_FAILED_CLOSE_SESSION(message: str) -> PyStarburstSessionException:
        return PyStarburstSessionException(f"Failed to close this session. The error is: {message}")

    @staticmethod
    def MORE_THAN_ONE_ACTIVE_SESSIONS() -> PyStarburstSessionException:
        return PyStarburstSessionException("More than one active session is detected.")

    # General Error codes 15XX

    @staticmethod
    def GENERAL_INVALID_OBJECT_NAME(
        type_name: str,
    ) -> PyStarburstInvalidObjectNameException:
        return PyStarburstInvalidObjectNameException(f"The object name '{type_name}' is invalid.")
