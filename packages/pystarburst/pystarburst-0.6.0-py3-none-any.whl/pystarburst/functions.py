#
# Copyright (c) 2012-2022 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

"""
Provides utility and SQL functions that generate :class:`~pystarburst.Column` expressions that you can pass to :class:`~pystarburst.DataFrame` transformation methods.

These utility functions generate references to columns, literals, and SQL expressions (e.g. "c + 1").

  - Use :func:`col()` to convert a column name to a :class:`Column` object. Refer to the API docs of :class:`Column` to know more ways of referencing a column.
  - Use :func:`lit()` to convert a Python value to a :class:`Column` object that represents a constant value in Trino SQL.
  - Use :func:`sql_expr()` to convert a Trino SQL expression to a :class:`Column`.

    >>> df = session.create_dataframe([[1, 'a', True, '2022-03-16'], [3, 'b', False, '2023-04-17']], schema=["a", "b", "c", "d"])
    >>> res1 = df.filter(col("a") == 1).collect()
    >>> res2 = df.filter(lit(1) == col("a")).collect()
    >>> res3 = df.filter(sql_expr("a = 1")).collect()
    >>> assert res1 == res2 == res3
    >>> res1
    [Row(A=1, B='a', C=True, D='2022-03-16')]

Some :class:`DataFrame` methods accept column names or SQL expressions text aside from a Column object for convenience.
For instance:

    >>> df.filter("a = 1").collect()  # use the SQL expression directly in filter
    [Row(A=1, B='a', C=True, D='2022-03-16')]
    >>> df.select("a").collect()
    [Row(A=1), Row(A=3)]

whereas :class:`Column` objects enable you to use chained column operators and transformations with
Python code fluently:

    >>> # Use columns and literals in expressions.
    >>> df.select(((col("a") + 1).cast("string")).alias("add_one")).show()
    -------------
    |"ADD_ONE"  |
    -------------
    |2          |
    |4          |
    -------------
    <BLANKLINE>

Trino has hundreds of `SQL functions <https://trino.io/docs/current/functions.html>`_
This module provides Python functions that correspond to the Trino SQL functions. They typically accept :class:`Column`
objects or column names as input parameters and return a new :class:`Column` objects.
The following examples demonstrate the use of some of these functions:

    >>> # This example calls the function that corresponds to the TO_DATE() SQL function.
    >>> df.select(dateadd('day', lit(1), to_date(col("d")))).show()
    ---------------------------------------
    |"DATEADD('DAY', 1, TO_DATE(""D""))"  |
    ---------------------------------------
    |2022-03-17                           |
    |2023-04-18                           |
    ---------------------------------------
    <BLANKLINE>

If you want to use a SQL function in Trino but can't find the corresponding Python function here,
you can create your own Python function with :func:`function`:

    >>> my_radians = function("radians")  # "radians" is the SQL function name.
    >>> df.select(my_radians(col("a")).alias("my_radians")).show()
    ------------------------
    |"MY_RADIANS"          |
    ------------------------
    |0.017453292519943295  |
    |0.05235987755982988   |
    ------------------------
    <BLANKLINE>

or call the SQL function directly:

    >>> df.select(call_function("radians", col("a")).as_("call_function_radians")).show()
    ---------------------------
    |"CALL_FUNCTION_RADIANS"  |
    ---------------------------
    |0.017453292519943295     |
    |0.05235987755982988      |
    ---------------------------
    <BLANKLINE>

**How to find help on input parameters of the Python functions for SQL functions**
The Python functions have the same name as the corresponding `SQL functions <https://trino.io/docs/current/functions.html>`_.

By reading the API docs or the source code of a Python function defined in this module, you'll see the type hints of the input parameters and return type.
The return type is always ``Column``. The input types tell you the acceptable values:

  - ``ColumnOrName`` accepts a :class:`Column` object, or a column name in str. Most functions accept this type.
    If you still want to pass a literal to it, use `lit(value)`, which returns a ``Column`` object that represents a literal value.

    >>> df.select(avg("a")).show()
    ----------------
    |"AVG(""A"")"  |
    ----------------
    |2.000000      |
    ----------------
    <BLANKLINE>
    >>> df.select(avg(col("a"))).show()
    ----------------
    |"AVG(""A"")"  |
    ----------------
    |2.000000      |
    ----------------
    <BLANKLINE>

  - ``LiteralType`` accepts a value of type ``bool``, ``int``, ``float``, ``str``, ``bytearray``, ``decimal.Decimal``,
    ``datetime.date``, ``datetime.datetime``, ``datetime.time``, or ``bytes``. An example is the third parameter of :func:`lead`.

    >>> import datetime
    >>> from pystarburst.window import Window
    >>> df.select(col("d"), lead("d", 1, datetime.date(2024, 5, 18), False).over(Window.order_by("d")).alias("lead_day")).show()
    ---------------------------
    |"D"         |"LEAD_DAY"  |
    ---------------------------
    |2022-03-16  |2023-04-17  |
    |2023-04-17  |2024-05-18  |
    ---------------------------
    <BLANKLINE>

  - ``ColumnOrLiteral`` accepts a ``Column`` object, or a value of ``LiteralType`` mentioned above.
    The difference from ``ColumnOrLiteral`` is ``ColumnOrLiteral`` regards a str value as a SQL string value instead of
    a column name. When a function is much more likely to accept a SQL constant value than a column expression, ``ColumnOrLiteral``
    is used. Yet you can still pass in a ``Column`` object if you need to. An example is the second parameter of
    :func:``when``.

    >>> df.select(when(df["a"] > 2, "Greater than 2").else_("Less than 2").alias("compare_with_2")).show()
    --------------------
    |"COMPARE_WITH_2"  |
    --------------------
    |Less than 2       |
    |Greater than 2    |
    --------------------
    <BLANKLINE>

  - ``int``, ``bool``, ``str``, or another specific type accepts a value of that type. An example is :func:`to_decimal`.

    >>> df.with_column("e", lit("1.2")).select(to_decimal("e", 5, 2)).show()
    -----------------------------
    |"TO_DECIMAL(""E"", 5, 2)"  |
    -----------------------------
    |1.20                       |
    |1.20                       |
    -----------------------------
    <BLANKLINE>

  - ``ColumnOrSqlExpr`` accepts a ``Column`` object, or a SQL expression. For instance, the first parameter in :func:``when``.

    >>> df.select(when("a > 2", "Greater than 2").else_("Less than 2").alias("compare_with_2")).show()
    --------------------
    |"COMPARE_WITH_2"  |
    --------------------
    |Less than 2       |
    |Greater than 2    |
    --------------------
    <BLANKLINE>
"""
from typing import Callable, Iterable, List, Optional, Union

import pystarburst.table_function
from pystarburst._internal.analyzer.expression.general import (
    ArrayExpression,
    CaseWhen,
    FunctionExpression,
    ListAgg,
    Literal,
    MultipleExpression,
    Star,
)
from pystarburst._internal.analyzer.expression.window import (
    FirstValue,
    Lag,
    LastValue,
    Lead,
    NthValue,
)
from pystarburst._internal.type_utils import (
    ColumnOrLiteral,
    ColumnOrLiteralStr,
    ColumnOrName,
    ColumnOrSqlExpr,
    LiteralType,
)
from pystarburst._internal.utils import parse_positional_args_to_list
from pystarburst.column import (
    CaseExpr,
    Column,
    _to_col_if_sql_expr,
    _to_col_if_str,
    _to_col_if_str_or_int,
)
from pystarburst.types import BinaryType, DataType, StringType, TimestampNTZType


def col(col_name: str) -> Column:
    """Returns the :class:`~pystarburst.Column` with the specified name."""
    return Column(col_name)


def column(col_name: str) -> Column:
    """Returns a :class:`~pystarburst.Column` with the specified name. Alias for col."""
    return Column(col_name)


def lit(literal: LiteralType) -> Column:
    """
    Creates a :class:`~pystarburst.Column` expression for a literal value.
    It supports basic Python data types, including ``int``, ``float``, ``str``,
    ``bool``, ``bytes``, ``bytearray``, ``datetime.time``, ``datetime.date``,
    ``datetime.datetime`` and ``decimal.Decimal``. Also, it supports Python structured data types,
    including ``list``, ``tuple`` and ``dict``, but this container must
    be JSON serializable.
    """
    return literal if isinstance(literal, Column) else Column(Literal(value=literal))


def sql_expr(sql: str) -> Column:
    """Creates a :class:`~pystarburst.Column` expression from raw SQL text.
    Note that the function does not interpret or check the SQL text."""
    return Column._expr(sql)


def current_user() -> Column:
    """
    Returns the name of the user currently logged into the system.

    Example:
        >>> # Return result is tied to session, so we only test if the result exists
        >>> result = session.create_dataframe([1]).select(current_user()).collect()
        >>> assert result is not None
    """
    return builtin("current_user")()


def current_catalog() -> Column:
    """Returns the name of the catalog in use for the current session.

    Example:
        >>> # Return result is tied to session, so we only test if the result exists
        >>> result = session.create_dataframe([1]).select(current_catalog()).collect()
        >>> assert result is not None
    """
    return builtin("current_catalog")()


def current_groups() -> Column:
    """Returns the list of groups for the current user running the query.

    Example:
        >>> # Return result is tied to session, so we only test if the result exists
        >>> result = session.create_dataframe([1]).select(current_groups()).collect()
        >>> assert result is not None
    """
    return builtin("current_groups()")()


def current_schema() -> Column:
    """Returns the name of the schema in use for the current session.

    Example:
        >>> # Return result is tied to session, so we only test if the result exists
        >>> result = session.create_dataframe([1]).select(current_schema()).collect()
        >>> assert result is not None
    """
    return builtin("current_schema")()


def add_months(date_or_timestamp: ColumnOrName, number_of_months: Union[Column, int]) -> Column:
    """Adds or subtracts a specified number of months to a date or timestamp, preserving the end-of-month information.

    Example:
        >>> import datetime
        >>> df = session.create_dataframe([datetime.date(2022, 4, 6)], schema=["d"])
        >>> df.select(add_months("d", 4)).collect()[0][0]
        datetime.date(2022, 8, 6)
    """
    c = _to_col_if_str(date_or_timestamp, "add_months")
    return builtin("date_add")("month", number_of_months, c)


def any_value(e: ColumnOrName) -> Column:
    """Returns a non-deterministic any value for the specified column.
    This is an aggregate and window function.

    Example:
        >>> df = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
        >>> result = df.select(any_value("a")).collect()
        >>> assert len(result) == 1  # non-deterministic value in result.
    """
    c = _to_col_if_str(e, "any_value")
    return call_builtin("any_value", c)


def power(x: ColumnOrName, p: Union[Column, int]) -> Column:
    """Returns x raised to the power of p.

    Example:
        >>> df = session.create_dataframe([2], schema=["a"])
        >>> df.select(power("a", 2)).collect()[0][0]
        4
    """
    c = _to_col_if_str(x, "power")
    return call_builtin("power", c, p)


def is_nan(x: ColumnOrName) -> Column:
    """Determine if x is not-a-number.

    Example:
        >>> df = session.create_dataframe([2], schema=["a"])
        >>> df.select(is_nan("a")).collect()[0][0]
        False
    """
    c = _to_col_if_str(x, "is_nan")
    return call_builtin("is_nan", c)


def bitand(column1: ColumnOrName, column2: ColumnOrName) -> Column:
    """Returns the bitwise negation of a numeric expression.

    Example:
        >>> df = session.create_dataframe([19, 25], schema=["a", "b"])
        >>> df.select(bitand("a", "b")).collect()[0][0]
        17
    """
    c1 = _to_col_if_str(column1, "bitwise_and")
    c2 = _to_col_if_str(column2, "bitwise_and")
    return call_builtin("bitwise_and", c1, c2)


def bitor(column1: ColumnOrName, column2: ColumnOrName) -> Column:
    """Returns the bitwise negation of a numeric expression.

    Example:
        >>> df = session.create_dataframe([19, 25], schema=["a", "b"])
        >>> df.select(bitor("a", "b")).collect()[0][0]
        27
    """
    c1 = _to_col_if_str(column1, "bitwise_or")
    c2 = _to_col_if_str(column2, "bitwise_or")
    return call_builtin("bitwise_or", c1, c2)


def bitxor(column1: ColumnOrName, column2: ColumnOrName) -> Column:
    """Returns the bitwise XOR of x and y in 2’s complement representation,

    Example:
        >>> df = session.create_dataframe([19, 25], schema=["a", "b"])
        >>> df.select(bitxor("a", "b")).collect()[0][0]
        10
    """
    c1 = _to_col_if_str(column1, "bitwise_xor")
    c2 = _to_col_if_str(column2, "bitwise_xor")
    return call_builtin("bitwise_xor", c1, c2)


def bitnot(e: ColumnOrName) -> Column:
    """Returns the bitwise negation of a numeric expression.

    Example:
        >>> df = session.create_dataframe([1], schema=["a"])
        >>> df.select(bitnot("a")).collect()[0][0]
        -2
    """
    c = _to_col_if_str(e, "bitwise_not")
    return call_builtin("bitwise_not", c)


def bitshiftleft(to_shift_column: ColumnOrName, n: Union[Column, int]) -> Column:
    """Returns the left shifted value of value

    Example:
        >>> df = session.create_dataframe([2], schema=["a"])
        >>> df.select(bitshiftleft("a", 1)).collect()[0][0]
        4
    """
    c = _to_col_if_str(to_shift_column, "bitwise_left_shift")
    n = _to_col_if_str(n, "bitwise_left_shift")
    return call_builtin("bitwise_left_shift", c, n)


def bitshiftright(to_shift_column: ColumnOrName, n: Union[Column, int]) -> Column:
    """Returns the right shifted value of value

    Example:
        >>> df = session.create_dataframe([2], schema=["a"])
        >>> df.select(bitshiftright("a", 1)).collect()[0][0]
        1
    """
    c = _to_col_if_str(to_shift_column, "bitwise_right_shift")
    n = _to_col_if_str(n, "bitwise_right_shift")
    return call_builtin("bitwise_right_shift", c, n)


