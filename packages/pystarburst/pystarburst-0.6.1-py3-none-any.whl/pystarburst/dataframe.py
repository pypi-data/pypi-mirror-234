#
# Copyright (c) 2012-2022 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

import itertools
import re
from functools import cached_property
from logging import getLogger
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
)

import pystarburst
from pystarburst import Alias
from pystarburst._internal.analyzer.analyzer_utils import escape_quotes, quote_name
from pystarburst._internal.analyzer.expression.general import (
    Attribute,
    Expression,
    Literal,
    NamedExpression,
    Star,
    UnresolvedAttribute,
)
from pystarburst._internal.analyzer.expression.sort import SortDirection, SortOrder
from pystarburst._internal.analyzer.plan.logical_plan.binary import (
    Except,
    Intersect,
    IntersectAll,
    Join,
    JoinType,
)
from pystarburst._internal.analyzer.plan.logical_plan.binary import Union as UnionPlan
from pystarburst._internal.analyzer.plan.logical_plan.binary import (
    UnionAll,
    UsingJoin,
    create_join_type,
)
from pystarburst._internal.analyzer.plan.logical_plan.table_function import (
    TableFunctionJoin,
)
from pystarburst._internal.analyzer.plan.logical_plan.unary import (
    CreateView,
    Filter,
    Limit,
    Project,
    Sample,
    Sort,
    Unpivot,
)
from pystarburst._internal.analyzer.plan.trino_plan import TrinoPlan
from pystarburst._internal.error_message import PyStarburstClientExceptionMessages
from pystarburst._internal.type_utils import ColumnOrName, ColumnOrSqlExpr, LiteralType
from pystarburst._internal.utils import (
    TempObjectType,
    column_to_bool,
    generate_random_alphanumeric,
    is_pandas_installed,
    is_sql_select_statement,
    is_trino_quoted_id_case_insensitive,
    is_trino_unquoted_suffix_case_insensitive,
    parse_positional_args_to_list,
    random_name_for_temp_object,
    validate_object_name,
)
from pystarburst.column import Column, _to_col_if_sql_expr
from pystarburst.dataframe_na_functions import DataFrameNaFunctions
from pystarburst.dataframe_stat_functions import DataFrameStatFunctions
from pystarburst.dataframe_writer import DataFrameWriter
from pystarburst.functions import abs as abs_
from pystarburst.functions import approx_percentile, col, count, lit
from pystarburst.functions import max as max_
from pystarburst.functions import mean
from pystarburst.functions import min as min_
from pystarburst.functions import random, row_number, sql_expr, stddev, when
from pystarburst.row import Row
from pystarburst.table_function import (
    TableFunctionCall,
    _create_table_function_expression,
    _get_cols_after_join_table,
)
from pystarburst.types import DoubleType, StringType, StructType, _NumericType

if TYPE_CHECKING:
    from table import Table

_logger = getLogger(__name__)

_ONE_MILLION = 1000000
_NUM_PREFIX_DIGITS = 4
_UNALIASED_REGEX = re.compile(f"""._[a-zA-Z0-9]{{{_NUM_PREFIX_DIGITS}}}_(.*)""")


def _generate_prefix(prefix: str) -> str:
    return f"{prefix}_{generate_random_alphanumeric(_NUM_PREFIX_DIGITS)}_"


def _get_unaliased(col_name: str) -> List[str]:
    unaliased = []
    c = col_name
    while True:
        match = _UNALIASED_REGEX.match(c)
        if match:
            c = match.group(1)
            unaliased.append(c)
        else:
            break

    return unaliased


def _alias_if_needed(
    df: "DataFrame",
    c: str,
    prefix: Optional[str],
    suffix: Optional[str],
    common_col_names: List[str],
):
    col = df.col(c)
    unquoted_col_name = c.strip('"')
    if c in common_col_names:
        if suffix:
            column_case_insensitive = is_trino_quoted_id_case_insensitive(c)
            suffix_unqouted_case_insensitive = is_trino_unquoted_suffix_case_insensitive(suffix)
            return col.alias(
                f'"{unquoted_col_name}{suffix.lower()}"'
                if column_case_insensitive and suffix_unqouted_case_insensitive
                else f'''"{unquoted_col_name}{escape_quotes(suffix.strip('"'))}"'''
            )
        return col.alias(f'"{prefix}{unquoted_col_name}"')
    else:
        return col.alias(f'"{unquoted_col_name}"')


def _disambiguate(
    lhs: "DataFrame",
    rhs: "DataFrame",
    join_type: JoinType,
    using_columns: List[str],
    *,
    lsuffix: str = "",
    rsuffix: str = "",
) -> Tuple["DataFrame", "DataFrame"]:
    if lsuffix == rsuffix and lsuffix:
        raise ValueError(f"'lsuffix' and 'rsuffix' must be different if they're not empty. You set {lsuffix!r} to both.")
    # Normalize the using columns.
    normalized_using_columns = {quote_name(c) for c in using_columns}
    #  Check if the LHS and RHS have columns in common. If they don't just return them as-is. If
    #  they do have columns in common, alias the common columns with randomly generated l_
    #  and r_ prefixes for the left and right sides respectively.
    #  We assume the column names from the schema are normalized and quoted.
    lhs_names = [attr.name for attr in lhs._output]
    rhs_names = [attr.name for attr in rhs._output]
    common_col_names = [n for n in lhs_names if n in set(rhs_names) and n not in normalized_using_columns]

    suffix_provided = lsuffix or rsuffix
    lhs_prefix = _generate_prefix("l") if not suffix_provided else ""
    rhs_prefix = _generate_prefix("r") if not suffix_provided else ""

    lhs_remapped = lhs.select(
        [
            _alias_if_needed(
                lhs,
                name,
                lhs_prefix,
                lsuffix,
                [] if join_type in [JoinType.LEFT_SEMI_JOIN, JoinType.ANTI_JOIN] else common_col_names,
            )
            for name in lhs_names
        ]
    )

    rhs_remapped = rhs.select([_alias_if_needed(rhs, name, rhs_prefix, rsuffix, common_col_names) for name in rhs_names])
    return lhs_remapped, rhs_remapped


