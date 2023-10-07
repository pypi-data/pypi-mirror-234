#
# Copyright (c) 2012-2022 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from typing import Dict, Iterable, NamedTuple, Optional, Union

import pystarburst
from pystarburst._internal.analyzer.expression.table import (
    Assignment,
    DeleteMergeExpression,
    InsertMergeExpression,
    UpdateMergeExpression,
)
from pystarburst._internal.analyzer.plan.logical_plan.binary import create_join_type
from pystarburst._internal.analyzer.plan.logical_plan.leaf import UnresolvedRelation
from pystarburst._internal.analyzer.plan.logical_plan.table import (
    TableDelete,
    TableMerge,
    TableUpdate,
)
from pystarburst._internal.error_message import PyStarburstClientExceptionMessages
from pystarburst._internal.type_utils import ColumnOrLiteral
from pystarburst.column import Column
from pystarburst.dataframe import DataFrame, _disambiguate


class UpdateResult(NamedTuple):
    """Result of updating rows in a :class:`Table`."""

    rows_updated: int  #: The number of rows modified.


class DeleteResult(NamedTuple):
    """Result of deleting rows in a :class:`Table`."""

    rows_deleted: int  #: The number of rows deleted.


class MergeResult(NamedTuple):
    """Result of merging a :class:`DataFrame` into a :class:`Table`."""

    rows_affected: int  #: The number of rows inserted, updated or deleted.


class WhenMatchedClause:
    """
    A matched clause for the :meth:`Table.merge` action. It matches all
    remaining rows in the target :class:`Table` that satisfy ``join_expr``
    while also satisfying ``condition``, if it is provided. You can use
    :func:`functions.when_matched` to instantiate this class.

    Args:
        condition: An optional :class:`Column` object representing the
            specified condition.
    """

    def __init__(self, condition: Optional[Column] = None) -> None:
        self._condition_expr = condition._expression if condition is not None else None
        self._clause = None

    def update(self, assignments: Dict[str, ColumnOrLiteral]) -> "WhenMatchedClause":
        """
        Defines an update action for the matched clause and
        returns an updated :class:`WhenMatchedClause` with the new
        update action added.

        Args:
            assignments: A list of values or a ``dict`` that associates
                the names of columns with the values that should be updated.
                The value of ``assignments`` can either be a literal value or
                a :class:`Column` object.

        Example::

            >>> # Adds a matched clause where a row in source is matched
            >>> # if its key is equal to the key of any row in target.
            >>> # For all such rows, update its value to the value of the
            >>> # corresponding row in source.
            >>> from pystarburst.functions import when_matched
            >>> target_df = session.create_dataframe([(10, "old"), (10, "too_old"), (11, "old")], schema=["key", "value"])
            >>> target_df.write.save_as_table("my_table", mode="overwrite")
            >>> target = session.table("my_table")
            >>> source = session.create_dataframe([(10, "new")], schema=["key", "value"])
            >>> target.merge(source, target["key"] == source["key"], [when_matched().update({"value": source["value"]})])
            MergeResult(rows_affected=2)
            >>> target.collect() # the value in the table is updated
            [Row(KEY=10, VALUE='new'), Row(KEY=10, VALUE='new'), Row(KEY=11, VALUE='old')]

        Note:
            An exception will be raised if this method or :meth:`WhenMatchedClause.delete`
            is called more than once on the same :class:`WhenMatchedClause` object.
        """
        if self._clause:
            raise PyStarburstClientExceptionMessages.MERGE_TABLE_ACTION_ALREADY_SPECIFIED(
                "update" if isinstance(self._clause, UpdateMergeExpression) else "delete",
                "WhenMatchedClause",
            )
        self._clause = UpdateMergeExpression(
            condition=self._condition_expr,
            assignments=[Assignment(column=Column(k)._expression, value=Column._to_expr(v)) for k, v in assignments.items()],
        )
        return self

    def delete(self):
        """
        Defines a delete action for the matched clause and
        returns an updated :class:`WhenMatchedClause` with the new
        delete action added.

        Example::

            >>> # Adds a matched clause where a row in source is matched
            >>> # if its key is equal to the key of any row in target.
            >>> # For all such rows, delete them.
            >>> from pystarburst.functions import when_matched
            >>> target_df = session.create_dataframe([(10, "old"), (10, "too_old"), (11, "old")], schema=["key", "value"])
            >>> target_df.write.save_as_table("my_table", mode="overwrite")
            >>> target = session.table("my_table")
            >>> source = session.create_dataframe([(10, "new")], schema=["key", "value"])
            >>> target.merge(source, target["key"] == source["key"], [when_matched().delete()])
            MergeResult(rows_affected=2)
            >>> target.collect() # the rows are deleted
            [Row(KEY=11, VALUE='old')]

        Note:
            An exception will be raised if this method or :meth:`WhenMatchedClause.update`
            is called more than once on the same :class:`WhenMatchedClause` object.
        """
        if self._clause:
            raise PyStarburstClientExceptionMessages.MERGE_TABLE_ACTION_ALREADY_SPECIFIED(
                "update" if isinstance(self._clause, UpdateMergeExpression) else "delete",
                "WhenMatchedClause",
            )
        self._clause = DeleteMergeExpression(condition=self._condition_expr)
        return self