# TODO : should be converted into AT TIME ZONE
def convert_timezone(
    target_timezone: ColumnOrName,
    source_time: ColumnOrName,
    source_timezone: Optional[ColumnOrName] = None,
) -> Column:
    """Converts the given source_time to the target timezone.

    For timezone information, refer to the `Trino time conversion notes <https://trino.io/docs/current/functions/datetime.html#time-zone-conversion>`_

        Args:
            target_timezone: The time zone to which the input timestamp should be converted.=
            source_time: The timestamp to convert. When it's a TIMESTAMP_LTZ, use ``None`` for ``source_timezone``.
            source_timezone: The time zone for the ``source_time``. Required for timestamps with no time zone (i.e. TIMESTAMP_NTZ). Use ``None`` if the timestamps have a time zone (i.e. TIMESTAMP_LTZ). Default is ``None``.

        Note:
            The sequence of the 3 params is different from the SQL function, which two overloads:

              - ``CONVERT_TIMEZONE( <source_tz> , <target_tz> , <source_timestamp_ntz> )``
              - ``CONVERT_TIMEZONE( <target_tz> , <source_timestamp> )``

            The first parameter ``source_tz`` is optional. But in Python an optional argument shouldn't be placed at the first.
            So ``source_timezone`` is after ``source_time``.

        Example:
            >>> import datetime
            >>> from dateutil import tz
            >>> datetime_with_tz = datetime.datetime(2022, 4, 6, 9, 0, 0, tzinfo=tz.tzoffset("myzone", -3600*7))
            >>> datetime_with_no_tz = datetime.datetime(2022, 4, 6, 9, 0, 0)
            >>> df = session.create_dataframe([[datetime_with_tz, datetime_with_no_tz]], schema=["a", "b"])
            >>> result = df.select(convert_timezone(lit("UTC"), col("a")), convert_timezone(lit("UTC"), col("b"), lit("Asia/Shanghai"))).collect()
            >>> result[0][0]
            datetime.datetime(2022, 4, 6, 16, 0, tzinfo=<UTC>)
            >>> result[0][1]
            datetime.datetime(2022, 4, 6, 1, 0)
    """
    source_tz = _to_col_if_str(source_timezone, "convert_timezone") if source_timezone is not None else None
    target_tz = _to_col_if_str(target_timezone, "convert_timezone")
    source_time_to_convert = _to_col_if_str(source_time, "convert_timezone")

    if source_timezone is None:
        return call_builtin("convert_timezone", target_tz, source_time_to_convert)
    return call_builtin("convert_timezone", source_tz, target_tz, source_time_to_convert)


def approx_distinct(e: ColumnOrName) -> Column:
    """Uses HyperLogLog to return an approximation of the distinct cardinality of the input (i.e. HLL(col1, col2, ... )
    returns an approximation of COUNT(DISTINCT col1, col2, ... ))."""
    c = _to_col_if_str(e, "approx_distinct")
    return builtin("approx_distinct")(c)


def avg(e: ColumnOrName) -> Column:
    """Returns the average of non-NULL records. If all records inside a group are NULL,
    the function returns NULL."""
    c = _to_col_if_str(e, "avg")
    return builtin("avg")(c)


def corr(column1: ColumnOrName, column2: ColumnOrName) -> Column:
    """Returns the correlation coefficient for non-null pairs in a group."""
    c1 = _to_col_if_str(column1, "corr")
    c2 = _to_col_if_str(column2, "corr")
    return builtin("corr")(c1, c2)


def count(e: ColumnOrName) -> Column:
    """Returns either the number of non-NULL records for the specified columns, or the
    total number of records."""
    c = _to_col_if_str(e, "count")
    return builtin("count")(Literal(value=1)) if isinstance(c._expression, Star) else builtin("count")(c._expression)


def count_distinct(*cols: ColumnOrName) -> Column:
    """Returns either the number of non-NULL distinct records for the specified columns,
    or the total number of the distinct records.
    """
    cs = [_to_col_if_str(c, "count_distinct") for c in cols]
    return Column(FunctionExpression(name="count", arguments=[c._expression for c in cs], is_distinct=True))


def covar_pop(column1: ColumnOrName, column2: ColumnOrName) -> Column:
    """Returns the population covariance for non-null pairs in a group."""
    col1 = _to_col_if_str(column1, "covar_pop")
    col2 = _to_col_if_str(column2, "covar_pop")
    return builtin("covar_pop")(col1, col2)


def covar_samp(column1: ColumnOrName, column2: ColumnOrName) -> Column:
    """Returns the sample covariance for non-null pairs in a group."""
    col1 = _to_col_if_str(column1, "covar_samp")
    col2 = _to_col_if_str(column2, "covar_samp")
    return builtin("covar_samp")(col1, col2)


def kurtosis(e: ColumnOrName) -> Column:
    """Returns the population excess kurtosis of non-NULL records. If all records
    inside a group are NULL, the function returns NULL."""
    c = _to_col_if_str(e, "kurtosis")
    return builtin("kurtosis")(c)


def max(e: ColumnOrName) -> Column:
    """Returns the maximum value for the records in a group. NULL values are ignored
    unless all the records are NULL, in which case a NULL value is returned."""
    c = _to_col_if_str(e, "max")
    return builtin("max")(c)


def max_by(e: ColumnOrName, f: ColumnOrName) -> Column:
    """Returns the maximum value for the records in a group. NULL values are ignored
    unless all the records are NULL, in which case a NULL value is returned."""
    c = _to_col_if_str(e, "max_by")
    d = _to_col_if_str(f, "max_by")
    return builtin("max_by")(c, d)


def mean(e: ColumnOrName) -> Column:
    """Return the average for the specific numeric columns. Alias of :func:`avg`."""
    c = _to_col_if_str(e, "mean")
    return avg(c)


def min(e: ColumnOrName) -> Column:
    """Returns the minimum value for the records in a group. NULL values are ignored
    unless all the records are NULL, in which case a NULL value is returned."""
    c = _to_col_if_str(e, "min")
    return builtin("min")(c)


def min_by(e: ColumnOrName, f: ColumnOrName) -> Column:
    """Returns the minimum value for the records in a group. NULL values are ignored
    unless all the records are NULL, in which case a NULL value is returned."""
    c = _to_col_if_str(e, "min_by")
    d = _to_col_if_str(f, "min_by")
    return builtin("min_by")(c, d)


def mode(e: ColumnOrName) -> Column:
    """Returns the most frequent value for the records in a group. NULL values are ignored.
    If all the values are NULL, or there are 0 rows, then the function returns NULL."""
    c = _to_col_if_str(e, "mode")
    return builtin("mode")(c)


def pmod(e: ColumnOrName, f: ColumnOrName) -> Column:
    """Returns the positive modulus for the input"""
    i = _to_col_if_str(e, "pmod")
    n = _to_col_if_str(f, "pmod")
    return builtin("if")(builtin("mod")(i, n) > 0, builtin("mod")(i, n), builtin("mod")(builtin("mod")(i, n) + n, n))


def skewness(e: ColumnOrName) -> Column:
    """Returns the sample skewness of non-NULL records. If all records inside a group
    are NULL, the function returns NULL."""
    c = _to_col_if_str(e, "skewness")
    return builtin("skewness")(c)


def stddev(e: ColumnOrName) -> Column:
    """Returns the sample standard deviation (square root of sample variance) of
    non-NULL values. If all records inside a group are NULL, returns NULL."""
    c = _to_col_if_str(e, "stddev")
    return builtin("stddev")(c)


def stddev_samp(e: ColumnOrName) -> Column:
    """Returns the sample standard deviation (square root of sample variance) of
    non-NULL values. If all records inside a group are NULL, returns NULL. Alias of
    :func:`stddev`."""
    c = _to_col_if_str(e, "stddev_samp")
    return builtin("stddev_samp")(c)


def stddev_pop(e: ColumnOrName) -> Column:
    """Returns the population standard deviation (square root of variance) of non-NULL
    values. If all records inside a group are NULL, returns NULL."""
    c = _to_col_if_str(e, "stddev_pop")
    return builtin("stddev_pop")(c)


def sum(e: ColumnOrName) -> Column:
    """Returns the sum of non-NULL records in a group. You can use the DISTINCT keyword
    to compute the sum of unique non-null values. If all records inside a group are
    NULL, the function returns NULL."""
    c = _to_col_if_str(e, "sum")
    return builtin("sum")(c)


def product(e: ColumnOrName) -> Column:
    """Returns the product of all values."""
    c = _to_col_if_str(e, "product")
    return builtin("reduce_agg")(c, lit(1), sql_expr("(a, b) -> a * b"), sql_expr("(a, b) -> a * b"))


def sum_distinct(e: ColumnOrName) -> Column:
    """Returns the sum of non-NULL distinct records in a group. You can use the
    DISTINCT keyword to compute the sum of unique non-null values. If all records
    inside a group are NULL, the function returns NULL."""
    c = _to_col_if_str(e, "sum_distinct")
    return _call_function("sum", True, c)


def variance(e: ColumnOrName) -> Column:
    """Returns the sample variance of non-NULL records in a group. If all records
    inside a group are NULL, a NULL is returned."""
    c = _to_col_if_str(e, "variance")
    return builtin("variance")(c)


def var_samp(e: ColumnOrName) -> Column:
    """Returns the sample variance of non-NULL records in a group. If all records
    inside a group are NULL, a NULL is returned. Alias of :func:`variance`"""
    c = _to_col_if_str(e, "var_samp")
    return variance(c)


def var_pop(e: ColumnOrName) -> Column:
    """Returns the population variance of non-NULL records in a group. If all records
    inside a group are NULL, a NULL is returned."""
    c = _to_col_if_str(e, "var_pop")
    return builtin("var_pop")(c)


def approx_percentile(col: ColumnOrName, percentile: float) -> Column:
    """Returns an approximated value for the desired percentile. This function uses the t-Digest algorithm."""
    c = _to_col_if_str(col, "approx_percentile")
    return builtin("approx_percentile")(c, sql_expr(str(percentile)))


def approx_percentile_accumulate(col: ColumnOrName) -> Column:
    """Returns the internal representation of the t-Digest state (as a JSON object) at the end of aggregation.
    This function uses the t-Digest algorithm.
    """
    c = _to_col_if_str(col, "approx_percentile_accumulate")
    return builtin("approx_percentile_accumulate")(c)


def approx_percentile_estimate(state: ColumnOrName, percentile: float) -> Column:
    """Returns the desired approximated percentile value for the specified t-Digest state.
    APPROX_PERCENTILE_ESTIMATE(APPROX_PERCENTILE_ACCUMULATE(.)) is equivalent to
    APPROX_PERCENTILE(.).
    """
    c = _to_col_if_str(state, "approx_percentile_estimate")
    return builtin("approx_percentile_estimate")(c, sql_expr(str(percentile)))


def approx_percentile_combine(state: ColumnOrName) -> Column:
    """Combines (merges) percentile input states into a single output state.
    This allows scenarios where APPROX_PERCENTILE_ACCUMULATE is run over horizontal partitions
    of the same table, producing an algorithm state for each table partition. These states can
    later be combined using APPROX_PERCENTILE_COMBINE, producing the same output state as a
    single run of APPROX_PERCENTILE_ACCUMULATE over the entire table.
    """
    c = _to_col_if_str(state, "approx_percentile_combine")
    return builtin("approx_percentile_combine")(c)


def grouping(*cols: ColumnOrName) -> Column:
    """
    Describes which of a list of expressions are grouped in a row produced by a GROUP BY query.

    :func:`grouping_id` is an alias of :func:`grouping`.

    Example::
        >>> from pystarburst import GroupingSets
        >>> df = session.create_dataframe([[1, 2, 3], [4, 5, 6]],schema=["a", "b", "c"])
        >>> grouping_sets = GroupingSets([col("a")], [col("b")], [col("a"), col("b")])
        >>> df.group_by_grouping_sets(grouping_sets).agg([count("c"), grouping("a"), grouping("b"), grouping("a", "b")]).collect()
        [Row(A=1, B=2, COUNT(C)=1, GROUPING(A)=0, GROUPING(B)=0, GROUPING(A, B)=0), \
Row(A=4, B=5, COUNT(C)=1, GROUPING(A)=0, GROUPING(B)=0, GROUPING(A, B)=0), \
Row(A=1, B=None, COUNT(C)=1, GROUPING(A)=0, GROUPING(B)=1, GROUPING(A, B)=1), \
Row(A=4, B=None, COUNT(C)=1, GROUPING(A)=0, GROUPING(B)=1, GROUPING(A, B)=1), \
Row(A=None, B=2, COUNT(C)=1, GROUPING(A)=1, GROUPING(B)=0, GROUPING(A, B)=2), \
Row(A=None, B=5, COUNT(C)=1, GROUPING(A)=1, GROUPING(B)=0, GROUPING(A, B)=2)]
    """
    columns = [_to_col_if_str(c, "grouping") for c in cols]
    return builtin("grouping")(*columns)


def coalesce(*e: ColumnOrName) -> Column:
    """Returns the first non-NULL expression among its arguments, or NULL if all its
    arguments are NULL."""
    c = [_to_col_if_str(ex, "coalesce") for ex in e]
    return builtin("coalesce")(*c)


def equal_nan(e: ColumnOrName) -> Column:
    """Return true if the value in the column is not a number (NaN)."""
    c = _to_col_if_str(e, "equal_nan")
    return c.equal_nan()


def is_null(e: ColumnOrName) -> Column:
    """Return true if the value in the column is null."""
    c = _to_col_if_str(e, "is_null")
    return c.is_null()


def negate(e: ColumnOrName) -> Column:
    """Returns the negation of the value in the column (equivalent to a unary minus)."""
    c = _to_col_if_str(e, "negate")
    return -c


def not_(e: ColumnOrName) -> Column:
    """Returns the inverse of a boolean expression."""
    c = _to_col_if_str(e, "not_")
    return ~c


def random(m: Optional[Union[ColumnOrName, int]] = None, n: Optional[Union[ColumnOrName, int]] = None) -> Column:
    """Each call returns a pseudo-random value"""
    if m is None and n is None:
        return builtin("random")()
    if n is None:
        n = m
        m = 0
    m_col = lit(m) if isinstance(m, int) else _to_col_if_str(m, "random")
    n_col = lit(n) if isinstance(n, int) else _to_col_if_str(n, "random")
    return builtin("random")(m_col, n_col)


