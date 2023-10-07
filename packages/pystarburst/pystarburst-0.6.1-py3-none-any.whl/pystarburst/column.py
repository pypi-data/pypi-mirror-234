#
# Copyright (c) 2012-2022 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from typing import Iterable, Optional, Union

import pystarburst
from pystarburst._internal.analyzer.analyzer_utils import quote_name
from pystarburst._internal.analyzer.expression.binary import (
    Add,
    And,
    Divide,
    EqualTo,
    GreaterThan,
    GreaterThanOrEqual,
    LessThan,
    LessThanOrEqual,
    Multiply,
    NotEqualTo,
    NullSafeEqualTo,
    Or,
    Remainder,
    Subtract,
)
from pystarburst._internal.analyzer.expression.general import (
    CaseWhen,
    Expression,
    InExpression,
    Like,
    Literal,
    MultipleExpression,
    NamedExpression,
    RegExpLike,
    ScalarSubquery,
    Star,
    UnresolvedAttribute,
)
from pystarburst._internal.analyzer.expression.sort import (
    NullOrdering,
    SortDirection,
    SortOrder,
)
from pystarburst._internal.analyzer.expression.unary import (
    Alias,
    Cast,
    IsNotNull,
    IsNull,
    Minus,
    Not,
    SubfieldInt,
    SubfieldString,
    TryCast,
    UnresolvedAlias,
)
from pystarburst._internal.type_utils import (
    VALID_PYTHON_TYPES_FOR_LITERAL_VALUE,
    ColumnOrLiteral,
    ColumnOrLiteralStr,
    ColumnOrName,
    ColumnOrSqlExpr,
    LiteralType,
    type_string_to_type_object,
)
from pystarburst._internal.utils import parse_positional_args_to_list
from pystarburst.types import DataType
from pystarburst.window import Window, WindowSpec


def _to_col_if_lit(col: Union[ColumnOrLiteral, "pystarburst.DataFrame"], func_name: str) -> "Column":
    if isinstance(col, (Column, pystarburst.DataFrame, list, tuple, set)):
        return col
    elif isinstance(col, VALID_PYTHON_TYPES_FOR_LITERAL_VALUE):
        return Column(Literal(value=col))
    else:
        raise TypeError(f"'{func_name}' expected Column, DataFrame, Iterable or LiteralType, got: {type(col)}")


def _to_col_if_sql_expr(col: ColumnOrSqlExpr, func_name: str) -> "Column":
    if isinstance(col, Column):
        return col
    elif isinstance(col, str):
        return Column._expr(col)
    else:
        raise TypeError(f"'{func_name}' expected Column or str as SQL expression, got: {type(col)}")


def _to_col_if_str(col: ColumnOrName, func_name: str) -> "Column":
    if isinstance(col, Column):
        return col
    elif isinstance(col, str):
        return Column(col)
    else:
        raise TypeError(f"'{func_name.upper()}' expected Column or str, got: {type(col)}")


def _to_col_if_str_or_int(col: Union[ColumnOrName, int], func_name: str) -> "Column":
    if isinstance(col, Column):
        return col
    elif isinstance(col, str):
        return Column(col)
    elif isinstance(col, int):
        return Column(Literal(value=col))
    else:
        raise TypeError(f"'{func_name.upper()}' expected Column, int or str, got: {type(col)}")