class WhenNotMatchedClause:
    """
    A not-matched clause for the :meth:`Table.merge` action. It matches all
    remaining rows in the target :class:`Table` that do not satisfy ``join_expr``
    but satisfy ``condition``, if it is provided. You can use
    :func:`functions.when_not_matched` to instantiate this class.

    Args:
        condition: An optional :class:`Column` object representing the
            specified condition.
    """

    def __init__(self, condition: Optional[Column] = None) -> None:
        self._condition_expr = condition._expression if condition is not None else None
        self._clause = None

    def insert(self, assignments: Union[Iterable[ColumnOrLiteral], Dict[str, ColumnOrLiteral]]) -> "WhenNotMatchedClause":
        """
        Defines an insert action for the not-matched clause and
        returns an updated :class:`WhenNotMatchedClause` with the new
        insert action added.

        Args:
            assignments: A list of values or a ``dict`` that associates
                the names of columns with the values that should be inserted.
                The value of ``assignments`` can either be a literal value or
                a :class:`Column` object.

        Examples::

            >>> # Adds a not-matched clause where a row in source is not matched
            >>> # if its key does not equal the key of any row in target.
            >>> # For all such rows, insert a row into target whose ley and value
            >>> # are assigned to the key and value of the not matched row.
            >>> from pystarburst.functions import when_not_matched
            >>> target_df = session.create_dataframe([(10, "old"), (10, "too_old"), (11, "old")], schema=["key", "value"])
            >>> target_df.write.save_as_table("my_table", mode="overwrite")
            >>> target = session.table("my_table")
            >>> source = session.create_dataframe([(12, "new")], schema=["key", "value"])
            >>> target.merge(source, target["key"] == source["key"], [when_not_matched().insert([source["key"], source["value"]])])
            MergeResult(rows_affected=1)
            >>> target.collect() # the rows are inserted
            [Row(KEY=12, VALUE='new'), Row(KEY=10, VALUE='old'), Row(KEY=10, VALUE='too_old'), Row(KEY=11, VALUE='old')]

            >>> # For all such rows, insert a row into target whose key is
            >>> # assigned to the key of the not matched row.
            >>> target_df.write.save_as_table("my_table", mode="overwrite")
            >>> target.merge(source, target["key"] == source["key"], [when_not_matched().insert({"key": source["key"]})])
            MergeResult(rows_affected=1)
            >>> target.collect() # the rows are inserted
            [Row(KEY=12, VALUE=None), Row(KEY=10, VALUE='old'), Row(KEY=10, VALUE='too_old'), Row(KEY=11, VALUE='old')]

        Note:
            An exception will be raised if this method is called more than once
            on the same :class:`WhenNotMatchedClause` object.
        """
        if self._clause:
            raise PyStarburstClientExceptionMessages.MERGE_TABLE_ACTION_ALREADY_SPECIFIED("insert", "WhenNotMatchedClause")
        if isinstance(assignments, dict):
            keys = [Column(k)._expression for k in assignments.keys()]
            values = [Column._to_expr(v) for v in assignments.values()]
        else:
            keys = []
            values = [Column._to_expr(v) for v in assignments]
        self._clause = InsertMergeExpression(condition=self._condition_expr, keys=keys, values=values)
        return self


def _get_update_result(affected_rows: int) -> UpdateResult:
    return UpdateResult(affected_rows)


def _get_delete_result(deleted_rows: int) -> DeleteResult:
    return DeleteResult(deleted_rows)


def _get_merge_result(rows_affected: int) -> MergeResult:
    return MergeResult(rows_affected)