def div0(dividend: Union[ColumnOrName, int, float], divisor: Union[ColumnOrName, int, float]) -> Column:
    """Performs division like the division operator (/),
    but returns 0 when the divisor is 0 (rather than reporting an error)."""
    dividend_col = lit(dividend) if isinstance(dividend, (int, float)) else _to_col_if_str(dividend, "div0")
    divisor_col = lit(divisor) if isinstance(divisor, (int, float)) else _to_col_if_str(divisor, "div0")
    return builtin("coalesce")(builtin("try")(dividend_col / divisor_col), 0)


def sqrt(e: ColumnOrName) -> Column:
    """Returns the square-root of a non-negative numeric expression."""
    c = _to_col_if_str(e, "sqrt")
    return builtin("sqrt")(c)


def abs(e: ColumnOrName) -> Column:
    """Returns the absolute value of a numeric expression."""
    c = _to_col_if_str(e, "abs")
    return builtin("abs")(c)


def acos(e: ColumnOrName) -> Column:
    """Computes the inverse cosine (arc cosine) of its input;
    the result is a number in the interval [-pi, pi]."""
    c = _to_col_if_str(e, "acos")
    return builtin("acos")(c)


def acosh(e: ColumnOrName) -> Column:
    """Computes the inverse hyperbolic cosine of its input;
    the result is a number in the interval [-pi, pi]."""
    c = _to_col_if_str(e, "acosh")
    return builtin("acosh")(c)


def asin(e: ColumnOrName) -> Column:
    """Computes the inverse sine (arc sine) of its input;
    the result is a number in the interval [-pi, pi]."""
    c = _to_col_if_str(e, "asin")
    return builtin("asin")(c)


def atan(e: ColumnOrName) -> Column:
    """Computes the inverse tangent (arc tangent) of its input;
    the result is a number in the interval [-pi, pi]."""
    c = _to_col_if_str(e, "atan")
    return builtin("atan")(c)


def atan2(y: ColumnOrName, x: ColumnOrName) -> Column:
    """Computes the inverse tangent (arc tangent) of its input;
    the result is a number in the interval [-pi, pi]."""
    y_col = _to_col_if_str(y, "atan2")
    x_col = _to_col_if_str(x, "atan2")
    return builtin("atan2")(y_col, x_col)


def ceil(e: ColumnOrName) -> Column:
    """Returns values from the specified column rounded to the nearest equal or larger
    integer."""
    c = _to_col_if_str(e, "ceil")
    return builtin("ceil")(c)


def conv(e: ColumnOrName, from_base: int, to_base: int) -> Column:
    """Computes a number in the string form from one base to another."""
    c = _to_col_if_str(e, "conv")
    return builtin("to_base")(builtin("from_base")(c, from_base), to_base)


def cos(e: ColumnOrName) -> Column:
    """Computes the cosine of its argument; the argument should be expressed in radians."""
    c = _to_col_if_str(e, "cos")
    return builtin("cos")(c)


def cosh(e: ColumnOrName) -> Column:
    """Computes the hyperbolic cosine of its argument."""
    c = _to_col_if_str(e, "cosh")
    return builtin("cosh")(c)


def cot(e: ColumnOrName) -> Column:
    """Computes the cotangent of its argument."""
    c = _to_col_if_str(e, "cot")
    return 1 / builtin("tan")(c)


def csc(e: ColumnOrName) -> Column:
    """Computes the cosecant of its argument."""
    c = _to_col_if_str(e, "csc")
    return 1 / builtin("sin")(c)


def sec(e: ColumnOrName) -> Column:
    """Computes the secant of its argument."""
    c = _to_col_if_str(e, "sec")
    return 1 / builtin("cos")(c)


def cbrt(e: ColumnOrName) -> Column:
    """Computes the cube root of its argument."""
    c = _to_col_if_str(e, "cbrt")
    return builtin("cbrt")(c)


def exp(e: ColumnOrName) -> Column:
    """Computes Euler's number e raised to a floating-point value."""
    c = _to_col_if_str(e, "exp")
    return builtin("exp")(c)


def expm1(e: ColumnOrName) -> Column:
    """Computes Euler's number e raised to a floating-point value minus one."""
    c = _to_col_if_str(e, "expm1")
    return builtin("exp")(c) - 1


def floor(e: ColumnOrName) -> Column:
    """Returns values from the specified column rounded to the nearest equal or
    smaller integer."""
    c = _to_col_if_str(e, "floor")
    return builtin("floor")(c)


def hypot(e: ColumnOrName, f: ColumnOrName) -> Column:
    """Returns sqrt(a^2 + b^2)."""
    a = _to_col_if_str(e, "hypot")
    b = _to_col_if_str(f, "hypot")
    return builtin("sqrt")(a * a + b * b)


def sin(e: ColumnOrName) -> Column:
    """Computes the sine of its argument; the argument should be expressed in radians."""
    c = _to_col_if_str(e, "sin")
    return builtin("sin")(c)


def sinh(e: ColumnOrName) -> Column:
    """Computes the hyperbolic sine of its argument."""
    c = _to_col_if_str(e, "sinh")
    return builtin("sinh")(c)


def signum(e: ColumnOrName) -> Column:
    """Computes the signum of its argument."""
    c = _to_col_if_str(e, "signum")
    return builtin("sign")(c)


def tan(e: ColumnOrName) -> Column:
    """Computes the tangent of its argument; the argument should be expressed in radians."""
    c = _to_col_if_str(e, "tan")
    return builtin("tan")(c)


def tanh(e: ColumnOrName) -> Column:
    """Computes the hyperbolic tangent of its argument."""
    c = _to_col_if_str(e, "tanh")
    return builtin("tanh")(c)


def degrees(e: ColumnOrName) -> Column:
    """Converts radians to degrees."""
    c = _to_col_if_str(e, "degrees")
    return builtin("degrees")(c)


def radians(e: ColumnOrName) -> Column:
    """Converts degrees to radians."""
    c = _to_col_if_str(e, "radians")
    return builtin("radians")(c)


def to_hex(e: ColumnOrName) -> Column:
    """Encodes binary into a hex string representation."""
    c = _to_col_if_str(e, "to_hex")
    return builtin("to_hex")(c)


def md5(e: ColumnOrName) -> Column:
    """Returns a 32-character hex-encoded string containing the 128-bit MD5 message digest."""
    c = _to_col_if_str(e, "md5").cast(BinaryType())
    return lower(to_hex(builtin("md5")(c)))


def sha1(e: ColumnOrName) -> Column:
    """Returns a 40-character hex-encoded string containing the 160-bit SHA-1 message digest."""
    c = _to_col_if_str(e, "sha1").cast(BinaryType())
    return lower(to_hex(builtin("sha1")(c)))


def sha2(e: ColumnOrName, num_bits: int) -> Column:
    """Returns a hex-encoded string containing the SHA-256 or SHA-512 message digest"""
    if num_bits in (0, 256):
        c = _to_col_if_str(e, "sha256").cast(BinaryType())
        return lower(to_hex(builtin("sha256")(c)))
    elif num_bits == 512:
        c = _to_col_if_str(e, "sha512").cast(BinaryType())
        return lower(to_hex(builtin("sha512")(c)))
    else:
        raise ValueError(f"Trino supports only SHA-256 and SHA-512, num_bits given: {num_bits}")


def crc32(e: ColumnOrName) -> Column:
    """Computes the CRC-32 of binary."""
    c = _to_col_if_str(e, "crc32").cast(BinaryType())
    return builtin("crc32")(c)


def xxhash64(e: ColumnOrName) -> Column:
    """Calculates the hash code of given columns using the 64-bit variant of the xxHash algorithm,
    and returns the result as a varbinary column.

    Example::

        >>> df = session.create_dataframe(['a'], schema=["a"])
        >>> df.select(xxhash64("a").alias("xxhash64")).collect()
        [Row(xxhash64=-3292477735350538661)]

    Args:
        e: The column or value to be hashed
    """
    c = _to_col_if_str(e, "xxhash64").cast(BinaryType())
    return builtin("from_big_endian_64")(builtin("xxhash64")(c))


def hash(e: ColumnOrName) -> Column:
    """Computes the 128-bit MurmurHash3 hash of binaryhash

    Example::

        >>> df = session.create_dataframe(['a'], schema=["a"])
        >>> df.select(xxhash64("a").alias("hash")).collect()
        [Row(hash=-3292477735350538661)]
    Args:
        e: The column or value to be hashed
    """
    c = _to_col_if_str(e, "hash").cast(BinaryType())
    return builtin("murmur3")(c)


def base64(e: ColumnOrName) -> Column:
    """Encodes binary into a base64 string representation."""
    c = _to_col_if_str(e, "base64").cast(BinaryType())
    return builtin("to_base64")(c)


def unbase64(e: ColumnOrName) -> Column:
    """Decodes a BASE64 encoded string column and returns it as a binary column."""
    c = _to_col_if_str(e, "unbase64")
    return builtin("from_base64")(c)


def codepoint(e: ColumnOrName) -> Column:
    """Returns the unicode code for the first character of a string. If the string is empty,
    a value of 0 is returned."""
    c = _to_col_if_str(e, "codepoint")
    return when(c == "", 0).otherwise(builtin("codepoint")(c.cast(StringType(1))))


def length(e: ColumnOrName) -> Column:
    """Returns the length of an input string or binary value. For strings,
    the length is the number of characters, and UTF-8 characters are counted as a
    single character. For binary, the length is the number of bytes."""
    c = _to_col_if_str(e, "length")
    return builtin("length")(c)


def octet_length(e: ColumnOrName) -> Column:
    """Calculates the byte length for the specified string column."""
    c = _to_col_if_str(e, "octet_length")
    return builtin("length")(c.cast(BinaryType()))


def bit_length(e: ColumnOrName) -> Column:
    """ "Calculates the bit length for the specified string column."""
    c = _to_col_if_str(e, "bit_length")
    return builtin("length")(c.cast(BinaryType())) * 8


def lower(e: ColumnOrName) -> Column:
    """Returns the input string with all characters converted to lowercase."""
    c = _to_col_if_str(e, "lower")
    return builtin("lower")(c)


def lpad(e: ColumnOrName, len: Union[Column, int], pad: ColumnOrName) -> Column:
    """Left-pads a string with characters from another string, or left-pads a
    binary value with bytes from another binary value."""
    c = _to_col_if_str(e, "lpad")
    p = _to_col_if_str(pad, "lpad")
    return builtin("lpad")(c, lit(len), p)


def ltrim(e: ColumnOrName, trim_string: Optional[ColumnOrName] = None) -> Column:
    """Removes leading characters, including whitespace, from a string."""
    c = _to_col_if_str(e, "ltrim")
    t = _to_col_if_str(trim_string, "ltrim") if trim_string is not None else None
    return builtin("ltrim")(c, t) if t is not None else builtin("ltrim")(c)


def rpad(e: ColumnOrName, len: Union[Column, int], pad: ColumnOrName) -> Column:
    """Right-pads a string with characters from another string, or right-pads a
    binary value with bytes from another binary value."""
    c = _to_col_if_str(e, "rpad")
    p = _to_col_if_str(pad, "rpad")
    return builtin("rpad")(c, lit(len), p)


def rtrim(e: ColumnOrName, trim_string: Optional[ColumnOrName] = None) -> Column:
    """Removes trailing characters, including whitespace, from a string."""
    c = _to_col_if_str(e, "rtrim")
    t = _to_col_if_str(trim_string, "rtrim") if trim_string is not None else None
    return builtin("rtrim")(c, t) if t is not None else builtin("rtrim")(c)


def repeat(s: ColumnOrName, n: Union[Column, int]) -> Column:
    """Builds a string by repeating the input for the specified number of times."""
    c = _to_col_if_str(s, "rtrim")
    repeat_array = builtin("repeat")(c, lit(n))
    return builtin("array_join")(repeat_array, "")


def reverse(col: ColumnOrName) -> Column:
    """Returns a reversed string or an array with reverse order of elements.

    Example::

        >>> df = session.create_dataframe([["Hello"], ["abc"]], schema=["col1"])
        >>> df.select(reverse(col("col1"))).show()
        -----------------------
        |"reverse(col1)"      |
        -----------------------
        |olleH                |
        |cba                  |
        -----------------------
        <BLANKLINE>

        >>> df = session.createDataFrame([([2, 1, 3],) ,([1],) ,([],)], ['data'])
        >>> res = df.select(reverse(df.data).alias('r')).collect()
        [Row(r=[3, 1, 2]), Row(r=[1]), Row(r=[])]
    """
    col = _to_col_if_str(col, "reverse")
    return builtin("reverse")(col)


def soundex(e: ColumnOrName) -> Column:
    """Returns a string that contains a phonetic representation of the input string."""
    c = _to_col_if_str(e, "soundex")
    return builtin("soundex")(c)


def trim(e: ColumnOrName, trim_string: Optional[ColumnOrName] = None) -> Column:
    """Removes leading and trailing characters from a string."""
    c = _to_col_if_str(e, "trim")
    t = _to_col_if_str(trim_string, "trim") if trim_string is not None else None
    return builtin("trim")(c, t) if t is not None else builtin("trim")(c)


def upper(e: ColumnOrName) -> Column:
    """Returns the input string with all characters converted to uppercase."""
    c = _to_col_if_str(e, "upper")
    return builtin("upper")(c)


def initcap(e: ColumnOrName) -> Column:
    """Translate the first letter of each word to upper case in the sentence."""
    c = _to_col_if_str(e, "initcap")
    return builtin("regexp_replace")(c, "(\\w)(\\w*)", sql_expr("x -> upper(x[1]) || lower(x[2])"))


def strpos(e: ColumnOrName, substring: ColumnOrLiteral, instance: Union[int, ColumnOrName]):
    """Returns the position of the N-th instance of substring in string.
    When instance is a negative number the search will start from the end of string.
    Positions start with 1. If not found, 0 is returned."""
    c = _to_col_if_str(e, "strpos")
    sub = lit(substring)
    inst = _to_col_if_str_or_int(instance, "strpos")
    return builtin("strpos")(c, sub, inst)


def instr(e: ColumnOrName, substring: ColumnOrLiteral) -> Column:
    """Locate the position of the first occurrence of substr column in the given string. Returns null if either of the arguments are null."""
    return strpos(e, substring, 1)


def hex(e: ColumnOrName) -> Column:
    """Computes the hex value of the given column."""
    c = _to_col_if_str(e, "hex")
    return builtin("to_hex")(c.cast(BinaryType()))