class DataFrame:
    """Represents a lazily-evaluated relational dataset that contains a collection
    of :class:`Row` objects with columns defined by a schema (column name and type).

    A DataFrame is considered lazy because it encapsulates the computation or query
    required to produce a relational dataset. The computation is not performed until
    you call a method that performs an action (e.g. :func:`collect`).

    **Creating a DataFrame**

    You can create a DataFrame in a number of different ways, as shown in the examples
    below.

    Creating tables and data to run the sample code:
        >>> session.sql("create table prices(product_id varchar, amount decimal(10, 2))").collect()
        []
        >>> session.sql("insert into prices values ('id1', 10.0), ('id2', 20.0)").collect()
        []
        >>> session.sql("create table product_catalog(id varchar, name varchar)").collect()
        []
        >>> session.sql("insert into prices values ('id1', 'Product A'), ('id2', 'Product B')").collect()
        []

    Example 1
        Creating a DataFrame by reading a table in Trino::

            >>> df_prices = session.table("prices")
            >>> df_catalog = session.table("product_catalog")

    Example 2
        Creating a DataFrame by specifying a sequence or a range::

            >>> session.create_dataframe([(1, "one"), (2, "two")], schema=["col_a", "col_b"]).show()
            ---------------------
            |"COL_A"  |"COL_B"  |
            ---------------------
            |1        |one      |
            |2        |two      |
            ---------------------
            <BLANKLINE>
            >>> session.range(1, 10, 2).to_df("col1").show()
            ----------
            |"COL1"  |
            ----------
            |1       |
            |3       |
            |5       |
            |7       |
            |9       |
            ----------
            <BLANKLINE>

    Example 3
        Create a new DataFrame by applying transformations to other existing DataFrames::

            >>> df_merged_data = df_catalog.join(df_prices, df_catalog["id"] == df_prices["product_id"])

    **Performing operations on a DataFrame**

    Broadly, the operations on DataFrame can be divided into two types:

    - **Transformations** produce a new DataFrame from one or more existing DataFrames. Note that transformations are lazy and don't cause the DataFrame to be evaluated. If the API does not provide a method to express the SQL that you want to use, you can use :func:`functions.sqlExpr` as a workaround.
    - **Actions** cause the DataFrame to be evaluated. When you call a method that performs an action, PyStarburst sends the SQL query for the DataFrame to the server for evaluation.

    **Transforming a DataFrame**

    The following examples demonstrate how you can transform a DataFrame.

    Example 4
        Using the :func:`select()` method to select the columns that should be in the
        DataFrame (similar to adding a ``SELECT`` clause)::

            >>> # Return a new DataFrame containing the product_id and amount columns of the prices table.
            >>> # This is equivalent to: SELECT PRODUCT_ID, AMOUNT FROM PRICES;
            >>> df_price_ids_and_amounts = df_prices.select(col("product_id"), col("amount"))

    Example 5
        Using the :func:`Column.as_` method to rename a column in a DataFrame (similar
        to using ``SELECT col AS alias``)::

            >>> # Return a new DataFrame containing the product_id column of the prices table as a column named
            >>> # item_id. This is equivalent to: SELECT PRODUCT_ID AS ITEM_ID FROM PRICES;
            >>> df_price_item_ids = df_prices.select(col("product_id").as_("item_id"))

    Example 6
        Using the :func:`filter` method to filter data (similar to adding a ``WHERE`` clause)::

            >>> # Return a new DataFrame containing the row from the prices table with the ID 1.
            >>> # This is equivalent to:
            >>> # SELECT * FROM PRICES WHERE PRODUCT_ID = 1;
            >>> df_price1 = df_prices.filter((col("product_id") == 1))

    Example 7
        Using the :func:`sort()` method to specify the sort order of the data (similar to adding an ``ORDER BY`` clause)::

            >>> # Return a new DataFrame for the prices table with the rows sorted by product_id.
            >>> # This is equivalent to: SELECT * FROM PRICES ORDER BY PRODUCT_ID;
            >>> df_sorted_prices = df_prices.sort(col("product_id"))

    Example 8
        Using :meth:`agg` method to aggregate results.

            >>> import pystarburst.functions as f
            >>> df_prices.agg(("amount", "sum")).collect()
            [Row(SUM(AMOUNT)=Decimal('30.00'))]
            >>> df_prices.agg(f.sum("amount")).collect()
            [Row(SUM(AMOUNT)=Decimal('30.00'))]
            >>> # rename the aggregation column name
            >>> df_prices.agg(f.sum("amount").alias("total_amount"), f.max("amount").alias("max_amount")).collect()
            [Row(TOTAL_AMOUNT=Decimal('30.00'), MAX_AMOUNT=Decimal('20.00'))]

    Example 9
        Using the :func:`group_by()` method to return a
        :class:`RelationalGroupedDataFrame` that you can use to group and aggregate
        results (similar to adding a ``GROUP BY`` clause).

        :class:`RelationalGroupedDataFrame` provides methods for aggregating results, including:

        - :func:`RelationalGroupedDataFrame.avg()` (equivalent to AVG(column))
        - :func:`RelationalGroupedDataFrame.count()` (equivalent to COUNT())
        - :func:`RelationalGroupedDataFrame.max()` (equivalent to MAX(column))
        - :func:`RelationalGroupedDataFrame.min()` (equivalent to MIN(column))
        - :func:`RelationalGroupedDataFrame.sum()` (equivalent to SUM(column))

        >>> # Return a new DataFrame for the prices table that computes the sum of the prices by
        >>> # category. This is equivalent to:
        >>> #  SELECT CATEGORY, SUM(AMOUNT) FROM PRICES GROUP BY CATEGORY
        >>> df_total_price_per_category = df_prices.group_by(col("product_id")).sum(col("amount"))
        >>> # Have multiple aggregation values with the group by
        >>> import pystarburst.functions as f
        >>> df_summary = df_prices.group_by(col("product_id")).agg(f.sum(col("amount")).alias("total_amount"), f.avg("amount"))
        >>> df_summary.show()
        -------------------------------------------------
        |"PRODUCT_ID"  |"TOTAL_AMOUNT"  |"AVG(AMOUNT)"  |
        -------------------------------------------------
        |id1           |10.00           |10.00000000    |
        |id2           |20.00           |20.00000000    |
        -------------------------------------------------
        <BLANKLINE>

    Example 10
        Using windowing functions. Refer to :class:`Window` for more details.

            >>> from pystarburst import Window
            >>> from pystarburst.functions import row_number
            >>> df_prices.with_column("price_rank",  row_number().over(Window.order_by(col("amount").desc()))).show()
            ------------------------------------------
            |"PRODUCT_ID"  |"AMOUNT"  |"PRICE_RANK"  |
            ------------------------------------------
            |id2           |20.00     |1             |
            |id1           |10.00     |2             |
            ------------------------------------------
            <BLANKLINE>

    Example 11
        Handling missing values. Refer to :class:`DataFrameNaFunctions` for more details.

            >>> df = session.create_dataframe([[1, None, 3], [4, 5, None]], schema=["a", "b", "c"])
            >>> df.na.fill({"b": 2, "c": 6}).show()
            -------------------
            |"A"  |"B"  |"C"  |
            -------------------
            |1    |2    |3    |
            |4    |5    |6    |
            -------------------
            <BLANKLINE>

    **Performing an action on a DataFrame**

    The following examples demonstrate how you can perform an action on a DataFrame.

    Example 12
        Performing a query and returning an array of Rows::

            >>> df_prices.collect()
            [Row(PRODUCT_ID='id1', AMOUNT=Decimal('10.00')), Row(PRODUCT_ID='id2', AMOUNT=Decimal('20.00'))]

    Example 13
        Performing a query and print the results::

            >>> df_prices.show()
            ---------------------------
            |"PRODUCT_ID"  |"AMOUNT"  |
            ---------------------------
            |id1           |10.00     |
            |id2           |20.00     |
            ---------------------------
            <BLANKLINE>

    Example 14
        Calculating statistics values. Refer to :class:`DataFrameStatFunctions` for more details.

            >>> df = session.create_dataframe([[1, 2], [3, 4], [5, -1]], schema=["a", "b"])
            >>> df.stat.corr("a", "b")
            -0.5960395606792697
    """

    def __init__(
        self,
        session: Optional["pystarburst.Session"] = None,
        plan: Optional[TrinoPlan] = None,
        is_cached: bool = False,
    ) -> None:
        self._session = session
        self._plan = plan
        self.is_cached: bool = is_cached  #: Whether the dataframe is cached.

        self._writer = DataFrameWriter(self)

        self._stat = DataFrameStatFunctions(self)
        self.approxQuantile = self.approx_quantile = self._stat.approx_quantile
        self.corr = self._stat.corr
        self.cov = self._stat.cov
        # TODO: add crosstab when solution for pivot has been identified
        # self.crosstab = self._stat.crosstab
        self.sampleBy = self.sample_by = self._stat.sample_by

        self._na = DataFrameNaFunctions(self)
        self.dropna = self._na.drop
        self.fillna = self._na.fill
        self.replace = self._na.replace

    @property
    def stat(self) -> DataFrameStatFunctions:
        return self._stat

    def collect(self, *, statement_properties: Optional[Dict[str, str]] = None) -> List[Row]:
        """Executes the query representing this DataFrame and returns the result as a
        list of :class:`Row` objects.

        """
        return self._internal_collect(statement_properties=statement_properties)

    def _internal_collect(self, *, statement_properties: Optional[Dict[str, str]] = None) -> List[Row]:
        return self._session._conn.execute(self._plan, statement_properties=statement_properties)

    def to_local_iterator(self, *, statement_properties: Optional[Dict[str, str]] = None) -> Iterator[Row]:
        """Executes the query representing this DataFrame and returns an iterator
        of :class:`Row` objects that you can use to retrieve the results.

        Unlike :meth:`collect`, this method does not load all data into memory
        at once.

        Example::

            >>> df = session.table("prices")
            >>> for row in df.to_local_iterator():
            ...     print(row)
            Row(PRODUCT_ID='id1', AMOUNT=Decimal('10.00'))
            Row(PRODUCT_ID='id2', AMOUNT=Decimal('20.00'))

        """
        return self._session._conn.execute(
            self._plan,
            to_iter=True,
            statement_properties=statement_properties,
        )

    def __copy__(self) -> "DataFrame":
        return self._with_plan(self._plan.source_plan)

    def to_df(self, *names: Union[str, Iterable[str]]) -> "DataFrame":
        """
        Creates a new DataFrame containing columns with the specified names.

        The number of column names that you pass in must match the number of columns in the existing
        DataFrame.

        Examples::

            >>> df1 = session.range(1, 10, 2).to_df("col1")
            >>> df2 = session.range(1, 10, 2).to_df(["col1"])

        Args:
            names: list of new column names
        """
        col_names = parse_positional_args_to_list(*names)
        if not all(isinstance(n, str) for n in col_names):
            raise TypeError("Invalid input type in to_df(), expected str or a list of strs.")

        if len(self._output) != len(col_names):
            raise ValueError(
                f"The number of columns doesn't match. "
                f"Old column names ({len(self._output)}): "
                f"{','.join(attr.name for attr in self._output)}. "
                f"New column names ({len(col_names)}): {','.join(col_names)}."
            )

        new_cols = []
        for attr, name in zip(self._output, col_names):
            new_cols.append(Column(attr).alias(name))
        return self.select(new_cols)

    def to_pandas(self):
        """
        Returns a Pandas DataFrame using the results from the PyStarburst DataFrame.

        Examples::

        >>> df = session.create_dataframe([[1, "a", 1.0], [2, "b", 2.0]]).to_df("id", "value1", "value2").to_pandas()
        """

        if is_pandas_installed:
            import pandas as pd

        return pd.DataFrame(self.collect())

    def transform(self, func: Callable[..., "DataFrame"], *args: Any, **kwargs: Any) -> "DataFrame":
        """Returns a new :class:`DataFrame`. Concise syntax for chaining custom transformations.

        Parameters
        ----------
        func : function
            a function that takes and returns a :class:`DataFrame`.
        *args
            Positional arguments to pass to func.
        **kwargs
            Keyword arguments to pass to func.

        Examples
        --------
        >>> from pystarburst.functions import col
        >>> df = session.createDataFrame([(1, 1.0), (2, 2.0)], ["int", "float"])
        >>> def cast_all_to_int(input_df):
        ...     return input_df.select([col(col_name).cast("int") for col_name in input_df.columns])
        >>> def sort_columns_asc(input_df):
        ...     return input_df.select(*sorted(input_df.columns)).toDF("float", "int")
        >>> df.transform(cast_all_to_int).transform(sort_columns_asc).show()
        +-----+---+
        |float|int|
        +-----+---+
        |    1|  1|
        |    2|  2|
        +-----+---+
        >>> def add_n(input_df, n):
        ...     return input_df.select([(col(col_name) + n).alias(col_name)
        ...                             for col_name in input_df.columns])
        >>> df.transform(add_n, 1).transform(add_n, n=10).toDF("int", "float").show()
        +---+-----+
        |int|float|
        +---+-----+
        | 12| 12.0|
        | 13| 13.0|
        +---+-----+
        """
        result = func(self, *args, **kwargs)
        assert isinstance(result, DataFrame), "Func returned an instance of type [%s], " "should have been DataFrame." % type(
            result
        )
        return result

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.col(item)
        elif isinstance(item, Column):
            return self.filter(item)
        elif isinstance(item, (list, tuple)):
            return self.select(item)
        elif isinstance(item, int):
            return self.__getitem__(self.columns[item])
        else:
            raise TypeError(f"Unexpected item type: {type(item)}")

    def __getattr__(self, name):
        if name.lower() not in [c.lower() for c in self.columns]:
            raise AttributeError(f"{self.__class__.__name__} object has no attribute {name}")
        return self.col(name)

    @property
    def columns(self) -> List[str]:
        """Returns all column names as a list.

        The returned column names are consistent with the Trino identifier syntax.

        ==================================   ==========================
        Column name used to create a table   Column name returned in str
        ==================================   ==========================
        a                                    'a'
        A                                    'a'
        "a"                                  'a'
        "a b"                                '"a b"'
        "a""b"                               '"a""b"'
        ==================================   ==========================
        """
        return self.schema.names

    def col(self, col_name: str) -> Column:
        """Returns a reference to a column in the DataFrame."""
        if col_name == "*":
            return Column(Star(expressions=self._output))
        else:
            return Column(self._resolve(col_name))

    def select(
        self,
        *cols: Union[
            Union[ColumnOrName, TableFunctionCall],
            Iterable[Union[ColumnOrName, TableFunctionCall]],
        ],
    ) -> "DataFrame":
        """Returns a new DataFrame with the specified Column expressions as output
        (similar to SELECT in SQL). Only the Columns specified as arguments will be
        present in the resulting DataFrame.

        You can use any :class:`Column` expression or strings for named columns.

        Example 1::
            >>> df = session.create_dataframe([[1, "some string value", 3, 4]], schema=["col1", "col2", "col3", "col4"])
            >>> df_selected = df.select(col("col1"), col("col2").substr(0, 10), df["col3"] + df["col4"])

        Example 2::

            >>> df_selected = df.select("col1", "col2", "col3")

        Example 3::

            >>> df_selected = df.select(["col1", "col2", "col3"])

        Example 4::

            >>> df_selected = df.select(df["col1"], df.col2, df.col("col3"))

        Example 5::

            >>> from pystarburst.functions import table_function
            >>> split_to_table = table_function("split_to_table")
            >>> df_selected = df.select(df.col1, split_to_table(df.col2, lit(" ")), df.col("col3")).show()
            -----------------------------------------------
            |"COL1"  |"SEQ"  |"INDEX"  |"VALUE"  |"COL3"  |
            -----------------------------------------------
            |1       |1      |1        |some     |3       |
            |1       |1      |2        |string   |3       |
            |1       |1      |3        |value    |3       |
            -----------------------------------------------
            <BLANKLINE>

        Note:
            A `TableFunctionCall` can be added in `select` when the dataframe results from another join. This is possible because we know
            the hierarchy in which the joins are applied.

        Args:
            *cols: A :class:`Column`, :class:`str`, :class:`table_function.TableFunctionCall`, or a list of those. Note that at most one
                   :class:`table_function.TableFunctionCall` object is supported within a select call.
        """
        exprs = parse_positional_args_to_list(*cols)
        if not exprs:
            raise ValueError("The input of select() cannot be empty")

        names = []
        table_func = None
        join_plan = None

        for e in exprs:
            if isinstance(e, Column):
                names.append(e._named())
            elif isinstance(e, str):
                names.append(Column(e)._named())
            elif isinstance(e, TableFunctionCall):
                if table_func:
                    raise ValueError(
                        f"At most one table function can be called inside a select(). "
                        f"Called '{table_func.name}' and '{e.name}'."
                    )
                table_func = e
                func_expr = _create_table_function_expression(func=table_func)
                join_plan = self._session._analyzer.resolve(TableFunctionJoin(self._plan, func_expr))
                _, new_cols = _get_cols_after_join_table(func_expr, self._plan, join_plan)
                names.extend(new_cols)
            else:
                raise TypeError("The input of select() must be Column, column name, TableFunctionCall, or a list of them")
        return self._with_plan(Project(project_list=names, child=join_plan or self._plan))

    def select_expr(self, *exprs: Union[str, Iterable[str]]) -> "DataFrame":
        """
        Projects a set of SQL expressions and returns a new :class:`DataFrame`.
        This method is equivalent to ``select(sql_expr(...))`` with :func:`select`
        and :func:`functions.sql_expr`.

        :func:`selectExpr` is an alias of :func:`select_expr`.

        Args:
            exprs: The SQL expressions.

        Examples::

            >>> df = session.create_dataframe([-1, 2, 3], schema=["a"])  # with one pair of [], the dataframe has a single column and 3 rows.
            >>> df.select_expr("abs(a)", "a + 2", "cast(a as string)").show()
            --------------------------------------------
            |"ABS(A)"  |"A + 2"  |"CAST(A AS STRING)"  |
            --------------------------------------------
            |1         |1        |-1                   |
            |2         |4        |2                    |
            |3         |5        |3                    |
            --------------------------------------------
            <BLANKLINE>

        """
        return self.select([sql_expr(expr) for expr in parse_positional_args_to_list(*exprs)])

    selectExpr = select_expr

    def drop(
        self,
        *cols: Union[ColumnOrName, Iterable[ColumnOrName]],
    ) -> "DataFrame":
        """Returns a new DataFrame that excludes the columns with the specified names
        from the output.

        This is functionally equivalent to calling :func:`select()` and passing in all
        columns except the ones to exclude. This is a no-op if schema does not contain
        the given column name(s).

        Example::

            >>> df = session.create_dataframe([[1, 2, 3]], schema=["a", "b", "c"])
            >>> df.drop("a", "b").show()
            -------
            |"C"  |
            -------
            |3    |
            -------
            <BLANKLINE>

        Args:
            *cols: the columns to exclude, as :class:`str`, :class:`Column` or a list
                of those.

        Raises:
            :class:`PyStarburstClientException`: if the resulting :class:`DataFrame`
                contains no output columns.
        """
        # an empty list should be accept, as dropping nothing
        if not cols:
            raise ValueError("The input of drop() cannot be empty")
        exprs = parse_positional_args_to_list(*cols)

        names = []
        for c in exprs:
            if isinstance(c, str):
                names.append(c)
            elif isinstance(c, Column) and isinstance(c._expression, Attribute):
                names.append(self._plan.alias_map.get(c._expression.id, c._expression.name))
            elif isinstance(c, Column) and isinstance(c._expression, (UnresolvedAttribute, Alias)):
                names.append(c._expression.name)
            else:
                raise PyStarburstClientExceptionMessages.DF_CANNOT_DROP_COLUMN_NAME(str(c))

        normalized_names = {quote_name(n) for n in names}
        existing_names = [attr.name for attr in self._output]
        keep_col_names = [c for c in existing_names if c not in normalized_names]
        if not keep_col_names:
            raise PyStarburstClientExceptionMessages.DF_CANNOT_DROP_ALL_COLUMNS()
        else:
            return self.select(list(keep_col_names))

    def filter(self, expr: ColumnOrSqlExpr) -> "DataFrame":
        """Filters rows based on the specified conditional expression (similar to WHERE
        in SQL).

        Examples::

            >>> df = session.create_dataframe([[1, 2], [3, 4]], schema=["A", "B"])
            >>> df_filtered = df.filter((col("A") > 1) & (col("B") < 100))  # Must use parenthesis before and after operator &.

            >>> # The following two result in the same SQL query:
            >>> df.filter(col("a") > 1).collect()
            [Row(A=3, B=4)]
            >>> df.filter("a > 1").collect()  # use SQL expression
            [Row(A=3, B=4)]

        Args:
            expr: a :class:`Column` expression or SQL text.

        :meth:`where` is an alias of :meth:`filter`.
        """
        return self._with_plan(
            Filter(
                condition=_to_col_if_sql_expr(expr, "filter/where")._expression,
                child=self._plan,
            )
        )

    def sort(
        self,
        *cols: Union[ColumnOrName, Iterable[ColumnOrName]],
        ascending: Optional[Union[bool, int, List[Union[bool, int]]]] = None,
    ) -> "DataFrame":
        """Sorts a DataFrame by the specified expressions (similar to ORDER BY in SQL).

        Examples::

            >>> from pystarburst.functions import col

            >>> df = session.create_dataframe([[1, 2], [3, 4], [1, 4]], schema=["A", "B"])
            >>> df.sort(col("A"), col("B").asc()).show()
            -------------
            |"A"  |"B"  |
            -------------
            |1    |2    |
            |1    |4    |
            |3    |4    |
            -------------
            <BLANKLINE>

            >>> df.sort(col("a"), ascending=False).show()
            -------------
            |"A"  |"B"  |
            -------------
            |3    |4    |
            |1    |2    |
            |1    |4    |
            -------------
            <BLANKLINE>

            >>> # The values from the list overwrite the column ordering.
            >>> df.sort(["a", col("b").desc()], ascending=[1, 1]).show()
            -------------
            |"A"  |"B"  |
            -------------
            |1    |2    |
            |1    |4    |
            |3    |4    |
            -------------
            <BLANKLINE>

        Args:
            *cols: A column name as :class:`str` or :class:`Column`, or a list of
             columns to sort by.
            ascending: A :class:`bool` or a list of :class:`bool` for sorting the
             DataFrame, where ``True`` sorts a column in ascending order and ``False``
             sorts a column in descending order . If you specify a list of multiple
             sort orders, the length of the list must equal the number of columns.
        """
        if not cols:
            raise ValueError("sort() needs at least one sort expression.")
        exprs = self._convert_cols_to_exprs("sort()", *cols)
        if not exprs:
            raise ValueError("sort() needs at least one sort expression.")
        orders = []
        if ascending is not None:
            if isinstance(ascending, (list, tuple)):
                orders = [SortDirection.ASCENDING if asc else SortDirection.DESCENDING for asc in ascending]
            elif isinstance(ascending, (bool, int)):
                orders = [SortDirection.ASCENDING if ascending else SortDirection.DESCENDING]
            else:
                raise TypeError("ascending can only be boolean or list," " but got {}".format(str(type(ascending))))
            if len(exprs) != len(orders):
                raise ValueError(
                    "The length of col ({}) should be same with"
                    " the length of ascending ({}).".format(len(exprs), len(orders))
                )

        sort_exprs = []
        for idx in range(len(exprs)):
            # orders will overwrite current orders in expression (but will not overwrite null ordering)
            # if no order is provided, use ascending order
            if isinstance(exprs[idx], SortOrder):
                sort_exprs.append(
                    SortOrder(child=exprs[idx].child, direction=orders[idx], null_ordering=exprs[idx].null_ordering)
                    if orders
                    else exprs[idx]
                )
            else:
                sort_exprs.append(SortOrder(child=exprs[idx], direction=orders[idx] if orders else SortDirection.ASCENDING))

        return self._with_plan(Sort(order=sort_exprs, is_global=True, child=self._plan))

    def agg(
        self,
        *exprs: Union[Column, Tuple[ColumnOrName, str], Dict[str, str]],
    ) -> "DataFrame":
        """Aggregate the data in the DataFrame. Use this method if you don't need to
        group the data (:func:`group_by`).

        Args:
            exprs: A variable length arguments list where every element is

                - A Column object
                - A tuple where the first element is a column object or a column name and the second element is the name of the aggregate function
                - A list of the above

                or a ``dict`` maps column names to aggregate function names.

        Examples::

            >>> from pystarburst.functions import col, stddev, stddev_pop

            >>> df = session.create_dataframe([[1, 2], [3, 4], [1, 4]], schema=["A", "B"])
            >>> df.agg(stddev(col("a"))).show()
            ----------------------
            |"STDDEV(A)"         |
            ----------------------
            |1.1547003940416753  |
            ----------------------
            <BLANKLINE>

            >>> df.agg(stddev(col("a")), stddev_pop(col("a"))).show()
            -------------------------------------------
            |"STDDEV(A)"         |"STDDEV_POP(A)"     |
            -------------------------------------------
            |1.1547003940416753  |0.9428091005076267  |
            -------------------------------------------
            <BLANKLINE>

            >>> df.agg(("a", "min"), ("b", "max")).show()
            -----------------------
            |"MIN(A)"  |"MAX(B)"  |
            -----------------------
            |1         |4         |
            -----------------------
            <BLANKLINE>

            >>> df.agg({"a": "count", "b": "sum"}).show()
            -------------------------
            |"COUNT(A)"  |"SUM(B)"  |
            -------------------------
            |3           |10        |
            -------------------------
            <BLANKLINE>

        Note:
            The name of the aggregate function to compute must be a valid Trino `aggregate function
            <https://trino.io/docs/current/functions/aggregate.html>`_.

        See also:
            - :meth:`RelationalGroupedDataFrame.agg`
            - :meth:`DataFrame.group_by`
        """
        return self.group_by().agg(*exprs)

    def rollup(
        self,
        *cols: Union[ColumnOrName, Iterable[ColumnOrName]],
    ) -> "pystarburst.RelationalGroupedDataFrame":
        """Performs a SQL
        `GROUP BY ROLLUP <https://trino.io/docs/current/sql/select.html?highlight=rollup#rollup>`_.
        on the DataFrame.

        Args:
            cols: The columns to group by rollup.
        """
        rollup_exprs = self._convert_cols_to_exprs("rollup()", *cols)
        return pystarburst.RelationalGroupedDataFrame(
            self,
            rollup_exprs,
            pystarburst.relational_grouped_dataframe._RollupType(),
        )

    def group_by(
        self,
        *cols: Union[ColumnOrName, Iterable[ColumnOrName]],
    ) -> "pystarburst.RelationalGroupedDataFrame":
        """Groups rows by the columns specified by expressions (similar to GROUP BY in
        SQL).

        This method returns a :class:`RelationalGroupedDataFrame` that you can use to
        perform aggregations on each group of data.

        Args:
            *cols: The columns to group by.

        Valid inputs are:

            - Empty input
            - One or multiple :class:`Column` object(s) or column name(s) (:class:`str`)
            - A list of :class:`Column` objects or column names (:class:`str`)

        Examples:

            >>> from pystarburst.functions import col, lit, sum as sum_, max as max_
            >>> df = session.create_dataframe([(1, 1),(1, 2),(2, 1),(2, 2),(3, 1),(3, 2)], schema=["a", "b"])
            >>> df.group_by().agg(sum_("b")).collect()
            [Row(SUM(B)=9)]
            >>> df.group_by("a").agg(sum_("b")).collect()
            [Row(A=1, SUM(B)=3), Row(A=2, SUM(B)=3), Row(A=3, SUM(B)=3)]
            >>> df.group_by(["a", lit("pystarburst")]).agg(sum_("b")).collect()
            [Row(A=1, LITERAL()='pystarburst', SUM(B)=3), Row(A=2, LITERAL()='snow', SUM(B)=3), Row(A=3, LITERAL()='snow', SUM(B)=3)]
            >>> df.group_by("a").agg((col("*"), "count"), max_("b")).collect()
            [Row(A=1, COUNT(LITERAL())=2, MAX(B)=2), Row(A=2, COUNT(LITERAL())=2, MAX(B)=2), Row(A=3, COUNT(LITERAL())=2, MAX(B)=2)]
            >>> df.group_by("a").function("avg")("b").collect()
            [Row(A=1, AVG(B)=Decimal('1.500000')), Row(A=2, AVG(B)=Decimal('1.500000')), Row(A=3, AVG(B)=Decimal('1.500000'))]
        """
        grouping_exprs = self._convert_cols_to_exprs("group_by()", *cols)
        return pystarburst.RelationalGroupedDataFrame(
            self,
            grouping_exprs,
            pystarburst.relational_grouped_dataframe._GroupByType(),
        )

    def group_by_grouping_sets(
        self,
        *grouping_sets: Union[
            "pystarburst.GroupingSets",
            Iterable["pystarburst.GroupingSets"],
        ],
    ) -> "pystarburst.RelationalGroupedDataFrame":
        """Performs a SQL
        `GROUP BY GROUPING SETS <https://trino.io/docs/current/sql/select.html#grouping-sets>`_.
        on the DataFrame.

        GROUP BY GROUPING SETS is an extension of the GROUP BY clause
        that allows computing multiple GROUP BY clauses in a single statement.
        The group set is a set of dimension columns.

        GROUP BY GROUPING SETS is equivalent to the UNION of two or
        more GROUP BY operations in the same result set.


        Examples::

            >>> from pystarburst import GroupingSets
            >>> df = session.create_dataframe([[1, 2, 10], [3, 4, 20], [1, 4, 30]], schema=["A", "B", "C"])
            >>> df.group_by_grouping_sets(GroupingSets([col("a")])).count().collect()
            [Row(A=1, COUNT=2), Row(A=3, COUNT=1)]
            >>> df.group_by_grouping_sets(GroupingSets(col("a"))).count().collect()
            [Row(A=1, COUNT=2), Row(A=3, COUNT=1)]
            >>> df.group_by_grouping_sets(GroupingSets([col("a")], [col("b")])).count().collect()
            [Row(A=1, B=None, COUNT=2), Row(A=3, B=None, COUNT=1), Row(A=None, B=2, COUNT=1), Row(A=None, B=4, COUNT=2)]
            >>> df.group_by_grouping_sets(GroupingSets([col("a"), col("b")], [col("c")])).count().collect()
            [Row(A=None, B=None, C=10, COUNT=1), Row(A=None, B=None, C=20, COUNT=1), Row(A=None, B=None, C=30, COUNT=1), Row(A=1, B=2, C=None, COUNT=1), Row(A=3, B=4, C=None, COUNT=1), Row(A=1, B=4, C=None, COUNT=1)]


        Args:
            grouping_sets: The list of :class:`GroupingSets` to group by.
        """
        return pystarburst.RelationalGroupedDataFrame(
            self,
            [gs._to_expression for gs in parse_positional_args_to_list(*grouping_sets)],
            pystarburst.relational_grouped_dataframe._GroupByType(),
        )

    def cube(
        self,
        *cols: Union[ColumnOrName, Iterable[ColumnOrName]],
    ) -> "pystarburst.RelationalGroupedDataFrame":
        """Performs a SQL
        `GROUP BY CUBE <https://trino.io/docs/current/sql/select.html#cube>`_.
        on the DataFrame.

        Args:
            cols: The columns to group by cube.
        """
        cube_exprs = self._convert_cols_to_exprs("cube()", *cols)
        return pystarburst.RelationalGroupedDataFrame(
            self,
            cube_exprs,
            pystarburst.relational_grouped_dataframe._CubeType(),
        )

    def distinct(self) -> "DataFrame":
        """Returns a new DataFrame that contains only the rows with distinct values
        from the current DataFrame.

        This is equivalent to performing a SELECT DISTINCT in SQL.
        """
        return self.group_by([self.col(quote_name(f.name)) for f in self.schema.fields]).agg()

    def drop_duplicates(self, *subset: Union[str, Iterable[str]]) -> "DataFrame":
        """Creates a new DataFrame by removing duplicated rows on given subset of columns.

        If no subset of columns is specified, this function is the same as the :meth:`distinct` function.
        The result is non-deterministic when removing duplicated rows from the subset of columns but not all columns.

        For example, if we have a DataFrame ``df``, which has columns ("a", "b", "c") and contains three rows ``(1, 1, 1), (1, 1, 2), (1, 2, 3)``,
        the result of ``df.dropDuplicates("a", "b")`` can be either
        ``(1, 1, 1), (1, 2, 3)``
        or
        ``(1, 1, 2), (1, 2, 3)``

        Args:
            subset: The column names on which duplicates are dropped.

        :meth:`dropDuplicates` is an alias of :meth:`drop_duplicates`.
        """
        if not subset:
            df = self.distinct()
            return df
        subset = parse_positional_args_to_list(*subset)

        filter_cols = [self.col(x) for x in subset]
        output_cols = [self.col(col_name) for col_name in self.columns]
        rownum = row_number().over(pystarburst.Window.partition_by(*filter_cols).order_by(*filter_cols))
        rownum_name = generate_random_alphanumeric()
        df = self.select(*output_cols, rownum.as_(rownum_name)).where(col(rownum_name) == 1).select(output_cols)
        return df

    def pivot(
        self,
        pivot_col: ColumnOrName,
        values: Iterable[LiteralType],
    ) -> "pystarburst.RelationalGroupedDataFrame":
        """Rotates this DataFrame by turning the unique values from one column in the input
        expression into multiple columns and aggregating results where required on any
        remaining column values.

        Only one aggregate is supported with pivot.

        Example::

            >>> create_result = session.sql('''create table monthly_sales(empid int, amount int, month varchar)
            ... as select * from values
            ... (1, 10000, 'JAN'),
            ... (1, 400, 'JAN'),
            ... (2, 4500, 'JAN'),
            ... (2, 35000, 'JAN'),
            ... (1, 5000, 'FEB'),
            ... (1, 3000, 'FEB'),
            ... (2, 200, 'FEB') ''').collect()
            >>> df = session.table("monthly_sales")
            >>> df.pivot("month", ['JAN', 'FEB']).sum("amount").show()
            -------------------------------
            |"EMPID"  |"'JAN'"  |"'FEB'"  |
            -------------------------------
            |1        |10400    |8000     |
            |2        |39500    |200      |
            -------------------------------
            <BLANKLINE>

        Args:
            pivot_col: The column or name of the column to use.
            values: A list of values in the column.
        """
        pc = self._convert_cols_to_exprs("pivot()", pivot_col)
        value_exprs = [v._expression if isinstance(v, Column) else Literal(value=v) for v in values]
        return pystarburst.RelationalGroupedDataFrame(
            self,
            [],
            pystarburst.relational_grouped_dataframe._PivotType(pc[0], value_exprs),
        )

    def unpivot(
        self,
        ids_column_list: Union[ColumnOrName, Iterable[ColumnOrName]],
        unpivot_column_list: List[ColumnOrName],
        name_column: str,
        value_column: str,
    ) -> "DataFrame":
        """Unpivot a DataFrame from wide format to long format, optionally leaving identifier columns set.
        Note that UNPIVOT is not exactly the reverse of PIVOT as it cannot undo aggregations made by PIVOT.

        Args:
            ids_column_list: The names of the columns in the source table or subequery that will be used as identifiers.
            unpivot_column_list: The names of the columns in the source table or subequery that will be narrowed into a single pivot column. The column names will populate ``name_column``, and the column values will populate ``value_column``.
            name_column: The name to assign to the generated column that will be populated with the names of the columns in the column list.
            value_column: The name to assign to the generated column that will be populated with the values from the columns in the column list.

        Example::

            >>> df = session.create_dataframe([
            ...     (1, 'electronics', 100, 200),
            ...     (2, 'clothes', 100, 300)
            ... ], schema=["empid", "dept", "jan", "feb"])
            >>> df = df.unpivot(["empid", "dept"], ["jan", "feb"], "month", "sales").sort("empid")
            >>> df.show()
            ---------------------------------------------
            |"empid"  |"dept"       |"month"  |"sales"  |
            ---------------------------------------------
            |1        |electronics  |JAN      |100      |
            |1        |electronics  |FEB      |200      |
            |2        |clothes      |JAN      |100      |
            |2        |clothes      |FEB      |300      |
            ---------------------------------------------
            <BLANKLINE>
        """
        ids_column_exprs = self._convert_cols_to_exprs("unpivot()", ids_column_list)
        unpivot_column_exprs = self._convert_cols_to_exprs("unpivot()", unpivot_column_list)
        unpivot_plan = Unpivot(
            ids_column_list=ids_column_exprs,
            unpivot_column_list=unpivot_column_exprs,
            name_column=name_column,
            value_column=value_column,
            child=self._plan,
        )

        return self._with_plan(unpivot_plan)

    def limit(self, n: int, offset: int = 0) -> "DataFrame":
        """Returns a new DataFrame that contains at most ``n`` rows from the current
        DataFrame, skipping ``offset`` rows from the beginning (similar to LIMIT and OFFSET in SQL).

        Note that this is a transformation method and not an action method.

        Args:
            n: Number of rows to return.
            offset: Number of rows to skip before the start of the result set. The default value is 0.

        Example::

            >>> df = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
            >>> df.limit(1).show()
            -------------
            |"A"  |"B"  |
            -------------
            |1    |2    |
            -------------
            <BLANKLINE>
            >>> df.limit(1, offset=1).show()
            -------------
            |"A"  |"B"  |
            -------------
            |3    |4    |
            -------------
            <BLANKLINE>
        """
        return self._with_plan(Limit(limit_expr=Literal(value=n), offset_expr=Literal(value=offset), child=self._plan))

    def union(self, other: "DataFrame") -> "DataFrame":
        """Returns a new DataFrame that contains all the rows in the current DataFrame
        and another DataFrame (``other``), excluding any duplicate rows. Both input
        DataFrames must contain the same number of columns.

        Example::
            >>> df1 = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
            >>> df2 = session.create_dataframe([[0, 1], [3, 4]], schema=["c", "d"])
            >>> df1.union(df2).show()
            -------------
            |"A"  |"B"  |
            -------------
            |1    |2    |
            |3    |4    |
            |0    |1    |
            -------------
            <BLANKLINE>

        Args:
            other: the other :class:`DataFrame` that contains the rows to include.
        """
        return self._with_plan(UnionPlan(left=self._plan, right=other._plan))

    def union_all(self, other: "DataFrame") -> "DataFrame":
        """Returns a new DataFrame that contains all the rows in the current DataFrame
        and another DataFrame (``other``), including any duplicate rows. Both input
        DataFrames must contain the same number of columns.

        Example::

            >>> df1 = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
            >>> df2 = session.create_dataframe([[0, 1], [3, 4]], schema=["c", "d"])
            >>> df1.union_all(df2).show()
            -------------
            |"A"  |"B"  |
            -------------
            |1    |2    |
            |3    |4    |
            |0    |1    |
            |3    |4    |
            -------------
            <BLANKLINE>

        Args:
            other: the other :class:`DataFrame` that contains the rows to include.
        """
        return self._with_plan(UnionAll(left=self._plan, right=other._plan))

    def union_by_name(self, other: "DataFrame") -> "DataFrame":
        """Returns a new DataFrame that contains all the rows in the current DataFrame
        and another DataFrame (``other``), excluding any duplicate rows.

        This method matches the columns in the two DataFrames by their names, not by
        their positions. The columns in the other DataFrame are rearranged to match
        the order of columns in the current DataFrame.

        Example::

            >>> df1 = session.create_dataframe([[1, 2]], schema=["a", "b"])
            >>> df2 = session.create_dataframe([[2, 1]], schema=["b", "a"])
            >>> df1.union_by_name(df2).show()
            -------------
            |"A"  |"B"  |
            -------------
            |1    |2    |
            -------------
            <BLANKLINE>

        Args:
            other: the other :class:`DataFrame` that contains the rows to include.
        """
        return self._union_by_name_internal(other, is_all=False)

    def union_all_by_name(self, other: "DataFrame") -> "DataFrame":
        """Returns a new DataFrame that contains all the rows in the current DataFrame
        and another DataFrame (``other``), including any duplicate rows.

        This method matches the columns in the two DataFrames by their names, not by
        their positions. The columns in the other DataFrame are rearranged to match
        the order of columns in the current DataFrame.

        Example::

            >>> df1 = session.create_dataframe([[1, 2]], schema=["a", "b"])
            >>> df2 = session.create_dataframe([[2, 1]], schema=["b", "a"])
            >>> df1.union_all_by_name(df2).show()
            -------------
            |"A"  |"B"  |
            -------------
            |1    |2    |
            |1    |2    |
            -------------
            <BLANKLINE>

        Args:
            other: the other :class:`DataFrame` that contains the rows to include.
        """
        return self._union_by_name_internal(other, is_all=True)

    def _union_by_name_internal(self, other: "DataFrame", is_all: bool = False) -> "DataFrame":
        left_output_attrs = self._output
        right_output_attrs = other._output
        right_output_attr_by_name = {rattr.name: rattr for rattr in right_output_attrs}

        try:
            right_project_list = [right_output_attr_by_name[lattr.name] for lattr in left_output_attrs]
        except KeyError:
            missing_lattrs = [lattr.name for lattr in left_output_attrs if lattr.name not in right_output_attr_by_name]
            raise PyStarburstClientExceptionMessages.DF_CANNOT_RESOLVE_COLUMN_NAME_AMONG(
                ", ".join(missing_lattrs),
                ", ".join(list(right_output_attr_by_name.keys())),
            )

        not_found_attrs = [rattr for rattr in right_output_attrs if rattr not in right_project_list]

        names = right_project_list + not_found_attrs
        right_child = self._with_plan(Project(project_list=names, child=other._plan))

        df = self._with_plan(
            UnionAll(left=self._plan, right=right_child._plan)
            if is_all
            else UnionPlan(left=self._plan, right=right_child._plan)
        )
        return df

    def intersect(self, other: "DataFrame") -> "DataFrame":
        """Returns a new DataFrame that contains the intersection of rows from the
        current DataFrame and another DataFrame (``other``). Duplicate rows are
        eliminated.

        Example::

            >>> df1 = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
            >>> df2 = session.create_dataframe([[1, 2], [5, 6]], schema=["c", "d"])
            >>> df1.intersect(df2).show()
            -------------
            |"A"  |"B"  |
            -------------
            |1    |2    |
            -------------
            <BLANKLINE>

        Args:
            other: the other :class:`DataFrame` that contains the rows to use for the
                intersection.
        """
        return self._with_plan(Intersect(left=self._plan, right=other._plan))

    def intersect_all(self, other: "DataFrame") -> "DataFrame":
        """Returns a new DataFrame that contains the intersection of rows from the
        current DataFrame and another DataFrame (``other``). Duplicate rows are
        persisted.

        Example::

            >>> df1 = session.create_dataframe([("id1", 1), ("id1", 1), ("id", 1), ("id1", 3)]).to_df("id", "value")
            >>> df2 = session.create_dataframe([("id1", 1), ("id1", 1), ("id", 1), ("id1", 2)]).to_df("id", "value")
            >>> df1.intersect_all(df2).show()
            ------------------
            |"id"  |"value"  |
            ------------------
            |id1    |1       |
            |id1    |1       |
            |id     |1       |
            ------------------
            <BLANKLINE>

        Args:
            other: the other :class:`DataFrame` that contains the rows to use for the
                intersection.
        """
        return self._with_plan(IntersectAll(left=self._plan, right=other._plan))

    def except_(self, other: "DataFrame") -> "DataFrame":
        """Returns a new DataFrame that contains all the rows from the current DataFrame
        except for the rows that also appear in the ``other`` DataFrame. Duplicate rows are eliminated.

        Example::

            >>> df1 = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
            >>> df2 = session.create_dataframe([[1, 2], [5, 6]], schema=["c", "d"])
            >>> df1.subtract(df2).show()
            -------------
            |"A"  |"B"  |
            -------------
            |3    |4    |
            -------------
            <BLANKLINE>

        :meth:`minus` and :meth:`subtract` are aliases of :meth:`except_`.

        Args:
            other: The :class:`DataFrame` that contains the rows to exclude.
        """
        return self._with_plan(Except(left=self._plan, right=other._plan))

    def join(
        self,
        right: "DataFrame",
        on: Optional[Union[ColumnOrName, Iterable[ColumnOrName]]] = None,
        how: Optional[str] = None,
        *,
        lsuffix: str = "",
        rsuffix: str = "",
        **kwargs,
    ) -> "DataFrame":
        """Performs a join of the specified type (``how``) with the current
        DataFrame and another DataFrame (``right``) on a list of columns
        (``on``).

        Args:
            right: The other :class:`DataFrame` to join.
            on: A column name or a :class:`Column` object or a list of them to be used for the join.
                When a list of column names are specified, this method assumes the named columns are present in both dataframes.
                You can use keyword ``using_columns`` to specify this condition. Note that to avoid breaking changes, when
                `using_columns`` is specified, it overrides ``on``.
            how: We support the following join types:

                - Inner join: "inner" (the default value)
                - Left outer join: "left", "leftouter"
                - Right outer join: "right", "rightouter"
                - Full outer join: "full", "outer", "fullouter"
                - Left semi join: "semi", "leftsemi"
                - Left anti join: "anti", "leftanti"
                - Cross join: "cross"

                You can also use ``join_type`` keyword to specify this condition.
                Note that to avoid breaking changes, currently when ``join_type`` is specified,
                it overrides ``how``.
            lsuffix: Suffix to add to the overlapping columns of the left DataFrame.
            rsuffix: Suffix to add to the overlapping columns of the right DataFrame.

        Note:
            When both ``lsuffix`` and ``rsuffix`` are empty, the overlapping columns will have random column names in the resulting DataFrame.
            You can reference to these randomly named columns using :meth:`Column.alias` (See the first usage in Examples).

        Examples::
            >>> from pystarburst.functions import col
            >>> df1 = session.create_dataframe([[1, 2], [3, 4], [5, 6]], schema=["a", "b"])
            >>> df2 = session.create_dataframe([[1, 7], [3, 8]], schema=["a", "c"])
            >>> df1.join(df2, df1.a == df2.a).select(df1.a.alias("a_1"), df2.a.alias("a_2"), df1.b, df2.c).show()
            -----------------------------
            |"A_1"  |"A_2"  |"B"  |"C"  |
            -----------------------------
            |1      |1      |2    |7    |
            |3      |3      |4    |8    |
            -----------------------------
            <BLANKLINE>
            >>> # refer a single column "a"
            >>> df1.join(df2, "a").select(df1.a.alias("a"), df1.b, df2.c).show()
            -------------------
            |"A"  |"B"  |"C"  |
            -------------------
            |1    |2    |7    |
            |3    |4    |8    |
            -------------------
            <BLANKLINE>
            >>> # rename the ambiguous columns
            >>> df3 = df1.to_df("df1_a", "b")
            >>> df4 = df2.to_df("df2_a", "c")
            >>> df3.join(df4, col("df1_a") == col("df2_a")).select(col("df1_a").alias("a"), "b", "c").show()
            -------------------
            |"A"  |"B"  |"C"  |
            -------------------
            |1    |2    |7    |
            |3    |4    |8    |
            -------------------
            <BLANKLINE>

            >>> # join multiple columns
            >>> mdf1 = session.create_dataframe([[1, 2], [3, 4], [5, 6]], schema=["a", "b"])
            >>> mdf2 = session.create_dataframe([[1, 2], [3, 4], [7, 6]], schema=["a", "b"])
            >>> mdf1.join(mdf2, ["a", "b"]).show()
            -------------
            |"A"  |"B"  |
            -------------
            |1    |2    |
            |3    |4    |
            -------------
            <BLANKLINE>
            >>> mdf1.join(mdf2, (mdf1["a"] < mdf2["a"]) & (mdf1["b"] == mdf2["b"])).select(mdf1["a"].as_("new_a"), mdf1["b"].as_("new_b")).show()
            ---------------------
            |"NEW_A"  |"NEW_B"  |
            ---------------------
            |5        |6        |
            ---------------------
            <BLANKLINE>
            >>> # use lsuffix and rsuffix to resolve duplicating column names
            >>> mdf1.join(mdf2, (mdf1["a"] < mdf2["a"]) & (mdf1["b"] == mdf2["b"]), lsuffix="_left", rsuffix="_right").show()
            -----------------------------------------------
            |"A_LEFT"  |"B_LEFT"  |"A_RIGHT"  |"B_RIGHT"  |
            -----------------------------------------------
            |5         |6         |7          |6          |
            -----------------------------------------------
            <BLANKLINE>
            >>> mdf1.join(mdf2, (mdf1["a"] < mdf2["a"]) & (mdf1["b"] == mdf2["b"]), rsuffix="_right").show()
            -------------------------------------
            |"A"  |"B"  |"A_RIGHT"  |"B_RIGHT"  |
            -------------------------------------
            |5    |6    |7          |6          |
            -------------------------------------
            <BLANKLINE>


        Note:
            When performing chained operations, this method will not work if there are
            ambiguous column names. For example,

            >>> df1.filter(df1.a == 1).join(df2, df1.a == df2.a).select(df1.a.alias("a"), df1.b, df2.c) # doctest: +SKIP

            will not work because ``df1.filter(df1.a == 1)`` has produced a new dataframe and you
            cannot refer to ``df1.a`` anymore. Instead, you can do either

            >>> df1.join(df2, (df1.a == 1) & (df1.a == df2.a)).select(df1.a.alias("a"), df1.b, df2.c).show()
            -------------------
            |"A"  |"B"  |"C"  |
            -------------------
            |1    |2    |7    |
            -------------------
            <BLANKLINE>

            or

            >>> df3 = df1.filter(df1.a == 1)
            >>> df3.join(df2, df3.a == df2.a).select(df3.a.alias("a"), df3.b, df2.c).show()
            -------------------
            |"A"  |"B"  |"C"  |
            -------------------
            |1    |2    |7    |
            -------------------
            <BLANKLINE>
        """
        using_columns = kwargs.get("using_columns") or on
        join_type = kwargs.get("join_type") or how
        if isinstance(right, DataFrame):
            if self is right or self._plan is right._plan:
                raise PyStarburstClientExceptionMessages.DF_SELF_JOIN_NOT_SUPPORTED()

            # Parse using_columns arg
            if column_to_bool(using_columns) is False:
                return self.cross_join(right, lsuffix=lsuffix, rsuffix=rsuffix)
            elif isinstance(using_columns, str):
                using_columns = [using_columns]
            elif isinstance(using_columns, Column):
                using_columns = using_columns
            elif (
                isinstance(using_columns, Iterable)
                and len(using_columns) > 0
                and not all([isinstance(col, str) for col in using_columns])
            ):
                bad_idx, bad_col = next((idx, col) for idx, col in enumerate(using_columns) if not isinstance(col, str))
                raise TypeError(
                    f"All list elements for 'on' or 'using_columns' must be string type. "
                    f"Got: '{type(bad_col)}' at index {bad_idx}"
                )
            elif not isinstance(using_columns, Iterable):
                raise TypeError(f"Invalid input type for join column: {type(using_columns)}")

            return self._join_dataframes(
                right,
                using_columns,
                create_join_type(join_type or "inner"),
                lsuffix=lsuffix,
                rsuffix=rsuffix,
            )

        raise TypeError("Invalid type for join. Must be Dataframe")

    def join_table_function(
        self,
        func: Union[str, List[str], TableFunctionCall],
        *func_arguments: ColumnOrName,
        **func_named_arguments: ColumnOrName,
    ) -> "DataFrame":
        """Lateral joins the current DataFrame with the output of the specified table function.

        References: `Trino SQL functions <https://trino.io/docs/current/functions/table.html>`_.

        Example 1
            Lateral join a table function by using the name and parameters directly:

            >>> df = session.sql("select 'James' as name, 'address1 address2 address3' as addresses")
            >>> df.join_table_function("split_to_table", df["addresses"], lit(" ")).show()
            --------------------------------------------------------------------
            |"NAME"  |"ADDRESSES"                 |"SEQ"  |"INDEX"  |"VALUE"   |
            --------------------------------------------------------------------
            |James   |address1 address2 address3  |1      |1        |address1  |
            |James   |address1 address2 address3  |1      |2        |address2  |
            |James   |address1 address2 address3  |1      |3        |address3  |
            --------------------------------------------------------------------
            <BLANKLINE>

        Example 2
            Lateral join a table function by calling:

            >>> from pystarburst.functions import table_function
            >>> split_to_table = table_function("split_to_table")
            >>> df = session.sql("select 'James' as name, 'address1 address2 address3' as addresses")
            >>> df.join_table_function(split_to_table(df["addresses"], lit(" "))).show()
            --------------------------------------------------------------------
            |"NAME"  |"ADDRESSES"                 |"SEQ"  |"INDEX"  |"VALUE"   |
            --------------------------------------------------------------------
            |James   |address1 address2 address3  |1      |1        |address1  |
            |James   |address1 address2 address3  |1      |2        |address2  |
            |James   |address1 address2 address3  |1      |3        |address3  |
            --------------------------------------------------------------------
            <BLANKLINE>

        Example 3
            Lateral join a table function with the partition and order by clause:

            >>> from pystarburst.functions import table_function
            >>> split_to_table = table_function("split_to_table")
            >>> df = session.create_dataframe([
            ...     ["John", "James", "address1 address2 address3"],
            ...     ["Mike", "James", "address4 address5 address6"],
            ...     ["Cathy", "Stone", "address4 address5 address6"],
            ... ],
            ... schema=["first_name", "last_name", "addresses"])
            >>> df.join_table_function(split_to_table(df["addresses"], lit(" ")).over(partition_by="last_name", order_by="first_name")).show()
            ----------------------------------------------------------------------------------------
            |"FIRST_NAME"  |"LAST_NAME"  |"ADDRESSES"                 |"SEQ"  |"INDEX"  |"VALUE"   |
            ----------------------------------------------------------------------------------------
            |John          |James        |address1 address2 address3  |1      |1        |address1  |
            |John          |James        |address1 address2 address3  |1      |2        |address2  |
            |John          |James        |address1 address2 address3  |1      |3        |address3  |
            |Mike          |James        |address4 address5 address6  |2      |1        |address4  |
            |Mike          |James        |address4 address5 address6  |2      |2        |address5  |
            |Mike          |James        |address4 address5 address6  |2      |3        |address6  |
            |Cathy         |Stone        |address4 address5 address6  |3      |1        |address4  |
            |Cathy         |Stone        |address4 address5 address6  |3      |2        |address5  |
            |Cathy         |Stone        |address4 address5 address6  |3      |3        |address6  |
            ----------------------------------------------------------------------------------------
            <BLANKLINE>

        Example 4
            Lateral join a table function with aliasing the output column names:

            >>> from pystarburst.functions import table_function
            >>> split_to_table = table_function("split_to_table")
            >>> df = session.sql("select 'James' as name, 'address1 address2 address3' as addresses")
            >>> df.join_table_function(split_to_table(col("addresses"), lit(" ")).alias("seq", "idx", "val")).show()
            ------------------------------------------------------------------
            |"NAME"  |"ADDRESSES"                 |"SEQ"  |"IDX"  |"VAL"     |
            ------------------------------------------------------------------
            |James   |address1 address2 address3  |1      |1      |address1  |
            |James   |address1 address2 address3  |1      |2      |address2  |
            |James   |address1 address2 address3  |1      |3      |address3  |
            ------------------------------------------------------------------
            <BLANKLINE>

        Args:

            func_name: The SQL function name.
            func_arguments: The positional arguments for the SQL function.
            func_named_arguments: The named arguments for the SQL function, if it accepts named arguments.

        Returns:
            A new :class:`DataFrame` that has the columns carried from this :class:`DataFrame`, plus new columns and rows from the lateral join with the table function.

        See Also:
            - :meth:`Session.table_function`, which creates a new :class:`DataFrame` by using the SQL table function.

        """
        func_expr = _create_table_function_expression(func, *func_arguments, **func_named_arguments)

        names = None
        if func_expr.aliases:
            join_plan = self._session._analyzer.resolve(TableFunctionJoin(self._plan, func_expr))
            old_cols, new_cols = _get_cols_after_join_table(func_expr, self._plan, join_plan)
            names = [*old_cols, *new_cols]

        if names:
            return self._with_plan(Project(project_list=names, child=join_plan))

        return self._with_plan(TableFunctionJoin(self._plan, func_expr))

    def cross_join(
        self,
        right: "DataFrame",
        *,
        lsuffix: str = "",
        rsuffix: str = "",
    ) -> "DataFrame":
        """Performs a cross join, which returns the Cartesian product of the current
        :class:`DataFrame` and another :class:`DataFrame` (``right``).

        If the current and ``right`` DataFrames have columns with the same name, and
        you need to refer to one of these columns in the returned DataFrame, use the
        :func:`col` function on the current or ``right`` DataFrame to disambiguate
        references to these columns.

        Example::

            >>> df1 = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
            >>> df2 = session.create_dataframe([[5, 6], [7, 8]], schema=["c", "d"])
            >>> df1.cross_join(df2).sort("a", "b", "c", "d").show()
            -------------------------
            |"A"  |"B"  |"C"  |"D"  |
            -------------------------
            |1    |2    |5    |6    |
            |1    |2    |7    |8    |
            |3    |4    |5    |6    |
            |3    |4    |7    |8    |
            -------------------------
            <BLANKLINE>
            >>> df3 = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
            >>> df4 = session.create_dataframe([[5, 6], [7, 8]], schema=["a", "b"])
            >>> df3.cross_join(df4, lsuffix="_l", rsuffix="_r").sort("a_l", "b_l", "a_r", "b_r").show()
            ---------------------------------
            |"A_L"  |"B_L"  |"A_R"  |"B_R"  |
            ---------------------------------
            |1      |2      |5      |6      |
            |1      |2      |7      |8      |
            |3      |4      |5      |6      |
            |3      |4      |7      |8      |
            ---------------------------------
            <BLANKLINE>

        Args:
            right: the right :class:`DataFrame` to join.
            lsuffix: Suffix to add to the overlapping columns of the left DataFrame.
            rsuffix: Suffix to add to the overlapping columns of the right DataFrame.

        Note:
            If both ``lsuffix`` and ``rsuffix`` are empty, the overlapping columns will have random column names in the result DataFrame.
            If either one is not empty, the overlapping columns won't have random names.
        """
        return self._join_dataframes_internal(
            right,
            JoinType.CROSS_JOIN,
            None,
            lsuffix=lsuffix,
            rsuffix=rsuffix,
        )

    def _join_dataframes(
        self,
        right: "DataFrame",
        using_columns: Union[Column, List[str]],
        join_type: JoinType,
        *,
        lsuffix: str = "",
        rsuffix: str = "",
    ) -> "DataFrame":
        if join_type == JoinType.CROSS_JOIN:
            if column_to_bool(using_columns):
                raise Exception("Cross joins cannot take columns as input.")

        if isinstance(using_columns, Column):
            return self._join_dataframes_internal(
                right,
                join_type,
                join_exprs=using_columns,
                lsuffix=lsuffix,
                rsuffix=rsuffix,
            )

        if join_type in [JoinType.LEFT_SEMI_JOIN, JoinType.ANTI_JOIN]:
            # Create a Column with expression 'true AND <expr> AND <expr> .."
            join_cond = Column(Literal(value=True))
            for c in using_columns:
                quoted = quote_name(c)
                join_cond = join_cond & (self.col(quoted) == right.col(quoted))
            return self._join_dataframes_internal(
                right,
                join_type,
                join_cond,
                lsuffix=lsuffix,
                rsuffix=rsuffix,
            )
        else:
            lhs, rhs = _disambiguate(
                self,
                right,
                join_type,
                using_columns,
                lsuffix=lsuffix,
                rsuffix=rsuffix,
            )
            join_logical_plan = UsingJoin(
                left=lhs._plan,
                right=rhs._plan,
                join_type=join_type,
                using_columns=using_columns,
            )
            return self._with_plan(join_logical_plan)

    def _join_dataframes_internal(
        self,
        right: "DataFrame",
        join_type: JoinType,
        join_exprs: Optional[Column],
        *,
        lsuffix: str = "",
        rsuffix: str = "",
    ) -> "DataFrame":
        (lhs, rhs) = _disambiguate(self, right, join_type, [], lsuffix=lsuffix, rsuffix=rsuffix)
        expression = join_exprs._expression if join_exprs is not None else None
        join_logical_plan = Join(
            left=lhs._plan,
            right=rhs._plan,
            join_type=join_type,
            condition=expression,
        )
        return self._with_plan(join_logical_plan)

    def with_column(self, col_name: str, col: Union[Column, TableFunctionCall]) -> "DataFrame":
        """
        Returns a DataFrame with an additional column with the specified name
        ``col_name``. The column is computed by using the specified expression ``col``.

        If a column with the same name already exists in the DataFrame, that column is
        replaced by the new column.

        Example 1::

            >>> df = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
            >>> df.with_column("mean", (df["a"] + df["b"]) / 2).show()
            ------------------------
            |"A"  |"B"  |"MEAN"    |
            ------------------------
            |1    |2    |1.500000  |
            |3    |4    |3.500000  |
            ------------------------
            <BLANKLINE>

        Args:
            col_name: The name of the column to add or replace.
            col: The :class:`Column` or :class:`table_function.TableFunctionCall` with single column output to add or replace.
        """
        return self.with_columns([col_name], [col])

    def with_columns(self, col_names: List[str], values: List[Union[Column, TableFunctionCall]]) -> "DataFrame":
        """Returns a DataFrame with additional columns with the specified names
        ``col_names``. The columns are computed by using the specified expressions
        ``values``.

        If columns with the same names already exist in the DataFrame, those columns
        are removed and appended at the end by new columns.

        Example 1::

            >>> from pystarburst.functions import table_function
            >>> split_to_table = table_function("split_to_table")
            >>> df = session.sql("select 'James' as name, 'address1 address2 address3' as addresses")
            >>> df.with_columns(["seq", "idx", "val"], [split_to_table(df.addresses, lit(" "))]).show()
            ------------------------------------------------------------------
            |"NAME"  |"ADDRESSES"                 |"SEQ"  |"IDX"  |"VAL"     |
            ------------------------------------------------------------------
            |James   |address1 address2 address3  |1      |1      |address1  |
            |James   |address1 address2 address3  |1      |2      |address2  |
            |James   |address1 address2 address3  |1      |3      |address3  |
            ------------------------------------------------------------------
            <BLANKLINE>

        Args:
            col_names: A list of the names of the columns to add or replace.
            values: A list of the :class:`Column` objects or :class:`table_function.TableFunctionCall` object
                    to add or replace.
        """
        # Get a list of the new columns and their dedupped values
        qualified_names = [quote_name(n) for n in col_names]
        new_column_names = set(qualified_names)

        if len(col_names) != len(new_column_names):
            raise ValueError("The same column name is used multiple times in the col_names parameter.")

        num_table_func_calls = sum(1 if isinstance(col, TableFunctionCall) else 0 for col in values)
        if num_table_func_calls == 0:
            if len(col_names) != len(values):
                raise ValueError(
                    f"The size of column names ({len(col_names)}) is not equal to the size of columns ({len(values)})"
                )
            new_cols = [col.as_(name) for name, col in zip(qualified_names, values)]
        elif num_table_func_calls > 1:
            raise ValueError(
                f"Only one table function call accepted inside with_columns call, ({num_table_func_calls}) provided"
            )
        else:
            if len(col_names) < len(values):
                raise ValueError(
                    "The size of column names must be equal to the size of the output columns. Fewer columns provided."
                )
            new_cols = []
            offset = 0
            for i in range(len(values)):
                col = values[i]
                if isinstance(col, Column):
                    name = col_names[i + offset]
                    new_cols.append(col.as_(name))
                else:
                    offset = len(col_names) - len(values)
                    names = col_names[i : i + offset + 1]
                    new_cols.append(col.as_(*names))

        # Get a list of existing column names that are not being replaced
        old_cols = [Column(field) for field in self._output if field.name not in new_column_names]

        # Put it all together
        return self.select([*old_cols, *new_cols])

    def count(self, *, statement_properties: Optional[Dict[str, str]] = None) -> int:
        """Executes the query representing this DataFrame and returns the number of
        rows in the result (similar to the COUNT function in SQL).

        """
        df = self.agg(("*", "count"))
        result = df._internal_collect(statement_properties=statement_properties)
        return result[0][0]

    @property
    def write(self) -> DataFrameWriter:
        """Returns a new :class:`DataFrameWriter` object that you can use to write the data in the :class:`DataFrame` to
        a Trino cluster

        Example::
            >>> df = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
            >>> df.write.mode("overwrite").save_as_table("saved_table")
            >>> session.table("saved_table").show()
            -------------
            |"A"  |"B"  |
            -------------
            |1    |2    |
            |3    |4    |
            -------------
        """

        return self._writer

    def show(
        self,
        n: int = 10,
        max_width: int = 50,
        *,
        statement_properties: Optional[Dict[str, str]] = None,
    ) -> None:
        """Evaluates this DataFrame and prints out the first ``n`` rows with the
        specified maximum number of characters per column.

        Args:
            n: The number of rows to print out.
            max_width: The maximum number of characters to print out for each column.
                If the number of characters exceeds the maximum, the method prints out
                an ellipsis (...) at the end of the column.
        """
        print(self._show_string(n, max_width, statement_properties=statement_properties))

    def _show_string(self, n: int = 10, max_width: int = 50, **kwargs) -> str:
        query = self._plan.queries[-1].strip().lower()

        if is_sql_select_statement(query):
            result, meta = self._session._conn.get_result_and_metadata(self.limit(n)._plan, **kwargs)
        else:
            res, meta = self._session._conn.get_result_and_metadata(self._plan, **kwargs)
            result = res[:n]

        # The query has been executed
        if meta is None:
            meta = [Attribute(name="status", datatype=StringType())]
            result = [["ok"]]
        col_count = len(meta)
        col_width = []
        header = []
        for field in meta:
            name = field.name
            col_width.append(len(name))
            header.append(name)

        body = []
        for row in result:
            lines = []
            for i, v in enumerate(row):
                texts = str(v).split("\n") if v is not None else ["NULL"]
                for t in texts:
                    col_width[i] = max(len(t), col_width[i])
                    col_width[i] = min(max_width, col_width[i])
                lines.append(texts)

            # max line number in this row
            line_count = max(len(li) for li in lines)
            res = []
            for line_number in range(line_count):
                new_line = []
                for colIndex in range(len(lines)):
                    n = lines[colIndex][line_number] if len(lines[colIndex]) > line_number else ""
                    new_line.append(n)
                res.append(new_line)
            body.extend(res)

        # Add 2 more spaces in each column
        col_width = [w + 2 for w in col_width]

        total_width = sum(col_width) + col_count + 1
        line = "-" * total_width + "\n"

        def row_to_string(row: List[str]) -> str:
            tokens = []
            if row:
                for segment, size in zip(row, col_width):
                    if len(segment) > max_width:
                        # if truncated, add ... to the end
                        formatted = (segment[: max_width - 3] + "...").ljust(size, " ")
                    else:
                        formatted = segment.ljust(size, " ")
                    tokens.append(formatted)
            else:
                tokens = [" " * size for size in col_width]
            return f"|{'|'.join(tok for tok in tokens)}|\n"

        return (
            line
            + row_to_string(header)
            + line
            # `body` of an empty df is empty
            + ("".join(row_to_string(b) for b in body) if body else row_to_string([]))
            + line
        )

    def create_or_replace_view(
        self,
        name: Union[str, Iterable[str]],
    ) -> List[Row]:
        """Creates a view that captures the computation expressed by this DataFrame.

        For ``name``, you can include the database and schema name (i.e. specify a
        fully-qualified name). If no database name or schema name are specified, the
        view will be created in the current database or schema.

        ``name`` must be a valid Trino identifier.

        Args:
            name: The name of the view to create or replace. Can be a list of strings
                that specifies the database name, schema name, and view name.
        """
        if isinstance(name, str):
            formatted_name = name
        elif isinstance(name, (list, tuple)) and all(isinstance(n, str) for n in name):
            formatted_name = ".".join(name)
        else:
            raise TypeError("The input of create_or_replace_view() can only a str or list of strs.")

        return self._do_create_or_replace_view(
            formatted_name,
        )

    def _do_create_or_replace_view(self, view_name: str, **kwargs):
        validate_object_name(view_name)
        logical_plan = CreateView(
            name=view_name,
            child=self._plan,
        )

        trino_plan = self._session._analyzer.resolve(logical_plan)
        return self._session._conn.execute(trino_plan, **kwargs)

    def first(
        self,
        n: Optional[int] = None,
        *,
        statement_properties: Optional[Dict[str, str]] = None,
    ) -> Union[Optional[Row], List[Row]]:
        """Executes the query representing this DataFrame and returns the first ``n``
        rows of the results.

        Args:
            n: The number of rows to return.

        Returns:
             A list of the first ``n`` :class:`Row` objects if ``n`` is not ``None``. If ``n`` is negative or
             larger than the number of rows in the result, returns all rows in the
             results. ``n`` is ``None``, it returns the first :class:`Row` of
             results, or ``None`` if it does not exist.
        """
        if n is None:
            df = self.limit(1)
            result = df._internal_collect(statement_properties=statement_properties)
            return result[0] if result else None
        elif not isinstance(n, int):
            raise ValueError(f"Invalid type of argument passed to first(): {type(n)}")
        elif n < 0:
            return self._internal_collect(statement_properties=statement_properties)
        else:
            df = self.limit(n)
            return df._internal_collect(statement_properties=statement_properties)

    take = first

    def head(self, n: Optional[int] = None) -> Union[Optional[Row], List[Row]]:
        """Returns the first ``n`` rows.

        Parameters
        ----------
        n : int, optional
            default None. Number of rows to return.

        Returns
        -------
        If n is number, return a list of n :class:`Row`.
        If n is None, return a single Row.

        Examples
        --------
        >>> df.head()
        Row(age=2, name='Alice')
        >>> df.head(1)
        [Row(age=2, name='Alice')]
        """
        if n is None:
            rs = self.head(1)
            return rs[0] if rs else None
        return self.take(n)

    def sample(self, frac: float) -> "DataFrame":
        """Samples rows based on either the number of rows to be returned or a
        percentage of rows to be returned.

        Args:
            frac: the percentage of rows to be sampled.
        Returns:
            a :class:`DataFrame` containing the sample of rows.
        """
        DataFrame._validate_sample_input(frac)
        sample_plan = Sample(child=self._plan, probability_fraction=frac)
        return self._with_plan(sample_plan)

    @staticmethod
    def _validate_sample_input(frac: float):
        if frac < 0.0 or frac > 1.0:
            raise ValueError(f"'frac' value {frac} " f"is out of range (0 <= probability_fraction <= 1)")

    @property
    def na(self) -> DataFrameNaFunctions:
        """
        Returns a :class:`DataFrameNaFunctions` object that provides functions for
        handling missing values in the DataFrame.
        """
        return self._na

    def describe(self, *cols: Union[str, List[str]]) -> "DataFrame":
        """
        Computes basic statistics for numeric columns, which includes
        ``count``, ``mean``, ``stddev``, ``min``, and ``max``. If no columns
        are provided, this function computes statistics for all numerical or
        string columns. Non-numeric and non-string columns will be ignored
        when calling this method.

        Example::
            >>> df = session.create_dataframe([[1, 2], [3, 4]], schema=["a", "b"])
            >>> desc_result = df.describe().sort("SUMMARY").show()
            -------------------------------------------------------
            |"SUMMARY"  |"A"                 |"B"                 |
            -------------------------------------------------------
            |count      |2.0                 |2.0                 |
            |max        |3.0                 |4.0                 |
            |mean       |2.0                 |3.0                 |
            |min        |1.0                 |2.0                 |
            |stddev     |1.4142135623730951  |1.4142135623730951  |
            -------------------------------------------------------
            <BLANKLINE>

        Args:
            cols: The names of columns whose basic statistics are computed.
        """
        cols = parse_positional_args_to_list(*cols)
        df = self.select(cols) if len(cols) > 0 else self

        # ignore non-numeric and non-string columns
        numerical_string_col_type_dict = {
            field.name: field.datatype for field in df.schema.fields if isinstance(field.datatype, (StringType, _NumericType))
        }

        stat_func_dict = {
            "count": count,
            "mean": mean,
            "stddev": stddev,
            "min": min_,
            "max": max_,
        }

        # if no columns should be selected, just return stat names
        if len(numerical_string_col_type_dict) == 0:
            df = self._session.create_dataframe(list(stat_func_dict.keys()), schema=["summary"])
            return df

        # otherwise, calculate stats
        res_df = None
        for name, func in stat_func_dict.items():
            agg_cols = []
            for c, t in numerical_string_col_type_dict.items():
                if isinstance(t, StringType):
                    if name in ["mean", "stddev"]:
                        agg_cols.append(func(lit(None).cast(DoubleType())).as_(c))
                    else:
                        agg_cols.append(func(c).cast(StringType()))
                else:
                    agg_cols.append(func(c))
            agg_stat_df = (
                self.agg(agg_cols)
                .to_df(list(numerical_string_col_type_dict.keys()))
                .select(
                    lit(name).as_("summary"),
                    *[
                        Column(c).cast(StringType()) if isinstance(t, StringType) and name in ["mean", "stddev"] else c
                        for c, t in numerical_string_col_type_dict.items()
                    ],
                )
            )
            res_df = res_df.union(agg_stat_df) if res_df else agg_stat_df

        return res_df.order_by(
            when(res_df["summary"] == "count", lit(1))
            .when(res_df["summary"] == "mean", lit(2))
            .when(res_df["summary"] == "stddev", lit(3))
            .when(res_df["summary"] == "min", lit(4))
            .else_(lit(5))
        )

    def summary(self, *statistics: Union[str, List[str]]) -> "DataFrame":
        """
        Computes specified statistics for numeric and string columns.
        Available statistics are: - count - mean - stddev - min - max -
        arbitrary approximate percentiles specified as a percentage (e.g., 75%)

        If no statistics are given, this function computes count, mean, stddev, min,
        approximate quartiles (percentiles at 25%, 50%, and 75%), and max.

        Args:
            statistics: The names of statistics whose basic statistics are computed.
        """
        stat_func_dict = {
            "count": count,
            "mean": mean,
            "stddev": stddev,
            "min": min_,
            "max": max_,
            "25%": approx_percentile,
            "50%": approx_percentile,
            "75%": approx_percentile,
        }

        for statistic in statistics:
            if statistic not in stat_func_dict.keys():
                raise ValueError(f"Incorrect statistic name '{statistic}'")

        if statistics is None:
            pass
        elif statistics:
            stat_func_dict = {key: value for key, value in stat_func_dict.items() if key in statistics}

        # ignore non-numeric and non-string columns
        numerical_string_col_type_dict = {
            field.name: field.datatype for field in self.schema.fields if isinstance(field.datatype, (StringType, _NumericType))
        }

        res_df = None
        for name, func in stat_func_dict.items():
            agg_cols = []
            for c, t in numerical_string_col_type_dict.items():
                if isinstance(t, StringType):
                    if name in ["mean", "stddev"]:
                        agg_cols.append(func(lit(None).cast(DoubleType())).as_(c))
                    elif "%" in name:
                        percentile = float(name.strip("%")) / 100
                        agg_cols.append(func(lit(None).cast(DoubleType()), percentile).as_(c))
                    else:
                        agg_cols.append(func(c).cast(StringType()))
                elif "%" in name:
                    percentile = float(name.strip("%")) / 100
                    agg_cols.append(func(c, percentile))
                else:
                    agg_cols.append(func(c))
            agg_stat_df = (
                self.agg(agg_cols)
                .to_df(list(numerical_string_col_type_dict.keys()))
                .select(
                    lit(name).as_("summary"),
                    *[
                        Column(c).cast(StringType())
                        if isinstance(t, StringType) and (name in ["mean", "stddev"] or "%" in name)
                        else c
                        for c, t in numerical_string_col_type_dict.items()
                    ],
                )
            )
            res_df = res_df.union(agg_stat_df) if res_df else agg_stat_df

        return res_df

    def with_column_renamed(self, existing: ColumnOrName, new: str) -> "DataFrame":
        """Returns a DataFrame with the specified column ``existing`` renamed as ``new``.

        Example::

            >>> # This example renames the column `A` as `NEW_A` in the DataFrame.
            >>> df = session.sql("select 1 as A, 2 as B")
            >>> df_renamed = df.with_column_renamed(col("A"), "NEW_A")
            >>> df_renamed.show()
            -----------------
            |"NEW_A"  |"B"  |
            -----------------
            |1        |2    |
            -----------------
            <BLANKLINE>

        Args:
            existing: The old column instance or column name to be renamed.
            new: The new column name.

        :meth:`with_column_renamed` is an alias of :meth:`rename`.
        """
        new_quoted_name = quote_name(new)
        if isinstance(existing, str):
            old_name = quote_name(existing)
        elif isinstance(existing, Column):
            if isinstance(existing._expression, Attribute):
                att = existing._expression
                old_name = self._plan.alias_map.get(att.id, att.name)
            else:
                raise ValueError(f"Unable to rename column {existing} because it doesn't exist.")
        else:
            raise TypeError("'existing' must be a column name or Column object.")

        to_be_renamed = [x for x in self._output if x.name.upper() == old_name.upper()]
        if not to_be_renamed:
            raise ValueError(f'Unable to rename column "{existing}" because it doesn\'t exist.')
        elif len(to_be_renamed) > 1:
            raise PyStarburstClientExceptionMessages.DF_CANNOT_RENAME_COLUMN_BECAUSE_MULTIPLE_EXIST(
                old_name, new_quoted_name, len(to_be_renamed)
            )
        new_columns = [Column(att).as_(new_quoted_name) if old_name == att.name else Column(att) for att in self._output]
        return self.select(new_columns)

    def cache_result(
        self,
        *,
        statement_properties: Optional[Dict[str, str]] = None,
    ) -> "Table":
        """Caches the content of this DataFrame to create a new cached Table DataFrame.

        All subsequent operations on the returned cached DataFrame are performed on the cached data
        and have no effect on the original DataFrame.

        You can use :meth:`Table.drop_table` or the ``with`` statement to clean up the cached result when it's not needed.
        Refer to the example code below.

        Note:
            An error will be thrown if a cached result is cleaned up and it's used again,
            or any other DataFrames derived from the cached result are used again.

        Examples::
            >>> create_result = session.sql("create temp table RESULT (NUM int)").collect()
            >>> insert_result = session.sql("insert into RESULT values(1),(2)").collect()

            >>> df = session.table("RESULT")
            >>> df.collect()
            [Row(NUM=1), Row(NUM=2)]

            >>> # Run cache_result and then insert into the original table to see
            >>> # that the cached result is not affected
            >>> df1 = df.cache_result()
            >>> insert_again_result = session.sql("insert into RESULT values (3)").collect()
            >>> df1.collect()
            [Row(NUM=1), Row(NUM=2)]
            >>> df.collect()
            [Row(NUM=1), Row(NUM=2), Row(NUM=3)]

            >>> # You can run cache_result on a result that has already been cached
            >>> df2 = df1.cache_result()
            >>> df2.collect()
            [Row(NUM=1), Row(NUM=2)]

            >>> df3 = df.cache_result()
            >>> # Drop RESULT and see that the cached results still exist
            >>> drop_table_result = session.sql(f"drop table RESULT").collect()
            >>> df1.collect()
            [Row(NUM=1), Row(NUM=2)]
            >>> df2.collect()
            [Row(NUM=1), Row(NUM=2)]
            >>> df3.collect()
            [Row(NUM=1), Row(NUM=2), Row(NUM=3)]
            >>> # Clean up the cached result
            >>> df3.drop_table()
            >>> # use context manager to clean up the cached result after it's use.
            >>> with df2.cache_result() as df4:
            ...     df4.collect()
            [Row(NUM=1), Row(NUM=2)]

        Args:

        Returns:
             A :class:`Table` object that holds the cached result in a temporary table.
             All operations on this new DataFrame have no effect on the original.
        """
        temp_table_name = random_name_for_temp_object(TempObjectType.TABLE)
        create_temp_table = self._session._plan_builder.create_temp_table(
            temp_table_name,
            self._plan,
            is_generated=True,
        )

        self._session._conn.execute(
            create_temp_table,
            statement_properties=statement_properties,
        )
        cached_df = self._session.table(temp_table_name)
        cached_df.is_cached = True
        return cached_df

    def random_split(
        self,
        weights: List[float],
        seed: Optional[int] = None,
        *,
        statement_properties: Optional[Dict[str, str]] = None,
    ) -> List["DataFrame"]:
        """
        Randomly splits the current DataFrame into separate DataFrames,
        using the specified weights.

        Args:
            weights: Weights to use for splitting the DataFrame. If the
                weights don't add up to 1, the weights will be normalized.
                Every number in ``weights`` has to be positive. If only one
                weight is specified, the returned DataFrame list only includes
                the current DataFrame.
            seed: The seed for sampling.

        Example::

            >>> df = session.range(10000)
            >>> weights = [0.1, 0.2, 0.3]
            >>> df_parts = df.random_split(weights)
            >>> len(df_parts) == len(weights)
            True

        Note:
            1. When multiple weights are specified, the current DataFrame will
            be cached before being split.

            2. When a weight or a normailized weight is less than ``1e-6``, the
            corresponding split dataframe will be empty.
        """
        if not weights:
            raise ValueError("weights can't be None or empty and must be positive numbers")
        elif len(weights) == 1:
            return [self]
        else:
            for w in weights:
                if w <= 0:
                    raise ValueError("weights must be positive numbers")

            temp_column_name = random_name_for_temp_object(TempObjectType.COLUMN)
            cached_df = self.with_column(temp_column_name, abs_(random(seed)) % _ONE_MILLION).cache_result(
                statement_properties=statement_properties
            )
            sum_weights = sum(weights)
            normalized_cum_weights = [0] + [
                int(w * _ONE_MILLION) for w in list(itertools.accumulate([w / sum_weights for w in weights]))
            ]
            normalized_boundaries = zip(normalized_cum_weights[:-1], normalized_cum_weights[1:])
            res_dfs = [
                cached_df.where((col(temp_column_name) >= lower_bound) & (col(temp_column_name) < upper_bound)).drop(
                    temp_column_name
                )
                for lower_bound, upper_bound in normalized_boundaries
            ]
            return res_dfs

    def col_regex(self, regex: str) -> "DataFrame":
        """
        Selects column based on the column name specified as a regex and returns it.

        :param regex: regex format
        """
        try:
            return self.select([col(c) for c in self.columns if re.match(regex, c)])
        except ValueError:
            raise ValueError(f"Regexp pattern '{regex}' don't match any column from the DataFrame")

    def alias(self, alias: str) -> "DataFrame":
        """Returns a new :class:`DataFrame` with an alias set.

        Parameters
        ----------
        alias : str
            an alias name to be set for the :class:`DataFrame`.

        Examples
        --------
        >>> from pystarburst.functions import *
        >>> df_as1 = df.alias("df_as1")
        >>> df_as2 = df.alias("df_as2")
        >>> joined_df = df_as1.join(df_as2, col("df_as1.name") == col("df_as2.name"), 'inner')
        >>> joined_df.select("df_as1.name", "df_as2.name", "df_as2.age") \
                .sort(desc("df_as1.name")).collect()
        [Row(name='Bob', name='Bob', age=5), Row(name='Alice', name='Alice', age=2)]
        """
        if not isinstance(alias, str):
            raise ValueError("alias should be a string")
        return self.select([col(c).alias(f"{alias}.{c}") for c in self.columns])

    @property
    def queries(self) -> Dict[str, List[str]]:
        """
        Returns a ``dict`` that contains a list of queries that will be executed to
        evaluate this DataFrame with the key `queries`, and a list of post-execution
        actions (e.g., queries to clean up temporary objects) with the key `post_actions`.
        """
        return {
            "queries": self._plan.queries or [],
            "post_actions": self._plan.post_actions or [],
        }

    def explain(self) -> None:
        """
        Prints the list of queries that will be executed to evaluate this DataFrame.
        Prints the query execution plan if only one SELECT/DML/DDL statement will be executed.

        For more information about the query execution plan, see the
        `EXPLAIN ANALYZE <https://trino.io/docs/current/sql/explain.html>`_ command.
        """
        print(self._explain_string())

    def _explain_string(self) -> str:
        output_queries = "\n---\n".join(f"{i+1}.\n{query.strip()}" for i, query in enumerate(self._plan.queries))
        msg = f"""---------DATAFRAME QUERY EXECUTION PLAN----------
Query List:
{output_queries}"""
        # if query list contains more then one queries, skip execution plan
        if len(self._plan.queries) == 1:
            exec_plan = self._session._explain_query(self._plan.queries[0])
            if exec_plan:
                msg = f"{msg}\nQuery Execution Plan:\n{exec_plan}"
            else:
                msg = f"{self._plan.queries[0]} can't be explained"

        return f"{msg}\n--------------------------------------------"

    def _resolve(self, col_name: str) -> Union[Expression, NamedExpression]:
        normalized_col_name = quote_name(col_name)
        cols = list(filter(lambda attr: attr.name == normalized_col_name, self._output))
        if len(cols) == 1:
            return cols[0].with_name(normalized_col_name)
        else:
            raise PyStarburstClientExceptionMessages.DF_CANNOT_RESOLVE_COLUMN_NAME(col_name)

    @cached_property
    def _output(self) -> List[Attribute]:
        return self._plan.output

    @cached_property
    def schema(self) -> StructType:
        """The definition of the columns in this DataFrame (the "relational schema" for
        the DataFrame).
        """
        return StructType._from_attributes(self._plan.attributes)

    def _with_plan(self, logical_plan):
        return DataFrame(self._session, self._session._analyzer.resolve(logical_plan))

    def _convert_cols_to_exprs(
        self,
        calling_method: str,
        *cols: Union[ColumnOrName, Iterable[ColumnOrName]],
    ) -> List[Expression]:
        """Convert a string or a Column, or a list of string and Column objects to expression(s)."""

        def convert(col: ColumnOrName) -> Expression:
            if isinstance(col, str):
                return self._resolve(col)
            elif isinstance(col, Column):
                return col._expression
            else:
                raise TypeError(
                    "{} only accepts str and Column objects, or a list containing str and"
                    " Column objects".format(calling_method)
                )

        exprs = [convert(col) for col in parse_positional_args_to_list(*cols)]
        return exprs

    where = filter

    # Add the following lines so API docs have them
    approxQuantile = approx_quantile = DataFrameStatFunctions.approx_quantile
    corr = DataFrameStatFunctions.corr
    cov = DataFrameStatFunctions.cov
    # TODO figure out how to do pivots
    # crosstab = DataFrameStatFunctions.crosstab
    sampleBy = sample_by = DataFrameStatFunctions.sample_by
    dropna = DataFrameNaFunctions.drop
    fillna = DataFrameNaFunctions.fill
    replace = DataFrameNaFunctions.replace
    # TODO figure out how to support temporary views
    # createOrReplaceTempView = create_or_replace_temp_view
    createOrReplaceView = create_or_replace_view
    crossJoin = cross_join
    dropDuplicates = drop_duplicates
    groupBy = group_by
    minus = subtract = exceptAll = except_
    toDF = to_df
    unionAll = union_all
    unionAllByName = union_all_by_name
    unionByName = union_by_name
    withColumn = with_column
    withColumnRenamed = with_column_renamed
    toLocalIterator = to_local_iterator
    randomSplit = random_split
    order_by = sort
    orderBy = order_by
    intersectAll = intersect_all
    colRegex = col_regex
    groupByGroupingSets = group_by_grouping_sets
    joinTableFunction = join_table_function
    # TODO figure out how to support temporary views
    # naturalJoin = natural_join
    withColumns = with_columns
    rename = with_column_renamed