class Table(DataFrame):
    """
    Represents a lazily-evaluated Table. It extends :class:`DataFrame` so all
    :class:`DataFrame` operations can be applied to it.

    You can create a :class:`Table` object by calling :meth:`Session.table`
    with the name of the table in Trino. See examples in :meth:`Session.table`.
    """

    def __init__(
        self,
        table_name: str,
        session: Optional["pystarburst.session.Session"] = None,
    ) -> None:
        super().__init__(session, session._analyzer.resolve(UnresolvedRelation(name=table_name)))
        self.is_cached: bool = self.is_cached  #: Whether the table is cached.
        self.table_name: str = table_name  #: The table name

    def __copy__(self) -> "Table":
        return Table(self.table_name, self._session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drop_table()

    def sample(
        self,
        frac: float,
        *,
        sampling_method: Optional[str] = None,
    ) -> "DataFrame":
        """Samples rows based on either the number of rows to be returned or a percentage of rows to be returned.

        Sampling with a seed is not supported on views or subqueries. This method works on tables so it supports ``seed``.
        This is the main difference between :meth:`DataFrame.sample` and this method.

        Args:
            frac: The percentage of rows to be sampled.
            sampling_method: Specifies the sampling method to use:
                - "BERNOULLI": Includes each row with a probability of p/100. Similar to flipping a weighted coin for each row.
                - "SYSTEM": Includes each block of rows with a probability of p/100. Similar to flipping a weighted coin for each block of rows. This method does not support fixed-size sampling.
                Default is ``None``. Then the Trino cluster will use "BERNOULLI" by default.

        Note:
            - SYSTEM sampling is often faster than BERNOULLI sampling.

        """
        if sampling_method and sampling_method.upper() not in (
            "BERNOULLI",
            "SYSTEM",
        ):
            raise ValueError(f"'sampling_method' value {sampling_method} must be None or one of 'BERNOULLI', or 'SYSTEM'.")

        # The analyzer will generate a sql with subquery. So we build the sql directly without using the analyzer.
        sampling_method_text = sampling_method or "BERNOULLI"
        sql_text = f"SELECT * FROM {self.table_name} TABLESAMPLE {sampling_method_text} ({str(frac * 100.0)})"
        return self._session.sql(sql_text)

    def update(
        self,
        assignments: Dict[str, ColumnOrLiteral],
        condition: Optional[Column] = None,
        *,
        statement_properties: Optional[Dict[str, str]] = None,
    ) -> UpdateResult:
        """
        Updates rows in the Table with specified ``assignments`` and returns a
        :class:`UpdateResult`, representing the number of rows modified and the
        number of multi-joined rows modified.

        Args:
            assignments: A ``dict`` that associates the names of columns with the
                values that should be updated. The value of ``assignments`` can
                either be a literal value or a :class:`Column` object.
            condition: An optional :class:`Column` object representing the
                specified condition. It must be provided if ``source`` is provided.

        Examples::

            >>> target_df = session.create_dataframe([(1, 1),(1, 2),(2, 1),(2, 2),(3, 1),(3, 2)], schema=["a", "b"])
            >>> target_df.write.save_as_table("my_table", mode="overwrite")
            >>> t = session.table("my_table")

            >>> # update all rows in column "b" to 0 and all rows in column "a"
            >>> # to the summation of column "a" and column "b"
            >>> t.update({"b": 0, "a": t.a + t.b})
            UpdateResult(rows_updated=6, multi_joined_rows_updated=0)
            >>> t.collect()
            [Row(A=2, B=0), Row(A=3, B=0), Row(A=3, B=0), Row(A=4, B=0), Row(A=4, B=0), Row(A=5, B=0)]

            >>> # update all rows in column "b" to 0 where column "a" has value 1
            >>> target_df.write.save_as_table("my_table", mode="overwrite")
            >>> t.update({"b": 0}, t["a"] == 1)
            UpdateResult(rows_updated=2, multi_joined_rows_updated=0)
            >>> t.collect()
            [Row(A=1, B=0), Row(A=1, B=0), Row(A=2, B=1), Row(A=2, B=2), Row(A=3, B=1), Row(A=3, B=2)]
        """
        new_df = self._with_plan(
            TableUpdate(
                table_name=self.table_name,
                assignments=[
                    Assignment(column=Column(k)._expression, value=Column._to_expr(v)) for k, v in assignments.items()
                ],
                condition=condition._expression if condition is not None else None,
            )
        )
        new_df._internal_collect(statement_properties=statement_properties)
        rowcount = new_df._session._conn._cursor.rowcount
        return _get_update_result(rowcount)

    def delete(
        self,
        condition: Optional[Column] = None,
        *,
        statement_properties: Optional[Dict[str, str]] = None,
    ) -> DeleteResult:
        """
        Deletes rows in a Table and returns a :class:`DeleteResult`,
        representing the number of rows deleted.

        Args:
            condition: An optional :class:`Column` object representing the
                specified condition. It must be provided if ``source`` is provided.

        Examples::

            >>> target_df = session.create_dataframe([(1, 1),(1, 2),(2, 1),(2, 2),(3, 1),(3, 2)], schema=["a", "b"])
            >>> target_df.write.save_as_table("my_table", mode="overwrite")
            >>> t = session.table("my_table")

            >>> # delete all rows in a table
            >>> t.delete()
            DeleteResult(rows_deleted=6)
            >>> t.collect()
            []

            >>> # delete all rows where column "a" has value 1
            >>> target_df.write.save_as_table("my_table", mode="overwrite")
            >>> t.delete(t["a"] == 1)
            DeleteResult(rows_deleted=2)
            >>> t.collect()
            [Row(A=2, B=1), Row(A=2, B=2), Row(A=3, B=1), Row(A=3, B=2)]
        """
        new_df = self._with_plan(
            TableDelete(
                table_name=self.table_name,
                condition=condition._expression if condition is not None else None,
            )
        )
        new_df._internal_collect(statement_properties=statement_properties)
        rowcount = new_df._session._conn._cursor.rowcount
        return _get_delete_result(rowcount)

    def merge(
        self,
        source: DataFrame,
        join_expr: Column,
        clauses: Iterable[Union[WhenMatchedClause, WhenNotMatchedClause]],
        *,
        statement_properties: Optional[Dict[str, str]] = None,
    ) -> MergeResult:
        """
        Merges this :class:`Table` with :class:`DataFrame` source on the specified
        join expression and a list of matched or not-matched clauses, and returns
        a :class:`MergeResult`, representing the number of rows inserted,
        updated and deleted by this merge action.
        See `MERGE <https://trino.io/docs/current/sql/merge.html>`_
        for details.

        Args:
            source: A :class:`DataFrame` to join with this :class:`Table`.
                It can also be another :class:`Table`.
            join_expr: A :class:`Column` object representing the expression on which
                to join this :class:`Table` and ``source``.
            clauses: A list of matched or not-matched clauses specifying the actions
                to perform when the values from this :class:`Table` and ``source``
                match or not match on ``join_expr``. These actions can only be instances
                of :class:`WhenMatchedClause` and :class:`WhenNotMatchedClause`, and will
                be performed sequentially in this list.

        Example::

            >>> from pystarburst.functions import when_matched, when_not_matched
            >>> target_df = session.create_dataframe([(10, "old"), (10, "too_old"), (11, "old")], schema=["key", "value"])
            >>> target_df.write.save_as_table("my_table", mode="overwrite")
            >>> target = session.table("my_table")
            >>> source = session.create_dataframe([(10, "new"), (12, "new"), (13, "old")], schema=["key", "value"])
            >>> target.merge(source, target["key"] == source["key"],
            ...              [when_matched().update({"value": source["value"]}), when_not_matched().insert({"key": source["key"]})])
            MergeResult(rows_affected=3)
            >>> target.collect()
            [Row(KEY=13, VALUE=None), Row(KEY=12, VALUE=None), Row(KEY=10, VALUE='new'), Row(KEY=10, VALUE='new'), Row(KEY=11, VALUE='old')]
        """
        merge_exprs = []
        for c in clauses:
            if isinstance(c, WhenMatchedClause):
                if isinstance(c._clause, UpdateMergeExpression):
                    updated = True
                else:
                    deleted = True
            elif isinstance(c, WhenNotMatchedClause):
                inserted = True
            else:
                raise TypeError("clauses only accepts WhenMatchedClause or WhenNotMatchedClause instances")
            merge_exprs.append(c._clause)

        new_df = self._with_plan(
            TableMerge(
                table_name=self.table_name,
                source=_disambiguate(self, source, create_join_type("left"), [])[1]._plan,
                join_expr=join_expr._expression,
                clauses=merge_exprs,
            )
        )
        new_df._internal_collect(statement_properties=statement_properties)
        rowcount = new_df._session._conn._cursor.rowcount
        return _get_merge_result(rowcount)

    def drop_table(self) -> None:
        """Drops the table from the Trino cluster.

        Note that subsequent operations such as :meth:`DataFrame.select`, :meth:`DataFrame.collect` on this ``Table`` instance and the derived DataFrame will raise errors because the underlying
        table in the Trino cluster no longer exists.
        """
        self._session.sql(f"drop table {self.table_name}")._internal_collect()