def unhex(e: ColumnOrName) -> Column:
    """Computes each pair of characters as a hexadecimal number and converts to the byte representation of number."""
    c = _to_col_if_str(e, "unhex")
    return builtin("from_hex")(c)


def levenshtein_distance(l: ColumnOrName, r: ColumnOrLiteral) -> Column:
    """Computes the Levenshtein distance of the two given strings."""
    left = _to_col_if_str(l, "levenshtein")
    right = lit(r)
    return builtin("levenshtein_distance")(left, right)


def locate(substring: ColumnOrLiteral, e: ColumnOrName, pos: Union[ColumnOrName, int] = 1) -> Column:
    """Locate the position of the first occurrence of substr in a string column, after position pos."""
    p = _to_col_if_str_or_int(pos, "locate")
    rest = substr(e, pos)
    rest_pos = strpos(rest, substring, 1)
    return builtin("if")(p == 1, strpos(e, substring, 1), builtin("if")(rest_pos != 0, rest_pos + pos - 1, rest_pos))


def log(base: Union[ColumnOrName, int, float], x: Union[ColumnOrName, int, float]) -> Column:
    """Returns the logarithm of a numeric expression."""
    b = lit(base) if isinstance(base, (int, float)) else _to_col_if_str(base, "log")
    arg = lit(x) if isinstance(x, (int, float)) else _to_col_if_str(x, "log")
    return builtin("log")(b, arg)


def log10(x: Union[ColumnOrName, int, float]) -> Column:
    """Returns the logarithm in base 10 of a numeric expression."""
    arg = lit(x) if isinstance(x, (int, float)) else _to_col_if_str(x, "log10")
    return builtin("log10")(arg)


def log1p(x: Union[ColumnOrName, int, float]) -> Column:
    """Returns the logarithm of a numeric expression plus one."""
    arg = lit(x) if isinstance(x, (int, float)) else _to_col_if_str(x, "log1p")
    return builtin("ln")(arg + 1)


def log2(x: Union[ColumnOrName, int, float]) -> Column:
    """Returns the base 2 logarithm of a numeric expression."""
    arg = lit(x) if isinstance(x, (int, float)) else _to_col_if_str(x, "log2")
    return builtin("log2")(arg)


def pow(left: Union[ColumnOrName, int, float], right: Union[ColumnOrName, int, float]) -> Column:
    """Returns a number (left) raised to the specified power (right)."""
    number = lit(left) if isinstance(left, (int, float)) else _to_col_if_str(left, "pow")
    power = lit(right) if isinstance(right, (int, float)) else _to_col_if_str(right, "pow")
    return builtin("pow")(number, power)


def round(e: ColumnOrName, scale: Union[ColumnOrName, int, float] = 0) -> Column:
    """Returns values from the specified column rounded to the nearest equal or
    smaller integer."""
    c = _to_col_if_str(e, "round")
    scale_col = lit(scale) if isinstance(scale, (int, float)) else _to_col_if_str(scale, "round")
    return builtin("round")(c, scale_col)


def split(
    str: ColumnOrName,
    pattern: ColumnOrLiteralStr,
) -> Column:
    """Splits a given string with a given separator and returns the result in an array
    of strings. To specify a string separator, use the :func:`lit()` function."""
    s = _to_col_if_str(str, "split")
    pat = lit(pattern)
    return builtin("regexp_split")(s, pat)


def substring(str: ColumnOrName, pos: Union[Column, int], len: Optional[Union[Column, int]] = None) -> Column:
    """Returns the portion of the string or binary value str, starting from the
    character/byte specified by pos, with limited length. The length should be greater
    than or equal to zero. If the length is a negative number, the function returns an
    empty string.

    Note:
        For ``pos``, 1 is the first character of the string in Trino

    :func:`substr` is an alias of :func:`substring`.
    """
    s = _to_col_if_str(str, "substring")
    p = pos if isinstance(pos, Column) else lit(pos)
    if len is None:
        return builtin("substr")(s, p)
    length = len if isinstance(len, Column) else lit(len)
    return builtin("substr")(s, p, length)


substr = substring


def substring_index(str: ColumnOrName, delim: ColumnOrLiteral, count: Union[Column, int]) -> Column:
    """Returns the substring from string str before count occurrences of the delimiter delim. If count is positive,
    everything the left of the final delimiter (counting from left) is returned.

    If count is negative, every to the right of the final delimiter (counting from the right) is returned.
    substring_index performs a case-sensitive match when searching for delim."""
    s = _to_col_if_str(str, "substring_index")
    c = lit(count)
    pos = strpos(str, delim, count)
    substring_index_impl = builtin("if")(c > 0, substring(str, 1, pos - 1), substring(str, pos + 1))
    return builtin("if")(pos == 0, s, substring_index_impl)


def format_string(format: str, *e: ColumnOrName) -> Column:
    """Formats the arguments in printf-style and returns the result as a string column."""
    c = [_to_col_if_str(ex, "format_string") for ex in e]
    return builtin("format")(format, *c)


def overlay(e: ColumnOrName, replace: ColumnOrLiteral, pos: Union[Column, int], len: Union[Column, int] = -1) -> Column:
    """Overlay the specified portion of src with replace, starting from byte position pos of src and proceeding for len bytes."""
    p = _to_col_if_str_or_int(pos, "overlay")
    l = _to_col_if_str_or_int(len, "overlay")
    r = lit(replace)
    prefix_pos = substr(e, 1, p - 1)
    prefix_neg = substr(e, 1, length(e) + p)
    prefix = builtin("if")(p >= 0, prefix_pos, prefix_neg)
    r_length = builtin("if")(l == -1, length(r), len)
    suffix_pos = substr(e, p + r_length)
    suffix_neg = substr(e, length(e) + p + r_length)
    suffix = builtin("if")(p >= 0, suffix_pos, suffix_neg)
    return concat(prefix, r, suffix)


def regexp_count(
    subject: ColumnOrName,
    pattern: ColumnOrLiteralStr,
) -> Column:
    """Returns the number of times that a pattern occurs in the subject."""
    sql_func_name = "regexp_count"
    sub = _to_col_if_str(subject, sql_func_name)
    pat = lit(pattern)

    return builtin(sql_func_name)(sub, pat)


def regexp_extract(
    subject: ColumnOrName,
    pattern: ColumnOrLiteralStr,
    group: Optional[Union[Column, int]] = 0,
) -> Column:
    """Finds the first occurrence of the regular expression pattern
    in string and returns the capturing group number group"""
    sql_func_name = "regexp_extract"
    sub = _to_col_if_str(subject, sql_func_name)
    pat = lit(pattern)
    group = lit(group)

    return builtin(sql_func_name)(sub, pat, group)


def regexp_replace(
    subject: ColumnOrName,
    pattern: ColumnOrLiteralStr,
    replacement: ColumnOrLiteralStr = "",
) -> Column:
    """Returns the subject with the specified pattern (or all occurrences of the pattern) either removed or replaced by a replacement string.
    If no matches are found, returns the original subject.
    """
    sql_func_name = "regexp_replace"
    sub = _to_col_if_str(subject, sql_func_name)
    pat = lit(pattern)
    rep = lit(replacement)
    return builtin(sql_func_name)(sub, pat, rep)


def replace(
    subject: ColumnOrName,
    pattern: ColumnOrLiteralStr,
    replacement: ColumnOrLiteralStr = "",
) -> Column:
    """
    Removes all occurrences of a specified subject and optionally replaces them with replacement.
    """
    sql_func_name = "replace"
    sub = _to_col_if_str(subject, sql_func_name)
    pat = lit(pattern)
    rep = lit(replacement)
    return builtin(sql_func_name)(sub, pat, rep)


def concat(*cols: ColumnOrName) -> Column:
    """Concatenates one or more strings, binary values, arrays. If any of the values is null, the result is also null.

    Args::
        cols: A list of the columns to concatenate.

    Example::
        >>> df = session.createDataFrame([('abcd','123')], ['s', 'd'])
        >>> df = df.select(concat(df.s, df.d).alias('s'))
        >>> df.collect()
        [Row(s='abcd123')]

        >>> df = session.createDataFrame([([1, 2], [3, 4], [5]), ([1, 2], None, [3])], ['a', 'b', 'c'])
        >>> df = df.select(concat(df.a, df.b, df.c).alias("arr"))
        >>> df.collect()
        [Row(arr=[1, 2, 3, 4, 5]), Row(arr=None)]
    """
    columns = [_to_col_if_str(c, "concat") for c in cols]
    return builtin("concat")(*columns)


def concat_ws(*cols: ColumnOrName) -> Column:
    """Concatenates two or more strings, or concatenates two or more binary values. If any of the values is null, the result is also null.
    The CONCAT_WS operator requires at least two arguments, and uses the first argument to separate all following arguments."""
    columns = [_to_col_if_str(c, "concat_ws") for c in cols]
    return builtin("concat_ws")(*columns)


def translate(
    src: ColumnOrName,
    matching_string: ColumnOrName,
    replace_string: ColumnOrName,
) -> Column:
    """Translates src from the characters in matchingString to the characters in
    replaceString."""
    source = _to_col_if_str(src, "translate")
    match = _to_col_if_str(matching_string, "translate")
    replace = _to_col_if_str(replace_string, "translate")
    return builtin("translate")(source, match, replace)


def contains(col: ColumnOrName, string: ColumnOrName) -> Column:
    """Returns true if col contains str."""
    c = _to_col_if_str(col, "contains")
    s = _to_col_if_str(string, "contains")
    return strpos(c, s, 1).cast("boolean")


def starts_with(col: ColumnOrName, str: ColumnOrName) -> Column:
    """Returns true if col starts with str."""
    c = _to_col_if_str(col, "starts_with")
    s = _to_col_if_str(str, "starts_with")
    return builtin("starts_with")(c, s)


def ends_with(col: ColumnOrName, str: ColumnOrName) -> Column:
    """Returns true if col starts with str."""
    c = _to_col_if_str(col, "starts_with")
    s = _to_col_if_str(str, "starts_with")
    return starts_with(builtin("reverse")(c), builtin("reverse")(s))


def to_time(e: ColumnOrName, fmt: Optional["Column"] = None) -> Column:
    """Converts an input expression into the corresponding time."""
    if fmt is None:
        fmt = "hh24:mm:ss"
    c = _to_col_if_str(e, "to_time")
    return builtin("to_time")(c, fmt) if fmt is not None else builtin("to_time")(c)


def to_timestamp(e: ColumnOrName, fmt: Optional["Column"] = None) -> Column:
    """Converts an input expression into the corresponding timestamp."""
    if fmt is None:
        fmt = "yyyy-mm-dd hh24:mi:ss"
    c = _to_col_if_str(e, "to_timestamp")
    return iff(
        starts_with(typeof(c), lit("varchar")), builtin("to_timestamp")(c.cast(StringType()), fmt), c.cast(TimestampNTZType())
    )


def to_date(e: ColumnOrName, fmt: Optional["Column"] = None) -> Column:
    """Converts an input expression into a date."""
    if fmt is None:
        fmt = "yyyy-mm-dd"
    c = _to_col_if_str(e, "to_date")
    return builtin("to_date")(c, fmt) if fmt is not None else builtin("to_date")(c)


def current_timestamp(precision: Optional[int] = None) -> Column:
    """Returns the current timestamp for the system."""
    if precision is None:
        return sql_expr("current_timestamp")
    return builtin("current_timestamp")(precision)


def current_date() -> Column:
    """Returns the current date for the system."""
    return sql_expr("current_date")


def current_time() -> Column:
    """Returns the current time for the system."""
    return sql_expr("current_time")


def current_timezone() -> Column:
    """Returns the current time zone for the system."""
    return builtin("current_timezone")()


def hour(e: ColumnOrName) -> Column:
    """
    Extracts the hour from a date or timestamp.

    Example::

        >>> import datetime
        >>> df = session.create_dataframe([
        ...     datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f"),
        ...     datetime.datetime.strptime("2020-08-21 01:30:05.000", "%Y-%m-%d %H:%M:%S.%f")
        ... ], schema=["a"])
        >>> df.select(hour("a")).collect()
        [Row(HOUR("A")=13), Row(HOUR("A")=1)]
    """
    c = _to_col_if_str(e, "hour")
    return builtin("hour")(c)


def minute(e: ColumnOrName) -> Column:
    """
    Extracts the minute from a date or timestamp.

    Example::

        >>> import datetime
        >>> df = session.create_dataframe([
        ...     datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f"),
        ...     datetime.datetime.strptime("2020-08-21 01:30:05.000", "%Y-%m-%d %H:%M:%S.%f")
        ... ], schema=["a"])
        >>> df.select(minute("a")).collect()
        [Row(MINUTE("A")=11), Row(MINUTE("A")=30)]
    """
    c = _to_col_if_str(e, "minute")
    return builtin("minute")(c)


def second(e: ColumnOrName) -> Column:
    """
    Extracts the second from a date or timestamp.

    Example::

        >>> import datetime
        >>> df = session.create_dataframe([
        ...     datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f"),
        ...     datetime.datetime.strptime("2020-08-21 01:30:05.000", "%Y-%m-%d %H:%M:%S.%f")
        ... ], schema=["a"])
        >>> df.select(second("a")).collect()
        [Row(SECOND("A")=20), Row(SECOND("A")=5)]
    """
    c = _to_col_if_str(e, "second")
    return builtin("second")(c)


def month(e: ColumnOrName) -> Column:
    """
    Extracts the month from a date or timestamp.


    Example::

        >>> import datetime
        >>> df = session.create_dataframe([
        ...     datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f"),
        ...     datetime.datetime.strptime("2020-08-21 01:30:05.000", "%Y-%m-%d %H:%M:%S.%f")
        ... ], schema=["a"])
        >>> df.select(month("a")).collect()
        [Row(MONTH("A")=5), Row(MONTH("A")=8)]
    """
    c = _to_col_if_str(e, "month")
    return builtin("month")(c)


def quarter(e: ColumnOrName) -> Column:
    """
    Extracts the quarter from a date or timestamp.

    Example::

        >>> import datetime
        >>> df = session.create_dataframe([
        ...     datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f"),
        ...     datetime.datetime.strptime("2020-08-21 01:30:05.000", "%Y-%m-%d %H:%M:%S.%f")
        ... ], schema=["a"])
        >>> df.select(quarter("a")).collect()
        [Row(QUARTER("A")=2), Row(QUARTER("A")=3)]
    """
    c = _to_col_if_str(e, "quarter")
    return builtin("quarter")(c)