class Column:
    """Represents a column or an expression in a :class:`DataFrame`.

    To access a Column object that refers a column in a :class:`DataFrame`, you can:

        - Use the column name.
        - Use the :func:`functions.col` function.
        - Use the :func:`DataFrame.col` method.
        - Use the index operator ``[]`` on a dataframe object with a column name.
        - Use the dot operator ``.`` on a dataframe object with a column name.

        >>> from pystarburst.functions import col
        >>> df = session.create_dataframe([["John", 1], ["Mike", 11]], schema=["name", "age"])
        >>> df.select("name").collect()
        [Row(NAME='John'), Row(NAME='Mike')]
        >>> df.select(col("name")).collect()
        [Row(NAME='John'), Row(NAME='Mike')]
        >>> df.select(df.col("name")).collect()
        [Row(NAME='John'), Row(NAME='Mike')]
        >>> df.select(df["name"]).collect()
        [Row(NAME='John'), Row(NAME='Mike')]
        >>> df.select(df.name).collect()
        [Row(NAME='John'), Row(NAME='Mike')]

        Trino object identifiers are case-insensitive.

        The returned column names after a DataFrame is evaluated follow the case-sensitivity rules too.
        The above ``df`` was created with column name "name" while the returned column name after ``collect()`` was called became "NAME".
        It's because the column is regarded as ignore-case so the Trino cluster returns the upper case.

    To create a Column object that represents a constant value, use :func:`functions.lit`:

        >>> from pystarburst.functions import lit
        >>> df.select(col("name"), lit("const value").alias("literal_column")).collect()
        [Row(NAME='John', LITERAL_COLUMN='const value'), Row(NAME='Mike', LITERAL_COLUMN='const value')]

    This class also defines utility functions for constructing expressions with Columns.
    Column objects can be built with the operators, summarized by operator precedence,
    in the following table:

    ==============================================  ==============================================
    Operator                                        Description
    ==============================================  ==============================================
    ``x[index]``                                    Index operator to get an item out of a Trino ARRAY or OBJECT
    ``**``                                          Power
    ``-x``, ``~x``                                  Unary minus, unary not
    ``*``, ``/``, ``%``                             Multiply, divide, remainder
    ``+``, ``-``                                    Plus, minus
    ``&``                                           And
    ``|``                                           Or
    ``==``, ``!=``, ``<``, ``<=``, ``>``, ``>=``    Equal to, not equal to, less than, less than or equal to, greater than, greater than or equal to
    ==============================================  ==============================================

        The following examples demonstrate how to use Column objects in expressions:

            >>> df = session.create_dataframe([[20, 5], [1, 2]], schema=["a", "b"])
            >>> df.filter((col("a") == 20) | (col("b") <= 10)).collect()  # use parentheses before and after the | operator.
            [Row(A=20, B=5), Row(A=1, B=2)]
            >>> df.filter((df["a"] + df.b) < 10).collect()
            [Row(A=1, B=2)]
            >>> df.select((col("b") * 10).alias("c")).collect()
            [Row(C=50), Row(C=20)]

        When you use ``|``, ``&``, and ``~`` as logical operators on columns, you must always enclose column expressions
        with parentheses as illustrated in the above example, because their order precedence is higher than ``==``, ``<``, etc.

        Do not use ``and``, ``or``, and ``not`` logical operators on column objects, for instance, ``(df.col1 > 1) and (df.col2 > 2)`` is wrong.
        The reason is Python doesn't have a magic method, or dunder method for them.
        It will raise an error and tell you to use ``|``, ``&`` or ``~``, for which Python has magic methods.
        A side effect is ``if column:`` will raise an error because it has a hidden call to ``bool(a_column)``, like using the ``and`` operator.
        Use ``if a_column is None:`` instead.

    To access elements of a semi-structured Object and Array, use ``[]`` on a Column object:

        >>> from pystarburst.types import StringType, IntegerType
        >>> df_with_semi_data = session.create_dataframe([[{"k1": "v1", "k2": "v2"}, ["a0", 1, "a2"]]], schema=["object_column", "array_column"])
        >>> df_with_semi_data.select(df_with_semi_data["object_column"]["k1"].alias("k1_value"), df_with_semi_data["array_column"][0].alias("a0_value"), df_with_semi_data["array_column"][1].alias("a1_value")).collect()
        [Row(K1_VALUE='"v1"', A0_VALUE='"a0"', A1_VALUE='1')]
        >>> # The above two returned string columns have JSON literal values because children of semi-structured data are semi-structured.
        >>> # The next line converts JSON literal to a string
        >>> df_with_semi_data.select(df_with_semi_data["object_column"]["k1"].cast(StringType()).alias("k1_value"), df_with_semi_data["array_column"][0].cast(StringType()).alias("a0_value"), df_with_semi_data["array_column"][1].cast(IntegerType()).alias("a1_value")).collect()
        [Row(K1_VALUE='v1', A0_VALUE='a0', A1_VALUE=1)]

    This class has methods for the most frequently used column transformations and operators. Module :mod:`functions` defines many functions to transform columns.
    """

    def __init__(self, expr: Union[str, Expression], type: DataType = None) -> None:
        self.type = type
        if isinstance(expr, str):
            if expr == "*":
                self._expression = Star(expressions=[])
            else:
                self._expression = UnresolvedAttribute(name=quote_name(expr))
        elif isinstance(expr, Expression):
            self._expression = expr
        else:
            raise TypeError("Column constructor only accepts str or expression.")

    def __getitem__(self, field: Union[str, int]) -> "Column":
        if isinstance(field, str):
            return Column(SubfieldString(child=self._expression, field=field))
        elif isinstance(field, int):
            return Column(SubfieldInt(child=self._expression, field=field + 1))
        else:
            raise TypeError(f"Unexpected item type: {type(field)}")

    # overload operators
    def __eq__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Equal to."""
        right = Column._to_expr(other)
        return Column(EqualTo(left=self._expression, right=right))

    def __ne__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Not equal to."""
        right = Column._to_expr(other)
        return Column(NotEqualTo(left=self._expression, right=right))

    def __gt__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Greater than."""
        return Column(GreaterThan(left=self._expression, right=Column._to_expr(other)))

    def __lt__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Less than."""
        return Column(LessThan(left=self._expression, right=Column._to_expr(other)))

    def __ge__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Greater than or equal to."""
        return Column(GreaterThanOrEqual(left=self._expression, right=Column._to_expr(other)))

    def __le__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Less than or equal to."""
        return Column(LessThanOrEqual(left=self._expression, right=Column._to_expr(other)))

    def __add__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Plus."""
        return Column(Add(left=self._expression, right=Column._to_expr(other)))

    def __radd__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        return Column(Add(left=Column._to_expr(other), right=self._expression))

    def __sub__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Minus."""
        return Column(Subtract(left=self._expression, right=Column._to_expr(other)))

    def __rsub__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        return Column(Subtract(left=Column._to_expr(other), right=self._expression))

    def __mul__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Multiply."""
        return Column(Multiply(left=self._expression, right=Column._to_expr(other)))

    def __rmul__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        return Column(Multiply(left=Column._to_expr(other), right=self._expression))

    def __truediv__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Divide."""
        return Column(Divide(left=self._expression, right=Column._to_expr(other)))

    def __rtruediv__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        return Column(Divide(left=Column._to_expr(other), right=self._expression))

    def __mod__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Reminder."""
        return Column(Remainder(left=self._expression, right=Column._to_expr(other)))

    def __rmod__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        return Column(Remainder(left=Column._to_expr(other), right=self._expression))

    def __pow__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Power."""
        return pystarburst.functions.power(self, other)

    def __rpow__(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        return pystarburst.functions.power(Column(Column._to_expr(other)), self)

    def __bool__(self) -> bool:
        raise TypeError(
            "Cannot convert a Column object into bool: please use '&' for 'and', '|' for 'or', "
            "'~' for 'not' if you're building DataFrame filter expressions. For example, use df.filter((col1 > 1) & (col2 > 2)) instead of df.filter(col1 > 1 and col2 > 2)."
        )

    def __iter__(self) -> None:
        raise TypeError(
            "Column is not iterable. This error can occur when you use the Python built-ins for sum, min and max. Please make sure you use the corresponding function from pystarburst.functions."
        )

    def __round__(self, n=None):
        raise TypeError(
            "Column cannot be rounded. This error can occur when you use the Python built-in round. Please make sure you use the pystarburst.functions.round function instead."
        )

    def in_(
        self,
        *vals: Union[
            LiteralType,
            Iterable[LiteralType],
            "pystarburst.DataFrame",
        ],
    ) -> "Column":
        """Returns a conditional expression that you can pass to the :meth:`DataFrame.filter`
        or where :meth:`DataFrame.where` to perform the equivalent of a WHERE ... IN query
        with a specified list of values. You can also pass this to a
        :meth:`DataFrame.select` call.

        The expression evaluates to true if the value in the column is one of the values in
        a specified sequence.

        For example, the following code returns a DataFrame that contains the rows where
        the column "a" contains the value 1, 2, or 3. This is equivalent to
        ``SELECT * FROM table WHERE a IN (1, 2, 3)``.

        :meth:`isin` is an alias for :meth:`in_`.

        Examples::

            >>> from pystarburst.functions import lit
            >>> df = session.create_dataframe([[1, "x"], [2, "y"] ,[4, "z"]], schema=["a", "b"])
            >>> # Basic example
            >>> df.filter(df["a"].in_(lit(1), lit(2), lit(3))).collect()
            [Row(A=1, B='x'), Row(A=2, B='y')]

            >>> # Check in membership for a DataFrame that has a single column
            >>> df_for_in = session.create_dataframe([[1], [2] ,[3]], schema=["col1"])
            >>> df.filter(df["a"].in_(df_for_in)).sort(df["a"].asc()).collect()
            [Row(A=1, B='x'), Row(A=2, B='y')]

            >>> # Use in with a select method call
            >>> df.select(df["a"].in_(lit(1), lit(2), lit(3)).alias("is_in_list")).collect()
            [Row(IS_IN_LIST=True), Row(IS_IN_LIST=True), Row(IS_IN_LIST=False)]

        Args:
            vals: The values, or a :class:`DataFrame` instance to use to check for membership against this column.
        """
        cols = parse_positional_args_to_list(*vals)
        cols = [_to_col_if_lit(col, "in_") for col in cols]

        column_count = len(self._expression.expressions) if isinstance(self._expression, MultipleExpression) else 1

        def value_mapper(value):
            if isinstance(value, (tuple, set, list)):
                if len(value) == column_count:
                    return MultipleExpression(expressions=[Column._to_expr(v) for v in value])
                else:
                    raise ValueError(f"The number of values {len(value)} does not match the number of columns {column_count}.")
            elif isinstance(value, pystarburst.DataFrame):
                if len(value.schema.fields) == column_count:
                    return ScalarSubquery(trino_plan=value._plan)
                else:
                    raise ValueError(
                        f"The number of values {len(value.schema.fields)} does not match the number of columns {column_count}."
                    )
            else:
                return Column._to_expr(value)

        value_expressions = [value_mapper(col) for col in cols]

        if len(cols) != 1 or not isinstance(value_expressions[0], ScalarSubquery):

            def validate_value(value_expr: Expression):
                if isinstance(value_expr, Literal):
                    return
                elif isinstance(value_expr, MultipleExpression):
                    for expr in value_expr.expressions:
                        validate_value(expr)
                    return
                else:
                    raise TypeError(
                        f"'{type(value_expr)}' is not supported for the values parameter of the function "
                        f"in(). You must either specify a sequence of literals or a DataFrame that "
                        f"represents a subquery."
                    )

            for ve in value_expressions:
                validate_value(ve)

        return Column(InExpression(column=self._expression, values=value_expressions))

    def equal_null(self, other: Union[ColumnOrLiteral, Expression]):
        """Null safe equals."""
        return Column(NullSafeEqualTo(left=self._expression, right=Column._to_expr(other)))

    def between(
        self,
        lower_bound: Union[ColumnOrLiteral, Expression],
        upper_bound: Union[ColumnOrLiteral, Expression],
    ) -> "Column":
        """Between lower bound and upper bound."""
        return (Column._to_expr(lower_bound) <= self) & (self <= Column._to_expr(upper_bound))

    def bitand(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Bitwise and."""
        return pystarburst.functions.bitand(self, other)

    def bitor(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Bitwise or."""
        return pystarburst.functions.bitor(self, other)

    def bitxor(self, other: Union[ColumnOrLiteral, Expression]) -> "Column":
        """Bitwise xor."""
        return pystarburst.functions.bitxor(self, other)

    def __neg__(self) -> "Column":
        """Unary minus."""
        return Column(Minus(child=self._expression))

    def equal_nan(self) -> "Column":
        """Is NaN."""
        return pystarburst.functions.is_nan(self)

    def is_null(self) -> "Column":
        """Is null."""
        return Column(IsNull(child=self._expression))

    def is_not_null(self) -> "Column":
        """Is not null."""
        return Column(IsNotNull(child=self._expression))

    # `and, or, not` cannot be overloaded in Python, so use bitwise operators as boolean operators
    def __and__(self, other: "Column") -> "Column":
        """And."""
        return Column(And(left=self._expression, right=Column._to_expr(other)))

    def __rand__(self, other: "Column") -> "Column":
        return Column(And(left=Column._to_expr(other), right=self._expression))

    def __or__(self, other: "Column") -> "Column":
        """Or."""
        return Column(Or(left=self._expression, right=Column._to_expr(other)))

    def __ror__(self, other: "Column") -> "Column":
        return Column(And(left=Column._to_expr(other), right=self._expression))

    def __invert__(self) -> "Column":
        """Unary not."""
        return Column(Not(child=self._expression))

    def _cast(self, to: Union[str, DataType], try_: bool = False) -> "Column":
        if isinstance(to, str):
            to = type_string_to_type_object(to)
        if try_:
            return Column(TryCast(child=self._expression, to=to))
        return Column(Cast(child=self._expression, to=to))

    def cast(self, to: Union[str, DataType]) -> "Column":
        """Casts the value of the Column to the specified data type.
        It raises an error when  the conversion can not be performed.
        """
        return self._cast(to, False)

    def try_cast(self, to: Union[str, DataType]) -> "Column":
        """Tries to cast the value of the Column to the specified data type.
        It returns a NULL value instead of raising an error when the conversion can not be performed.
        """
        return self._cast(to, True)

    def desc(self) -> "Column":
        """Returns a Column expression with values sorted in descending order."""
        return Column(SortOrder(child=self._expression, direction=SortDirection.DESCENDING))

    def desc_nulls_first(self) -> "Column":
        """Returns a Column expression with values sorted in descending order
        (null values sorted before non-null values)."""
        return Column(
            SortOrder(child=self._expression, direction=SortDirection.DESCENDING, null_ordering=NullOrdering.NULLS_FIRST)
        )

    def desc_nulls_last(self) -> "Column":
        """Returns a Column expression with values sorted in descending order
        (null values sorted after non-null values)."""
        return Column(
            SortOrder(child=self._expression, direction=SortDirection.DESCENDING, null_ordering=NullOrdering.NULLS_LAST)
        )

    def asc(self) -> "Column":
        """Returns a Column expression with values sorted in ascending order."""
        return Column(SortOrder(child=self._expression, direction=SortDirection.ASCENDING))

    def asc_nulls_first(self) -> "Column":
        """Returns a Column expression with values sorted in ascending order
        (null values sorted before non-null values)."""
        return Column(
            SortOrder(child=self._expression, direction=SortDirection.ASCENDING, null_ordering=NullOrdering.NULLS_FIRST)
        )

    def asc_nulls_last(self) -> "Column":
        """Returns a Column expression with values sorted in ascending order
        (null values sorted after non-null values)."""
        return Column(
            SortOrder(child=self._expression, direction=SortDirection.ASCENDING, null_ordering=NullOrdering.NULLS_LAST)
        )

    def like(self, pattern: ColumnOrLiteralStr) -> "Column":
        """Allows case-sensitive matching of strings based on comparison with a pattern.

        Args:
            pattern: A :class:`Column` or a ``str`` that indicates the pattern.
                A ``str`` will be interpreted as a literal value instead of a column name.

        For details, see the Trino documentation on
        `LIKE <https://trino.io/docs/current/functions/comparison.html#pattern-comparison-like>`_.
        """
        return Column(
            Like(
                expr=self._expression,
                pattern=Column._to_expr(pattern),
            )
        )

    def ilike(self, pattern: ColumnOrLiteralStr) -> "Column":
        """Allows case-insensitive matching of strings based on comparison with a pattern.

        Args:
            pattern: A :class:`Column` or a ``str`` that indicates the pattern.
                A ``str`` will be interpreted as a literal value instead of a column name.

        For details, see the Trino documentation on
        `LIKE <https://trino.io/docs/current/functions/comparison.html#pattern-comparison-like>`_.
        """
        return Column(
            Like(
                expr=pystarburst.functions.lower(self)._expression,
                pattern=pystarburst.functions.lower(pystarburst.functions.lit(pattern))._expression,
            )
        )

    def regexp(self, pattern: ColumnOrLiteralStr) -> "Column":
        """Returns true if this Column contains the specified regular expression.

        Args:
            pattern: A :class:`Column` or a ``str`` that indicates the pattern.
                A ``str`` will be interpreted as a literal value instead of a column name.

        For details, see the Trino documentation on
        `regular expressions <https://trino.io/docs/current/functions/regexp.html#regexp_like>`.

        :meth:`rlike` is an alias of :meth:`regexp`.
        :meth:`regexp_like` is an alias of :meth:`regexp`.

        """
        return Column(
            RegExpLike(
                expr=self._expression,
                pattern=Column._to_expr(pattern),
            )
        )

    def starts_with(self, other: ColumnOrLiteralStr) -> "Column":
        """Returns true if this Column starts with another string.

        Args:
            other: A :class:`Column` or a ``str`` that is used to check if this column starts with it.
                A ``str`` will be interpreted as a literal value instead of a column name.
        """
        other = pystarburst.functions.lit(other)
        return pystarburst.functions.starts_with(self, other)

    def ends_with(self, other: ColumnOrLiteralStr) -> "Column":
        """Returns true if this Column ends with another string.

        Args:
            other: A :class:`Column` or a ``str`` that is used to check if this column ends with it.
                A ``str`` will be interpreted as a literal value instead of a column name.
        """
        other = pystarburst.functions.lit(other)
        return pystarburst.functions.ends_with(self, other)

    def substr(
        self,
        start_pos: Union["Column", int],
        length: Union["Column", int],
    ) -> "Column":
        """Returns a substring of this string column.

        Args:
            start_pos: The starting position of the substring. Please note that the first character has position 1 instead of 0 in Trino cluster.
            length: The length of the substring.

        :meth:`substring` is an alias of :meth:`substr`.
        """
        return pystarburst.functions.substring(self, start_pos, length)

    def contains(self, other: ColumnOrLiteralStr) -> "Column":
        """Returns true if this Column contains another string.

        Args:
            other: A :class:`Column` or a ``str`` that is used to check if this column contains it.
                A ``str`` will be interpreted as a literal value instead of a column name.
        """
        return pystarburst.functions.contains(self, other)

    def __str__(self):
        return f"Column[{self._expression}]"

    def __repr__(self):
        return f"Column({self._expression})"

    def as_(self, alias: str) -> "Column":
        """Returns a new renamed Column. Alias of :func:`name`."""
        return self.name(alias)

    def alias(self, alias: str) -> "Column":
        """Returns a new renamed Column. Alias of :func:`name`."""
        return self.name(alias)

    def name(self, alias: str) -> "Column":
        """Returns a new renamed Column."""
        return Column(Alias(child=self._expression, name=quote_name(alias)))

    def over(self, window: Optional[WindowSpec] = None) -> "Column":
        """
        Returns a window frame, based on the specified :class:`~pystarburst.window.WindowSpec`.
        """
        if not window:
            window = Window._spec()
        return window._with_aggregate(self._expression)

    def _named(self) -> NamedExpression:
        if isinstance(self._expression, NamedExpression):
            return self._expression
        return UnresolvedAlias(child=self._expression)

    @classmethod
    def _to_expr(cls, expr: Union[ColumnOrLiteral, Expression]) -> Expression:
        """
        Convert a Column object, or an literal value to an expression.
        If it's a Column, get its expression.
        If it's already an expression, return it directly.
        If it's a literal value (here we treat str as literal value instead of column name),
        create a Literal expression.
        """
        if isinstance(expr, cls):
            return expr._expression
        elif isinstance(expr, Expression):
            return expr
        else:
            return Literal(value=expr)

    @classmethod
    def _expr(cls, e: str) -> "Column":
        return cls(UnresolvedAttribute(name=e))

    # Add these alias for user code migration
    isin = in_
    astype = cast
    rlike = regexp
    regexp_like = regexp
    substring = substr
    bitwiseAND = bitand
    bitwiseOR = bitor
    bitwiseXOR = bitxor
    isNotNull = is_not_null
    isNull = is_null
    eqNullSafe = equal_null
    startswith = starts_with
    endswith = ends_with


class CaseExpr(Column):
    """
    Represents a `CASE <https://trino.io/docs/current/functions/conditional.html#case>`_
    expression.

    To construct this object for a CASE expression, call the :func:`functions.when`
    specifying a condition and the corresponding result for that condition.
    Then, call :func:`when` and :func:`otherwise` methods to specify additional conditions
    and results.

    Examples::

        >>> from pystarburst.functions import when, col, lit

        >>> df = session.create_dataframe([[None], [1], [2]], schema=["a"])
        >>> df.select(when(col("a").is_null(), lit(1)) \\
        ...     .when(col("a") == 1, lit(2)) \\
        ...     .otherwise(lit(3)).alias("case_when_column")).collect()
        [Row(CASE_WHEN_COLUMN=1), Row(CASE_WHEN_COLUMN=2), Row(CASE_WHEN_COLUMN=3)]
    """

    def __init__(self, expr: CaseWhen) -> None:
        super().__init__(expr)
        self._branches = expr.branches

    def when(self, condition: ColumnOrSqlExpr, value: Union[ColumnOrLiteral]) -> "CaseExpr":
        """
        Appends one more WHEN condition to the CASE expression.

        Args:
            condition: A :class:`Column` expression or SQL text representing the specified condition.
            value: A :class:`Column` expression or a literal value, which will be returned
                if ``condition`` is true.
        """
        return CaseExpr(
            CaseWhen(
                branches=[
                    *self._branches,
                    CaseWhen.Branch(
                        condition=_to_col_if_sql_expr(condition, "when")._expression,
                        result=Column._to_expr(value),
                    ),
                ]
            )
        )

    def otherwise(self, value: Union[ColumnOrLiteral]) -> "CaseExpr":
        """Sets the default result for this CASE expression.

        :meth:`else_` is an alias of :meth:`otherwise`.
        """
        return CaseExpr(CaseWhen(branches=self._branches, else_value=Column._to_expr(value)))

    else_ = otherwise