def year(e: ColumnOrName) -> Column:
    """
    Extracts the year from a date or timestamp.

    Example::

        >>> import datetime
        >>> df = session.create_dataframe([
        ...     datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f"),
        ...     datetime.datetime.strptime("2020-08-21 01:30:05.000", "%Y-%m-%d %H:%M:%S.%f")
        ... ], schema=["a"])
        >>> df.select(year("a")).collect()
        [Row(YEAR("A")=2020), Row(YEAR("A")=2020)]
    """
    c = _to_col_if_str(e, "year")
    return builtin("year")(c)


def day(e: ColumnOrName) -> Column:
    """
    Extracts the day from a date or timestamp.

    Example::

        >>> import datetime
        >>> df = session.create_dataframe([
        ...     datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f"),
        ...     datetime.datetime.strptime("2020-08-21 01:30:05.000", "%Y-%m-%d %H:%M:%S.%f")
        ... ], schema=["a"])
        >>> df.select(day("a")).collect()
        [Row(day("a")=1), Row(day("a")=21)]
    """
    c = _to_col_if_str(e, "day")
    return builtin("day")(c)


def arrays_overlap(array1: ColumnOrName, array2: ColumnOrName) -> Column:
    """Compares whether two ARRAYs have at least one element in common. Returns TRUE
    if there is at least one element in common; otherwise returns FALSE. The function
    is NULL-safe, meaning it treats NULLs as known values for comparing equality."""
    a1 = _to_col_if_str(array1, "arrays_overlap")
    a2 = _to_col_if_str(array2, "arrays_overlap")
    return builtin("arrays_overlap")(a1, a2)


def array_distinct(col: ColumnOrName):
    """Remove duplicate values from the array.

    Args:
        col: The array column

    Returns:
        Returns a new ARRAY that contains only the distinct elements from the input ARRAY.

    Example::

        >>> from pystarburst.functions import array_construct,array_distinct,lit
        >>> df = session.createDataFrame([["1"]], ["A"])
        >>> df = df.withColumn("array", array_construct(lit(1), lit(1), lit(1), lit(2), lit(3), lit(2), lit(2)))
        >>> df.withColumn("array_d", array_distinct("ARRAY")).show()
        |"a"  |"array"                |"array_d"  |
        -------------------------------------------
        |1    |[1, 1, 1, 2, 3, 2, 2]  |[1, 2, 3]  |
        -------------------------------------------
        <BLANKLINE>
    """
    col = _to_col_if_str(col, "array_distinct")
    return builtin("array_distinct")(col)


def array_intersect(array1: ColumnOrName, array2: ColumnOrName) -> Column:
    """Returns an array that contains the matching elements in the two input arrays.

    The function is NULL-safe, meaning it treats NULLs as known values for comparing equality.

    Args:
        array1: An ARRAY that contains elements to be compared.
        array2: An ARRAY that contains elements to be compared."""
    a1 = _to_col_if_str(array1, "array_intersect")
    a2 = _to_col_if_str(array2, "array_intersect")
    return builtin("array_intersect")(a1, a2)


def array_union(array1: ColumnOrName, array2: ColumnOrName) -> Column:
    """Returns an array of the elements in the union of array1 and array2, without duplicates.

    Example::

        >>> from pystarburst import Row
        >>> df = session.createDataFrame([Row(c1=["b", "a", "c"], c2=["c", "d", "a", "f"])])
        >>> df.select(array_union(df.c1, df.c2)).collect()
        [Row(array_union(c1, c2)=['b', 'a', 'c', 'd', 'f'])]
    """
    a1 = _to_col_if_str(array1, "array_union")
    a2 = _to_col_if_str(array2, "array_union")
    return builtin("array_union")(a1, a2)


def array_except(array1: ColumnOrName, array2: ColumnOrName) -> Column:
    """Returns an array of elements in array1 but not in array2, without duplicates.

    Example::

        >>> from pystarburst import Row
        >>> df = session.createDataFrame([Row(c1=["b", "a", "c"], c2=["c", "d", "a", "f"])])
        >>> df.select(array_except(df.c1, df.c2)).collect()
        [Row(array_except(c1, c2)=['b'])]
    """
    a1 = _to_col_if_str(array1, "array_except")
    a2 = _to_col_if_str(array2, "array_except")
    return builtin("array_except")(a1, a2)


def array_min(array: ColumnOrName) -> Column:
    """Returns the minimum value of input array. Null values are omitted.

    Example::
        >>> df = session.createDataFrame([([2, 1, 3],), ([None, 10, -1],)], ['data'])
        >>> df.select(array_min(df.data).alias('min')).collect()
        [Row(min=1), Row(min=-1)]
    """
    a = _to_col_if_str(array, "array_min")
    a_wo_nulls = array_except(a, lit([None]))
    return builtin("array_min")(a_wo_nulls)


def array_max(array: ColumnOrName) -> Column:
    """Returns the maximum value of input array. Null values are omitted.

    Example::
        >>> df = session.createDataFrame([([2, 1, 3],), ([None, 10, -1],)], ['data'])
        >>> df.select(array_max(df.data).alias('max')).collect()
        [Row(max=3), Row(max=10)]
    """
    a = _to_col_if_str(array, "array_max")
    a_wo_nulls = array_except(a, lit([None]))
    return builtin("array_max")(a_wo_nulls)


def flatten(array: ColumnOrName) -> Column:
    """Returns a single array from an array of arrays. If the array is nested more than
    two levels deep, then only a single level of nesting is removed.

    Args:
        array: the input array

    Example::
        >>> df = session.createDataFrame([([[1, 2, 3], [4, 5], [6]],), ([None, [4, 5]],)], ['data'])
        >>> df.select(flatten(df.data)).show()
        ----------------------
        |"flatten(data)"     |
        ----------------------
        |[1, 2, 3, 4, 5, 6]  |
        |[4, 5]              |
        ----------------------
    """
    array = _to_col_if_str(array, "flatten")
    return builtin("flatten")(array)


def sort_array(array: ColumnOrName, sort_ascending: Optional[bool] = True) -> Column:
    """Returns rows of array column in sorted order. Users can choose the sort order.

    Args:
        array: name of the column or column element which describes the column
        sort_ascending: Boolean that decides if array elements are sorted in ascending order.
            Defaults to True.

    Examples::
        >>> df = session.sql("select array[20, 0, null, 10] as a")
        >>> df.select(sort_array(df.a).as_("sorted_a")).show()
        ---------------------
        |"sorted_a"         |
        ---------------------
        |[0, 10, 20, None]  |
        ---------------------
        <BLANKLINE>
        >>> df.select(sort_array(df.a, False).as_("sorted_a")).show()
        ---------------------
        |"sorted_a"         |
        ---------------------
        |[None, 20, 10, 0]  |
        ---------------------
        <BLANKLINE>"""

    array = _to_col_if_str(array, "sort_array")

    if sort_ascending:
        return builtin("array_sort")(array)
    else:
        return reverse(builtin("array_sort")(array))


def shuffle(array: ColumnOrName) -> Column:
    """
    Generates a random permutation of the given array.

    Args:
        array: The column containing the source ARRAY.

    Examples::
        >>> df = spark.createDataFrame([([1, 20, 3, 5],), ([1, 20, None, 3],)], ['data'])
        >>> df.select(shuffle(df.data).alias('s')).collect()
        [Row(s=[3, 1, 5, 20]), Row(s=[20, None, 3, 1])]
    """

    a = _to_col_if_str(array, "shuffle")
    return builtin("shuffle")(a)


def sequence(start: ColumnOrName, stop: ColumnOrName, step: Optional[ColumnOrName] = None) -> Column:
    """Generate a sequence of integers from `start` to `stop`, incrementing by `step`.
    If `step` is not set, incrementing by 1 if start is less than or equal to stop, otherwise -1.

    Args:
        start: the column that contains the integer to start with (inclusive).
        stop: the column that contains the integer to stop (inclusive).
        step: the column that contains the integer to increment.

    Example::
        >>> df1 = session.create_dataframe([(-2, 2)], ["a", "b"])
        >>> df1.select(sequence("a", "b").alias("result")).show()
        ---------------------
        |"result"           |
        ---------------------
        |[-2, -1, 0, 1, 2]  |
        ---------------------
        <BLANKLINE>
        >>> df2 = session.create_dataframe([(4, -4, -2)], ["a", "b", "c"])
        >>> df2.select(sequence("a", "b", "c").alias("result")).show()
        ---------------------
        |"result"           |
        ---------------------
        |[4, 2, 0, -2, -4]  |
        ---------------------
        <BLANKLINE>
    """
    start_col = _to_col_if_str(start, "sequence")
    stop_col = _to_col_if_str(stop, "sequence")
    if step is None:
        return builtin("sequence")(start_col, stop_col)
    else:
        step_col = _to_col_if_str(step, "sequence")
        return builtin("sequence")(start_col, stop_col, step_col)


def array_repeat(element: ColumnOrName, count: Union[ColumnOrName, int]) -> Column:
    """Creates an array containing an element repeated count times."""
    e = _to_col_if_str(element, "array_repeat")
    c = _to_col_if_str_or_int(count, "array_repeat")
    return builtin("repeat")(e, c)


def arrays_zip(*columns: ColumnOrName) -> Column:
    """Merges the given arrays, element-wise, into a single array of rows.
    The M-th element of the N-th argument will be the N-th field of the M-th output element.
    If the arguments have an uneven length, missing values are filled with NULL.
    Currently, this function accepts at most 5 arrays (limitation of Trino `zip` function).
    """
    c = [_to_col_if_str(arr, "zip") for arr in columns]
    return builtin("zip")(*c)


def datediff(part: str, col1: ColumnOrName, col2: ColumnOrName) -> Column:
    """Calculates the difference between two date, time, or timestamp columns based on the date or time part requested.

    `Supported date and time parts <https://trino.io/docs/current/functions/datetime.html?highlight=date_diff#date_diff>`_

    Example::

        >>> # year difference between two date columns
        >>> import datetime
        >>> date_df = session.create_dataframe([[datetime.date(2020, 1, 1), datetime.date(2021, 1, 1)]], schema=["date_col1", "date_col2"])
        >>> date_df.select(datediff("year", col("date_col1"), col("date_col2")).alias("year_diff")).show()
        ---------------
        |"YEAR_DIFF"  |
        ---------------
        |1            |
        ---------------
        <BLANKLINE>

    Args:
        part: The time part to use for calculating the difference
        col1: The first timestamp column or minuend in the datediff
        col2: The second timestamp column or the subtrahend in the datediff
    """
    if not isinstance(part, str):
        raise ValueError("part must be a string")
    c1 = _to_col_if_str(col1, "date_diff")
    c2 = _to_col_if_str(col2, "date_diff")
    return builtin("date_diff")(part, c1, c2)


def trunc(e: ColumnOrName, scale: Union[ColumnOrName, int, float] = 0) -> Column:
    """Rounds the input expression down to the nearest (or equal) integer closer to zero,
    or to the nearest equal or smaller value with the specified number of
    places after the decimal point."""
    c = _to_col_if_str(e, "trunc")
    scale_col = lit(scale) if isinstance(scale, (int, float)) else _to_col_if_str(scale, "trunc")
    return builtin("trunc")(c, scale_col)


def date_add(col: ColumnOrName, days: Union[ColumnOrName, int]) -> Column:
    """Adds the specified value in days from the specified date.

    `Supported date and time parts <https://trino.io/docs/current/functions/datetime.html#date_add>`_

    Example::

        >>> # add 24 days on dates
        >>> import datetime
        >>> date_df = session.create_dataframe([[datetime.date(2020, 10, 20)]], schema=["date_col"])
        >>> date_df.select(date_add(col("date_col"), lit(24)).alias("date")).show()
        ----------------
        |"DATE"        |
        ----------------
        |2020-11-13    |
        ----------------
        <BLANKLINE>

    Args:
        col: The timestamp column
        days: The number of days to add
    """
    c = _to_col_if_str(col, "date_add")
    d = _to_col_if_str_or_int(days, "date_add")
    return builtin("date_add")("day", d, c)


def date_format(col: ColumnOrName, date_time_format: str) -> Column:
    """Format string that is compatible with JodaTime’s DateTimeFormat pattern format.

    `Supported date and time parts <https://trino.io/docs/current/functions/datetime.html#format_datetime>`_

    Example::

        >>> # add one year on dates
        >>> import datetime
        >>> date_df = session.create_dataframe([[datetime.date(2020, 1, 1)]], schema=["date_col"])
        >>> date_df.select(date_format(col("date_col"), "YYYY/MM/dd").alias("date")).show()
        ----------------
        |"DATE"        |
        ----------------
        |"2021/01/01"  |
        ----------------
        <BLANKLINE>

    Args:
        col: The timestamp column
        date_time_format: The format string
    """
    if not isinstance(date_time_format, str):
        raise ValueError("part must be a string")
    c = _to_col_if_str(col, "format_datetime")
    return builtin("format_datetime")(c, date_time_format)


def date_sub(col: ColumnOrName, days: Union[ColumnOrName, int]) -> Column:
    """Subtracts the specified value in days from the specified date.

    `Supported date and time parts <https://trino.io/docs/current/functions/datetime.html#date_add>`_

    Example::

        >>> # subtracts 24 days on dates
        >>> import datetime
        >>> date_df = session.create_dataframe([[datetime.date(2020, 10, 20)]], schema=["date_col"])
        >>> date_df.select(date_sub(col("date_col"), lit(24)).alias("date")).show()
        ----------------
        |"DATE"        |
        ----------------
        |2020-09-26    |
        ----------------
        <BLANKLINE>

    Args:
        col: The timestamp column
        days: The number of days to subtract
    """
    c = _to_col_if_str(col, "date_add")
    d = _to_col_if_str_or_int(days, "date_add")
    return builtin("date_add")("day", -d, c)


def date_trunc(part: str, expr: ColumnOrName) -> Column:
    """
    Truncates a DATE, TIME, or TIMESTAMP to the specified precision.

    Note that truncation is not the same as extraction. For example:
    - Truncating a timestamp down to the quarter returns the timestamp corresponding to midnight of the first day of the
    quarter for the input timestamp.
    - Extracting the quarter date part from a timestamp returns the quarter number of the year in the timestamp.

    Example::
        >>> import datetime
        >>> df = session.create_dataframe(
        ...     [[datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f")]],
        ...     schema=["a"],
        ... )
        >>> df.select(date_trunc("YEAR", "a"), date_trunc("MONTH", "a"), date_trunc("DAY", "a")).collect()
        [Row(DATE_TRUNC("YEAR", "A")=datetime.datetime(2020, 1, 1, 0, 0), DATE_TRUNC("MONTH", "A")=datetime.datetime(2020, 5, 1, 0, 0), DATE_TRUNC("DAY", "A")=datetime.datetime(2020, 5, 1, 0, 0))]
        >>> df.select(date_trunc("HOUR", "a"), date_trunc("MINUTE", "a"), date_trunc("SECOND", "a")).collect()
        [Row(DATE_TRUNC("HOUR", "A")=datetime.datetime(2020, 5, 1, 13, 0), DATE_TRUNC("MINUTE", "A")=datetime.datetime(2020, 5, 1, 13, 11), DATE_TRUNC("SECOND", "A")=datetime.datetime(2020, 5, 1, 13, 11, 20))]
        >>> df.select(date_trunc("QUARTER", "a")).collect()
        [Row(DATE_TRUNC("QUARTER", "A")=datetime.datetime(2020, 4, 1, 0, 0))]
    """
    expr_col = _to_col_if_str(expr, "date_trunc")
    return builtin("date_trunc")(part, expr_col)


def dayofmonth(e: ColumnOrName) -> Column:
    """
    Extracts the corresponding day (number) of the month from a date or timestamp.

    Example::
        >>> import datetime
        >>> df = session.create_dataframe(
        ...     [[datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f")]],
        ...     schema=["a"],
        ... )
        >>> df.select(dayofmonth("a")).collect()
        [Row(day_of_month("A")=1)]
    """
    c = _to_col_if_str(e, "day_of_month")
    return builtin("day_of_month")(c)


def dayofweek(e: ColumnOrName) -> Column:
    """
    Extracts the corresponding day (number) of the week from a date or timestamp.

    Example::
        >>> import datetime
        >>> df = session.create_dataframe(
        ...     [[datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f")]],
        ...     schema=["a"],
        ... )
        >>> df.select(dayofweek("a")).collect()
        [Row(day_of_week("A")=5)]
    """
    c = _to_col_if_str(e, "day_of_week")
    return builtin("day_of_week")(c)


def dayofyear(e: ColumnOrName) -> Column:
    """
    Extracts the corresponding day (number) of the year from a date or timestamp.

    Example::
        >>> import datetime
        >>> df = session.create_dataframe(
        ...     [[datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f")]],
        ...     schema=["a"],
        ... )
        >>> df.select(dayofyear("a")).collect()
        [Row(day_of_year("A")=122)]
    """
    c = _to_col_if_str(e, "day_of_year")
    return builtin("day_of_year")(c)


def last_day(col: ColumnOrName) -> Column:
    """
    Returns the last day of the month which the given date belongs to.

    `Supported date and time parts <https://trino.io/docs/current/functions/datetime.html#last_day_of_month>`_

    Example::
        >>> import datetime
        >>> df = session.create_dataframe(
        ...     [[datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f")]],
        ...     schema=["a"],
        ... )
        >>> date_df.select(last_day(col("a")).alias("date")).show()
        ----------------
        |"DATE"        |
        ----------------
        |2020-05-31    |
        ----------------
        <BLANKLINE>

    Args:
        col: The timestamp column
    """
    c = _to_col_if_str(col, "last_day_of_month")
    return builtin("last_day_of_month")(c)


def weekofyear(e: ColumnOrName) -> Column:
    """
    Extracts the corresponding week (number) of the year from a date or timestamp.

    Example::

        >>> import datetime
        >>> df = session.create_dataframe(
        ...     [[datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f")]],
        ...     schema=["a"],
        ... )
        >>> df.select(weekofyear("a")).collect()
        [Row(WEEKOFYEAR("A")=18)]
    """
    c = _to_col_if_str(e, "week_of_year")
    return builtin("week_of_year")(c)


def trunc(col: ColumnOrName, trunc_format: ColumnOrLiteralStr) -> Column:
    """
    Truncates a DATE, TIME, or TIMESTAMP to the specified precision.

    Note that truncation is not the same as extraction. For example:
    - Truncating a timestamp down to the quarter returns the timestamp corresponding to midnight of the first day of the
    quarter for the input timestamp.
    - Extracting the quarter date part from a timestamp returns the quarter number of the year in the timestamp.

    Example::
        >>> import datetime
        >>> df = session.create_dataframe(
        ...     [[datetime.datetime.strptime("2020-05-01 13:11:20.000", "%Y-%m-%d %H:%M:%S.%f")]],
        ...     schema=["a"],
        ... )
        >>> df.select(trunc("YEAR", "a"), trunc("MONTH", "a")).collect()
        [Row(DATE_TRUNC("YEAR", "A")=datetime.date(2020, 1, 1), DATE_TRUNC("MONTH", "A")=datetime.datetime(2020, 5, 1)]

    Args:
        col: the date/time/timestamp column
        trunc_format: the truncation format
    """
    expr_col = _to_col_if_str(col, "trunc")
    expr_trunc_format = lit(trunc_format)
    return builtin("date_trunc")(expr_trunc_format, expr_col).cast("date")


def make_date(col_year: ColumnOrName, col_month: ColumnOrName, col_day: ColumnOrName) -> Column:
    """
    Generate a date from a year, month and day columns.

    Example::
        >>> import datetime
        >>> df = session.create_dataframe(
        ...     [[2020, 1, 30]],
        ...     schema=["a", "b", "c"],
        ... )
        >>> df.select(make_date("a", "b", "c")).collect()
        [Row(MAKE_DATE("A", "B", "C")=datetime.date(2020, 1, 30)]

    Args:
        col_year: The year column
        col_month: The month column
        col_day: The day column
    """
    expr_col_year = _to_col_if_str(col_year, "make_date")
    expr_col_month = _to_col_if_str(col_month, "make_date")
    expr_col_day = _to_col_if_str(col_day, "make_date")
    return builtin("date_parse")(builtin("format")("%d/%d/%d", expr_col_year, expr_col_month, expr_col_day), "%Y/%m/%d").cast(
        "date"
    )


def to_utc_timestamp(col: ColumnOrName, col_tz: ColumnOrLiteralStr) -> Column:
    """
    Takes a timestamp which is timezone-agnostic, and interprets it as a timestamp
    in the given timezone, and renders that timestamp as a timestamp in UTC.

    `Supported date and time parts <https://trino.io/docs/current/functions/datetime.html#with_timezone>`_

    Example::
        >>> df = session.create_dataframe(
        ...     [["1997-02-28 10:30:00", "Japan")]],
        ...     schema=["timestamp", "tz"],
        ... )
        >>> date_df.select(to_utc_timestamp(col("timestamp"), col("tz")).alias("datetime")).show()
        ------------------------
        |"DATETIME"            |
        ------------------------
        |1997-02-28 1:30:00 UTC|
        ------------------------
        <BLANKLINE>

    Args:
        col: The timestamp column
        col_tz: the timezone column
    """
    expr_col = _to_col_if_str(col, "to_utc_timestamp")
    expr_col_tz = lit(col_tz)
    return builtin("at_timezone")(builtin("with_timezone")(expr_col.cast("timestampntz"), expr_col_tz), "UTC")


def from_utc_timestamp(col: ColumnOrName, col_tz: ColumnOrLiteralStr) -> Column:
    """
    Takes a timestamp which is timezone-agnostic, and interprets it as a timestamp
    in UTC, and renders that timestamp as a timestamp in the given time zone.

    `Supported date and time parts <https://trino.io/docs/current/functions/datetime.html#with_timezone>`_

    Example::
        >>> df = session.create_dataframe(
        ...     [["1997-02-28 1:30:00", "Japan")]],
        ...     schema=["timestamp", "tz"],
        ... )
        >>> date_df.select(from_utc_timestamp(col("timestamp"), col("tz")).alias("datetime")).show()
        ---------------------------
        |"DATETIME"               |
        ---------------------------
        |1997-02-28 10:30:00 Japan|
        ---------------------------
        <BLANKLINE>

    Args:
        col: The timestamp column
        col_tz: the timezone column
    """
    expr_col = _to_col_if_str(col, "from_utc_timestamp")
    expr_col_tz = lit(col_tz)
    return builtin("at_timezone")(builtin("with_timezone")(expr_col.cast("timestampntz"), "UTC"), expr_col_tz)


def typeof(col: ColumnOrName) -> Column:
    """Reports the type of a value stored in a VARIANT column. The type is returned as a string."""
    c = _to_col_if_str(col, "typeof")
    return builtin("typeof")(c)


def json_extract(col: ColumnOrName, path: ColumnOrName) -> Column:
    """Parses a JSON string and returns the value of an element at a specified path in the resulting
    JSON document."""
    c = _to_col_if_str(col, "json_extract")
    p = _to_col_if_str(path, "json_extract")
    return builtin("json_extract")(c, p)


def json_parse(e: ColumnOrName) -> Column:
    """Parse the value of the specified column as a JSON string and returns the
    resulting JSON document."""
    c = _to_col_if_str(e, "json_parse")
    return builtin("json_parse")(c)


def array_agg(col: ColumnOrName, is_distinct: bool = False) -> Column:
    """Returns the input values, pivoted into an ARRAY. If the input is empty, an empty
    ARRAY is returned."""
    c = _to_col_if_str(col, "array_agg")
    return _call_function("array_agg", is_distinct, c)


def array_append(array: ColumnOrName, element: ColumnOrName) -> Column:
    """Returns an ARRAY containing all elements from the source ARRAY as well as the new element.
    The new element is located at end of the ARRAY.

    Args:
        array: The column containing the source ARRAY.
        element: The column containing the element to be appended.
            The data type does need to match the data type of the
            existing elements in the ARRAY."""
    a = _to_col_if_str(array, "array_append")
    e = _to_col_if_str(element, "array_append")
    return builtin("concat")(a, e)


def array_prepend(array: ColumnOrName, element: ColumnOrName) -> Column:
    """Returns an ARRAY containing the new element as well as all elements from the source ARRAY.
    The new element is positioned at the beginning of the ARRAY.

    Args:
        array: Column containing the source ARRAY.
        element: Column containing the element to be prepended.
            The data type does need to match the data type of the
            existing elements in the ARRAY.

    Example::
        >>> from pystarburst import Row
        >>> df = session.create_dataframe([Row(a=[1, 2, 3])])
        >>> df.select(array_prepend("a", lit(4)).alias("result")).show()
        ----------------
        |"result"      |
        ----------------
        |[4, 1, 2, 3]  |
        ----------------
        <BLANKLINE>
    """
    a = _to_col_if_str(array, "array_prepend")
    e = _to_col_if_str(element, "array_prepend")
    return builtin("concat")(e, a)


def array_compact(array: ColumnOrName) -> Column:
    """Returns a compacted ARRAY with missing and null values removed,
    effectively converting sparse arrays into dense arrays.

    Args:
        array: Column containing the source ARRAY to be compacted

    Example::
        >>> from pystarburst import Row
        >>> df = session.create_dataframe([Row(a=[1, None, 3])])
        >>> df.select("a", array_compact("a").alias("compacted")).show()
        ------------------------------
        |"a"           |"compacted"  |
        ------------------------------
        |[1, None, 3]  |[1, 3]       |
        ------------------------------
        <BLANKLINE>
    """
    a = _to_col_if_str(array, "array_compact")
    return builtin("filter")(a, sql_expr("x -> x IS NOT NULL"))


def array_construct(*args: ColumnOrLiteral) -> Column:
    """Creates a new array column.

    Args:
        args: Columns containing the values (or expressions that evaluate to values).

    Example::
        >>> df = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
        >>> df.select(array_construct("a", "b").alias("result")).show()
        ------------
        |"result"  |
        ------------
        |[1, 2]    |
        |[3, 4]    |
        ------------
        <BLANKLINE>
    """
    cols = [_to_col_if_str_or_int(arg, "array_construct") for arg in args]
    exprs = [Column._to_expr(col) for col in cols]
    return Column(ArrayExpression(elements=exprs))


def array_contains(array: ColumnOrName, element: ColumnOrName) -> Column:
    """Returns true if the array contains the element."""
    a = _to_col_if_str(array, "array_contains")
    e = _to_col_if_str(element, "array_contains")
    return builtin("contains")(a, e)


# TODO: Make consistent with PySpark behaviour:
#  Index above array size appends the array, or prepends the array if index is negative, with ‘null’ elements
#  https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.array_insert.html#pyspark.sql.functions.array_insert
def array_insert(array: ColumnOrName, pos: Union[ColumnOrName, int], element: ColumnOrName) -> Column:
    """Returns an ARRAY containing all elements from the source ARRAY as well as the new element.

    Args:
        array: Column containing the source ARRAY.
        pos: Column containing a (one-based) position in the source ARRAY.
            The new element is inserted at this position. The original element from this
            position (if any) and all subsequent elements (if any) are shifted by one position
            to the right in the resulting array (i.e. inserting at position 1 has the same
            effect as using array_prepend).
            A negative position is interpreted as an index from the back of the array (e.g.
            -1 results in insertion before the last element in the array).
        element: Column containing the element to be inserted. The new element is located at
            position pos. The relative order of the other elements from the source
            array is preserved.

    Example::
        >>> from pystarburst import Row
        >>> df = session.create_dataframe([Row([1, 2]), Row([1, 3])], schema=["a"])
        >>> df.select(array_insert("a", lit(1), lit(10)).alias("result")).show()
        --------------
        |"result"    |
        --------------
        |[10, 1, 2]  |
        |[10, 1, 3]  |
        --------------
        <BLANKLINE>
    """
    a = _to_col_if_str(array, "array_insert")
    p = _to_col_if_str_or_int(pos, "array_insert")
    e = _to_col_if_str(element, "array_insert")

    first_slice = builtin("if")(p > 0, array_slice(a, 1, p - 1), array_slice(a, 1, size(a) + p))
    last_slice = array_slice(a, p, size(a))

    return array_append(array_append(first_slice, e), last_slice)


def array_remove(array: ColumnOrName, element: Union[ColumnOrName, int, float]):
    """Remove all elements that equal element from array."""
    a = _to_col_if_str(array, "array_remove")
    e = lit(element) if isinstance(element, (int, float)) else _to_col_if_str(element, "array_remove")
    return builtin("array_remove")(a, e)


def element_at(col1: Union[ColumnOrName, int], col2: Union[ColumnOrName, int]) -> Column:
    """Returns element of array at given index or value for given key in map.
    Notice that Trino ARRAY indexing starts from 1.

    Example::

        >>> from pystarburst.functions import lit
        >>> df = session.createDataFrame([({"a": 1.0, "b": 2.0}, [1, 2, 3],), ({}, [],)], ["map", "list"])
        >>> df.select(element_at(df.list, 1).as_("idx1")).sort(col("idx1")).show()
        ----------
        |"idx1"  |
        ----------
        |NULL    |
        |1       |
        ----------
        <BLANKLINE>

        >>> df.select(element_at(df.map, lit("a")).as_("get_a")).sort(col("get_a")).show()
        -----------
        |"get_a"  |
        -----------
        |NULL     |
        |1.0      |
        -----------
        <BLANKLINE>"""
    c1 = _to_col_if_str_or_int(col1, "element_at")
    c2 = _to_col_if_str_or_int(col2, "element_at")
    return builtin("element_at")(c1, c2)


def get(col1: Union[ColumnOrName, int], col2: Union[ColumnOrName, int]) -> Column:
    """Returns element of array at given (0-based) index. If the index points outside of the array boundaries, then this function returns NULL.

    Example::

        >>> df = session.createDataFrame([({"a": 1.0, "b": 2.0}, [1, 2, 3],), ({}, [],)], ["map", "list"])
        >>> df.select(get(df.list, 1).as_("idx1")).sort(col("idx1")).show()
        ----------
        |"idx1"  |
        ----------
        |NULL    |
        |2       |
        ----------
        <BLANKLINE>"""
    c1 = _to_col_if_str_or_int(col1, "get")
    c2 = _to_col_if_str_or_int(col2, "get")

    return iff(c2 >= 0, builtin("element_at")(c1, c2 + 1), None)


def array_position(array: ColumnOrName, element: ColumnOrName) -> Column:
    """Returns the position of the first occurrence of the element in array (or 0 if not found).
    Notice that Trino ARRAY indexing starts from 1"""
    a = _to_col_if_str(array, "array_position")
    e = _to_col_if_str(element, "array_position")
    return builtin("array_position")(a, e)


def size(array: ColumnOrName) -> Column:
    """Returns the cardinality (size) of the array or map.

    Example::
        >>> from pystarburst import Row
        >>> df = session.create_dataframe([Row(a=[1, 2, 3])])
        >>> df.select(size("a").alias("result")).show()
        ------------
        |"result"  |
        ------------
        |3         |
        ------------
        <BLANKLINE>
    """
    a = _to_col_if_str(array, "size")
    return builtin("cardinality")(a)


def array_slice(array: ColumnOrName, start: Union[ColumnOrName, int], length: Union[ColumnOrName, int]) -> Column:
    """Subsets array starting from index `start` (or starting from the end if `start` is negative)
    with a length of `length`. The position of the first element is 1"""
    a = _to_col_if_str(array, "array_slice")
    s = _to_col_if_str_or_int(start, "array_slice")
    l = _to_col_if_str_or_int(length, "array_slice")
    return builtin("slice")(a, s, l)


def array_join(array: ColumnOrName, delimiter: ColumnOrName, null_replacement: Optional[ColumnOrName] = None) -> Column:
    """Concatenates the elements of the given array using the delimiter and an optional string to replace nulls.

    Args:
        array: Column containing the ARRAY of elements to convert to a string.
        delimiter: Column containing the string to put between each element (e.g. a space,
            comma, or other human-readable delimiter).
        null_replacement: Optional value to replace nulls.

    Example::
        >>> from pystarburst import Row
        >>> df = session.create_dataframe([Row(a=[1, 45, None])])
        >>> df.select(array_join("a", lit(",")).alias("result")).show()
        ------------
        |"result"  |
        ------------
        |1,45      |
        ------------
        <BLANKLINE>
    """
    a = _to_col_if_str(array, "array_join")
    d = _to_col_if_str(delimiter, "array_join")

    if null_replacement is None:
        return builtin("array_join")(a, d)
    else:
        n = _to_col_if_str(null_replacement, "array_join")
        return builtin("array_join")(a, d, n)


def asc(c: ColumnOrName) -> Column:
    """Returns a Column expression with values sorted in ascending order."""
    c = _to_col_if_str(c, "asc")
    return c.asc()


def asc_nulls_first(c: ColumnOrName) -> Column:
    """Returns a Column expression with values sorted in ascending order
    (null values sorted before non-null values)."""
    c = _to_col_if_str(c, "asc_nulls_first")
    return c.asc_nulls_first()


def asc_nulls_last(c: ColumnOrName) -> Column:
    """Returns a Column expression with values sorted in ascending order
    (null values sorted after non-null values)."""
    c = _to_col_if_str(c, "asc_nulls_last")
    return c.asc_nulls_last()


def desc(c: ColumnOrName) -> Column:
    """Returns a Column expression with values sorted in descending order."""
    c = _to_col_if_str(c, "desc")
    return c.desc()


def desc_nulls_first(c: ColumnOrName) -> Column:
    """Returns a Column expression with values sorted in descending order
    (null values sorted before non-null values)."""
    c = _to_col_if_str(c, "desc_nulls_first")
    return c.desc_nulls_first()


def desc_nulls_last(c: ColumnOrName) -> Column:
    """Returns a Column expression with values sorted in descending order
    (null values sorted after non-null values)."""
    c = _to_col_if_str(c, "desc_nulls_last")
    return c.desc_nulls_last()


def cast(column: ColumnOrName, to: Union[str, DataType]) -> Column:
    """Converts a value of one data type into another data type.
    The semantics of CAST are the same as the semantics of the corresponding to datatype conversion functions.
    If the cast is not possible, an error is raised."""
    c = _to_col_if_str(column, "cast")
    return c.cast(to)


def try_cast(column: ColumnOrName, to: Union[str, DataType]) -> Column:
    """A special version of CAST for a subset of data type conversions.
    It performs the same operation (i.e. converts a value of one data type into another data type), but returns a NULL value instead of raising an error when the conversion can not be performed.

    The ``column`` argument must be a column in Trino.
    """
    c = _to_col_if_str(column, "try_cast")
    return c.try_cast(to)


def iff(
    condition: ColumnOrSqlExpr,
    expr1: Union[ColumnOrLiteral],
    expr2: Union[ColumnOrLiteral],
) -> Column:
    """
    Returns one of two specified expressions, depending on a condition.
    This is equivalent to an ``if-then-else`` expression.

    Args:
        condition: A :class:`Column` expression or SQL text representing the specified condition.
        expr1: A :class:`Column` expression or a literal value, which will be returned
            if ``condition`` is true.
        expr2: A :class:`Column` expression or a literal value, which will be returned
            if ``condition`` is false.
    """
    return builtin("if")(_to_col_if_sql_expr(condition, "if"), expr1, expr2)


def when(condition: ColumnOrSqlExpr, value: Union[ColumnOrLiteral]) -> CaseExpr:
    """Works like a cascading if-then-else statement.
    A series of conditions are evaluated in sequence.
    When a condition evaluates to TRUE, the evaluation stops and the associated
    result (after THEN) is returned. If none of the conditions evaluate to TRUE,
    then the result after the optional OTHERWISE is returned, if present;
    otherwise NULL is returned.

    Args:
        condition: A :class:`Column` expression or SQL text representing the specified condition.
        value: A :class:`Column` expression or a literal value, which will be returned
            if ``condition`` is true.
    """
    return CaseExpr(
        CaseWhen(
            branches=[
                CaseWhen.Branch(
                    condition=_to_col_if_sql_expr(condition, "when")._expression,
                    result=Column._to_expr(value),
                )
            ]
        )
    )


def in_(
    cols: List[ColumnOrName],
    *vals: Union["pystarburst.DataFrame", LiteralType, Iterable[LiteralType]],
) -> Column:
    """Returns a conditional expression that you can pass to the filter or where methods to
    perform the equivalent of a WHERE ... IN query that matches rows containing a sequence of
    values.

    The expression evaluates to true if the values in a row matches the values in one of
    the specified sequences.

    The following code returns a DataFrame that contains the rows in which
    the columns `c1` and `c2` contain the values:
    - `1` and `"a"`, or
    - `2` and `"b"`
    This is equivalent to ``SELECT * FROM table WHERE (c1, c2) IN ((1, 'a'), (2, 'b'))``.

    Example::

        >>> df = session.create_dataframe([[1, "a"], [2, "b"], [3, "c"]], schema=["col1", "col2"])
        >>> df.filter(in_([col("col1"), col("col2")], [[1, "a"], [2, "b"]])).show()
        -------------------
        |"COL1"  |"COL2"  |
        -------------------
        |1       |a       |
        |2       |b       |
        -------------------
        <BLANKLINE>

    The following code returns a DataFrame that contains the rows where
    the values of the columns `c1` and `c2` in `df2` match the values of the columns
    `a` and `b` in `df1`. This is equivalent to
    ``SELECT * FROM table2 WHERE (c1, c2) IN (SELECT a, b FROM table1)``.

    Example::

        >>> df1 = session.sql("select 1, 'a'")
        >>> df.filter(in_([col("col1"), col("col2")], df1)).show()
        -------------------
        |"COL1"  |"COL2"  |
        -------------------
        |1       |a       |
        -------------------
        <BLANKLINE>

    Args::
        cols: A list of the columns to compare for the IN operation.
        vals: A list containing the values to compare for the IN operation.
    """
    vals = parse_positional_args_to_list(*vals)
    columns = [_to_col_if_str(c, "in_") for c in cols]
    return Column(MultipleExpression(expressions=[c._expression for c in columns])).in_(vals)


def cume_dist() -> Column:
    """
    Finds the cumulative distribution of a value with regard to other values
    within the same window partition.
    """
    return builtin("cume_dist")()


def rank() -> Column:
    """
    Returns the rank of a value within an ordered group of values.
    The rank value starts at 1 and continues up.
    """
    return builtin("rank")()


def percent_rank() -> Column:
    """
    Returns the relative rank of a value within a group of values, specified as a percentage
    ranging from 0.0 to 1.0.
    """
    return builtin("percent_rank")()


def dense_rank() -> Column:
    """
    Returns the rank of a value within a group of values, without gaps in the ranks.
    The rank value starts at 1 and continues up sequentially.
    If two values are the same, they will have the same rank.
    """
    return builtin("dense_rank")()


def row_number() -> Column:
    """
    Returns a unique row number for each row within a window partition.
    The row number starts at 1 and continues up sequentially.
    """
    return builtin("row_number")()


def lag(
    e: ColumnOrName,
    offset: int = 1,
    default_value: Optional[Union[ColumnOrLiteral]] = None,
    ignore_nulls: bool = False,
) -> Column:
    """
    Accesses data in a previous row in the same result set without having to
    join the table to itself.
    """
    c = _to_col_if_str(e, "lag")
    return Column(Lag(expr=c._expression, offset=offset, default=Column._to_expr(default_value), ignore_nulls=ignore_nulls))


def lead(
    e: ColumnOrName,
    offset: int = 1,
    default_value: Optional[Union[Column, LiteralType]] = None,
    ignore_nulls: bool = False,
) -> Column:
    """
    Accesses data in a subsequent row in the same result set without having to
    join the table to itself.
    """
    c = _to_col_if_str(e, "lead")
    return Column(Lead(expr=c._expression, offset=offset, default=Column._to_expr(default_value), ignore_nulls=ignore_nulls))


def nth_value(
    e: ColumnOrName,
    offset: int,
    ignore_nulls: bool = False,
) -> Column:
    """
    Returns the value at the specified offset from the beginning of the window. Offsets start at 1.
    The offset can be any scalar expression. If the offset is null or greater than the number of values in the window,
    null is returned. It is an error for the offset to be zero or negative.
    """
    c = _to_col_if_str(e, "nth_value")
    return Column(NthValue(expr=c._expression, offset=offset, ignore_nulls=ignore_nulls))


def last_value(
    e: ColumnOrName,
    ignore_nulls: bool = False,
) -> Column:
    """
    Returns the last value within an ordered group of values.
    """
    c = _to_col_if_str(e, "last_value")
    return Column(LastValue(expr=c._expression, ignore_nulls=ignore_nulls))


def first_value(
    e: ColumnOrName,
    ignore_nulls: bool = False,
) -> Column:
    """
    Returns the first value within an ordered group of values.
    """
    c = _to_col_if_str(e, "first_value")
    return Column(FirstValue(expr=c._expression, ignore_nulls=ignore_nulls))


def ntile(e: Union[int, ColumnOrName]) -> Column:
    """
    Divides an ordered data set equally into the number of buckets specified by n.
    Buckets are sequentially numbered 1 through n.

    Args:
        e: The desired number of buckets; must be a positive integer value.
    """
    c = _to_col_if_str_or_int(e, "ntile")
    return builtin("ntile")(c)


def greatest(*columns: ColumnOrName) -> Column:
    """Returns the largest value from a list of expressions. If any of the argument values is NULL, the result is NULL. GREATEST supports all data types, including VARIANT."""
    c = [_to_col_if_str(ex, "greatest") for ex in columns]
    return builtin("greatest")(*c)


def least(*columns: ColumnOrName) -> Column:
    """Returns the smallest value from a list of expressions. LEAST supports all data types, including VARIANT."""
    c = [_to_col_if_str(ex, "least") for ex in columns]
    return builtin("least")(*c)


def listagg(
    e: ColumnOrName, delimiter: str = "", *within_group: Union[ColumnOrName, Iterable[ColumnOrName]], is_distinct: bool = False
) -> Column:
    """
    Returns the concatenated input values, separated by `delimiter` string.
    See `LISTAGG <https://trino.io/docs/current/functions/aggregate.html#listagg>`_ for details.

    Args:
        e: A :class:`Column` object or column name that determines the values
            to be put into the list.
        delimiter: A string delimiter.
        is_distinct: Whether the input expression is distinct.

    Examples::

        df.group_by(df.col1).agg(listagg(df.col2. ",", f.col2.asc()))
        df.select(listagg(df["col2"], ",", f.col2.asc(), is_distinct=False)
    """
    c = _to_col_if_str(e, "listagg")
    if not within_group:
        raise ValueError(f"within_group is missing")
    within_exprs = [_to_col_if_str(col, "within_group")._expression for col in parse_positional_args_to_list(*within_group)]
    return Column(ListAgg(col=c._expression, delimiter=delimiter, is_distinct=is_distinct, within_group=within_exprs))


def when_matched(
    condition: Optional[Column] = None,
) -> "pystarburst.table.WhenMatchedClause":
    """
    Specifies a matched clause for the :meth:`Table.merge <pystarburst.Table.merge>` action.
    See :class:`~pystarburst.table.WhenMatchedClause` for details.
    """
    return pystarburst.table.WhenMatchedClause(condition)


def when_not_matched(
    condition: Optional[Column] = None,
) -> "pystarburst.table.WhenNotMatchedClause":
    """
    Specifies a not-matched clause for the :meth:`Table.merge <pystarburst.Table.merge>` action.
    See :class:`~pystarburst.table.WhenNotMatchedClause` for details.
    """
    return pystarburst.table.WhenNotMatchedClause(condition)


def fail(error_description: ColumnOrLiteralStr) -> Column:
    """
    Throws an exception with the provided error message.

    Args:
        error_description: A :class:`Column` object or column name that determines the error description

    Examples::

        df.select(fail("unsupported operation"))
    """
    c = lit(error_description)
    return builtin("fail")(c)


def assert_true(col: ColumnOrName, error_description: ColumnOrLiteralStr = None) -> Column:
    """
    Returns null if the input column is true; throws an exception with the provided error message
    otherwise.

    Examples
    --------
    >>> df = session.createDataFrame([(0,1)], ['a', 'b'])
    >>> df.select(assert_true(df.a < df.b).alias('r')).collect()
    [Row(r=None)]
    >>> df = session.createDataFrame([(0,1)], ['a', 'b'])
    >>> df.session(assert_true(df.a < df.b, df.a).alias('r')).collect()
    [Row(r=None)]
    >>> df = session.createDataFrame([(0,1)], ['a', 'b'])
    >>> df.select(assert_true(df.a < df.b, 'error').alias('r')).collect()
    [Row(r=None)]
    """
    c = lit(error_description)
    return builtin("if")(col, None, builtin("fail")(c))


def call_table_function(
    function_name: str, *args: ColumnOrLiteral, **kwargs: ColumnOrLiteral
) -> "pystarburst.table_function.TableFunctionCall":
    """Invokes a Trino table function, including system-defined table functions and user-defined table functions.

    It returns a :meth:`~pystarburst.table_function.TableFunctionCall` so you can specify the partition clause.

    Args:
        function_name: The name of the table function.
        args: The positional arguments of the table function.
        **kwargs: The named arguments of the table function. Some table functions (e.g., ``flatten``) have named arguments instead of positional ones.

    Example:
            >>> from pystarburst.functions import lit
            >>> session.table_function(call_table_function("split_to_table", lit("split words to table"), lit(" ")).over()).collect()
            [Row(SEQ=1, INDEX=1, VALUE='split'), Row(SEQ=1, INDEX=2, VALUE='words'), Row(SEQ=1, INDEX=3, VALUE='to'), Row(SEQ=1, INDEX=4, VALUE='table')]
    """
    return pystarburst.table_function.TableFunctionCall(function_name, *args, **kwargs)


def table_function(function_name: str) -> Callable:
    """Create a function object to invoke a Trino table function.

    Args:
        function_name: The name of the table function.

    Example:
            >>> from pystarburst.functions import lit
            >>> split_to_table = table_function("split_to_table")
            >>> session.table_function(split_to_table(lit("split words to table"), lit(" ")).over()).collect()
            [Row(SEQ=1, INDEX=1, VALUE='split'), Row(SEQ=1, INDEX=2, VALUE='words'), Row(SEQ=1, INDEX=3, VALUE='to'), Row(SEQ=1, INDEX=4, VALUE='table')]
    """
    return lambda *args, **kwargs: call_table_function(function_name, *args, **kwargs)


def call_function(function_name: str, *args: ColumnOrLiteral) -> Column:
    """Invokes a Trino `system-defined function <https://trino.io/docs/current/functions.html>`_ (built-in function) with the specified name
    and arguments.

    Args:
        function_name: The name of built-in function in Trino
        args: Arguments can be in two types:

            - :class:`~pystarburst.Column`, or
            - Basic Python types, which are converted to pystarburst literals.

    Example::
        >>> df = session.create_dataframe([1, 2, 3, 4], schema=["a"])  # a single column with 4 rows
        >>> df.select(call_function("avg", col("a"))).show()
        ----------------
        |"avg(""a"")"  |
        ----------------
        |2.500000      |
        ----------------
        <BLANKLINE>

    """

    return _call_function(function_name, False, *args)


def function(function_name: str) -> Callable:
    """
    Function object to invoke a Trino `system-defined function <https://trino.io/docs/current/functions.html>`_ (built-in function). Use this to invoke
    any built-in functions not explicitly listed in this object.

    Args:
        function_name: The name of built-in function in Trino.

    Returns:
        A :class:`Callable` object for calling a Trino system-defined function.

    Example::
        >>> df = session.create_dataframe([1, 2, 3, 4], schema=["a"])  # a single column with 4 rows
        >>> df.select(call_function("avg", col("a"))).show()
        ----------------
        |"avg(""a"")"  |
        ----------------
        |2.500000      |
        ----------------
        <BLANKLINE>
        >>> my_avg = function('avg')
        >>> df.select(my_avg(col("a"))).show()
        ----------------
        |"avg(""a"")"  |
        ----------------
        |2.500000      |
        ----------------
        <BLANKLINE>
    """
    return lambda *args: call_function(function_name, *args)


def _call_function(
    name: str,
    is_distinct: bool = False,
    *args: ColumnOrLiteral,
) -> Column:
    expressions = [Column._to_expr(arg) for arg in parse_positional_args_to_list(*args)]
    return Column(FunctionExpression(name=name, arguments=expressions, is_distinct=is_distinct))


def from_unixtime(col: ColumnOrName, date_time_format: str = "yyyy-MM-dd HH:mm:ss") -> Column:
    """Convert a Unix timestamp into a string with given pattern (‘yyyy-MM-dd HH:mm:ss’, by default)

    `Supported date and time parts <https://trino.io/docs/current/functions/datetime.html#from_unixtime>`_

    Example::

        >>> # Example run in the EST timezone
        >>> import datetime
        >>> date_df = session.create_dataframe([[1428476356]], schema=["unix_time"])
        >>> date_df.select(from_unixtime(col("unix_time"), "YYYY/MM/dd hh:mm:ss").alias("datetime")).show()
        ------------------------
        |"DATETIME"            |
        ------------------------
        |"2015/04/08 02:59:16" |
        ------------------------
        <BLANKLINE>

    Args:
        col: The Unix timestamp column
        date_time_format: The format string
    """
    if not isinstance(date_time_format, str):
        raise ValueError("date_time_format must be a string")
    c = _to_col_if_str(col, "from_unixtime")
    return builtin("format_datetime")(builtin("from_unixtime")(c), date_time_format)


def unix_timestamp(col: ColumnOrName, date_time_format: str = "yyyy-MM-dd HH:mm:ss") -> Column:
    """Convert a time string with a given pattern (‘yyyy-MM-dd HH:mm:ss’, by default) to Unix timestamp (in seconds).

    `Supported date and time parts <https://trino.io/docs/current/functions/datetime.html#to_unixtime>`_

    Example::

        >>> # Example run in the EST timezone
        >>> import datetime
        >>> date_df = session.create_dataframe([["04/08/2015 02:59:16"]], schema=["date_col"])
        >>> date_df.select(to_unixtime(col("date_col"), "MM/dd/yyyy hh:mm:ss").alias("unix_time")).show()
        ----------------
        |"UNIX_TIME"   |
        ----------------
        |1428476356    |
        ----------------
        <BLANKLINE>

    Args:
        col: The timestamp column or addend in the date_format
        date_time_format: The format string
    """
    if not isinstance(date_time_format, str):
        raise ValueError("part must be a string")
    c = _to_col_if_str(col, "parse_datetime")
    return builtin("to_unixtime")(builtin("parse_datetime")(c, date_time_format))


def timestamp_seconds(col: ColumnOrName) -> Column:
    """Convert a Unix timestamp into a local datetime.

    `Supported date and time parts <https://trino.io/docs/current/functions/datetime.html#from_unixtime>`_

    Example::

        >>> # Example run in the EST timezone
        >>> import datetime
        >>> date_df = session.create_dataframe([[1428476356]], schema=["unix_time"])
        >>> date_df.select(timestamp_seconds(col("unix_time")).alias("datetime")).show()
        --------------------------
        |"DATETIME"              |
        --------------------------
        |2015-04-08 02:59:16.000 |
        --------------------------
        <BLANKLINE>

    Args:
        col: The Unix timestamp column
    """
    c = _to_col_if_str(col, "from_unixtime")
    return builtin("from_unixtime")(c).cast("timestampntz")


def create_map(*cols: ColumnOrName) -> Column:
    """Creates a new map out of a series of rows

    Example:

        >>> df = session.createDataFrame(
        [
            ("Alice", 2),
            ("Bob", 5),
            ("Charlie", 6),
        ],
        schema=["a", "b"])
        >>> df.select(create_map("a", "b")).show()
        ---------------------------------------------
        |"map_from_entries(array_agg(row (a, b)))"  |
        ---------------------------------------------
        |{'Bob': 5, 'Alice': 2, 'Charlie': 6}       |
        ---------------------------------------------

    Args:
        cols: the column containing two-element rows, each one containing the key-value pair
    """
    cs = [_to_col_if_str(c, "row") for c in cols]
    return builtin("map_from_entries")(builtin("array_agg")(builtin("row")(cs)))


def map_from_arrays(col1: ColumnOrName, col2: ColumnOrName) -> Column:
    """Creates a new map from two arrays

    Example:

        >>> df = session.createDataFrame([(["Alice", "Bob", "Charlie"], [2, 5, 8])], schema=["a", "b"])
        >>> df.select(map_from_arrays("a", "b")).show()
        ----------------------------------------
        |"map_from_entries(zip(a, b))"         |
        ----------------------------------------
        |{'Bob': 5, 'Alice': 2, 'Charlie': 8}  |
        ----------------------------------------

    Args:
        col1: the array containing all the keys
        col2: the array containing all the values
    """
    c1 = _to_col_if_str(col1, "zip")
    c2 = _to_col_if_str(col2, "zip")
    return builtin("map_from_entries")(builtin("zip")(c1, c2))


def map_keys(col: ColumnOrName) -> Column:
    """Returns an unordered array containing the keys of the map

    Example:

        >>> df = session.sql("SELECT MAP_FROM_ENTRIES(ARRAY[(1, 'a'), (2, 'b')]) as a")
        >>> df.select(map_keys('a')).show()

        -----------------
        |"map_keys(a)"  |
        -----------------
        |[1, 2]         |
        -----------------

    Args:
        col: the input map
    """
    c = _to_col_if_str(col, "map_keys")
    return builtin("map_keys")(c)


def map_values(col: ColumnOrName) -> Column:
    """Returns an unordered array containing the values of the map

    Example:

        >>> df = session.sql("SELECT MAP_FROM_ENTRIES(ARRAY[(1, 'a'), (2, 'b')]) as a")
        >>> df.select(map_values('a')).show()

        -------------------
        |"map_values(a)"  |
        -------------------
        |['a', 'b']       |
        -------------------

    Args:
        col: the input map
    """
    c = _to_col_if_str(col, "map_values")
    return builtin("map_values")(c)


def map_entries(col: ColumnOrName) -> Column:
    """Returns an unordered array of all entries in the given map

    Example:

        >>> df = session.sql("SELECT MAP_FROM_ENTRIES(ARRAY[(1, 'a'), (2, 'b')]) as a")
        >>> df.select(map_entries('a')).show()

        ------------------------
        |"map_entries(a)"      |
        ------------------------
        |[(1, 'a'), (2, 'b')]  |
        ------------------------

    Args:
        col: the input map
    """
    c = _to_col_if_str(col, "map_entries")
    return builtin("map_entries")(c)


def map_from_entries(col: ColumnOrName) -> Column:
    """Converts an array of entries (key value struct types) to a map of values

    Example:

        >>> df = session.sql("SELECT ARRAY[(1, 'a'), (2, 'b')] as a")
        >>> df.select(map_from_entries('a')).show()

        -------------------------
        |"map_from_entries(a)"  |
        -------------------------
        |{'1': 'a', '2': 'b'}   |
        -------------------------

    Args:
        col: the input map
    """
    c = _to_col_if_str(col, "map_from_entries")
    return builtin("map_from_entries")(c)


def map_concat(*cols: ColumnOrName) -> Column:
    """Returns the union of all the given maps

    Example:

        >>> df = session.sql("SELECT MAP_FROM_ENTRIES(ARRAY[(1, 'a'), (2, 'b')]) as a, MAP_FROM_ENTRIES(ARRAY[(3, 'c')]) as b")
        >>> df.select(map_concat('a', 'b')).show()

        ----------------------------------
        |"map_concat(a, b)"              |
        ----------------------------------
        |{'1': 'a', '2': 'b', '3': 'c'}  |
        ----------------------------------

    Args:
        cols: the maps to concatenate
    """
    cs = [_to_col_if_str(c, "map_concat") for c in cols]
    return builtin("map_concat")(cs)


# Add aliases for user code migration
approx_count_distinct = approx_distinct
array_cat = concat
array_flatten = flatten
array_intersection = array_intersect
array_size = size
array_to_string = array_join
builtin = function
call_builtin = call_function
collect_set = collectSet = lambda *args, **kwargs: array_agg(*args, **kwargs, is_distinct=True)
collect_list = collectList = array_agg
countDistinct = count_distinct
dateadd = date_add
expr = sql_expr
levenshtein = levenshtein_distance
raise_error = fail
skew = skewness
sumDistinct = sum_distinct
week_of_year = weekofyear
ascii = codepoint
startswith = starts_with
endswith = ends_with
parse_json = json_parse
isnan = is_nan
isnull = is_null
bitwiseNOT = bitnot
bitwise_not = bitnot
percentile_approx = approx_percentile
