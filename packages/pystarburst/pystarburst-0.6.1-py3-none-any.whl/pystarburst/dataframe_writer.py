#
# Copyright (c) 2012-2022 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from typing import Dict, Iterable, Optional, Union

import pystarburst  # for forward references of type hints
from pystarburst import Literal
from pystarburst._internal.analyzer.plan.logical_plan.table import CreateTable, SaveMode
from pystarburst._internal.utils import str_to_enum, validate_object_name


class DataFrameWriter:
    """Provides methods for writing data from a :class:`DataFrame` to supported output destinations.

    To use this object:

    1. Create an instance of a :class:`DataFrameWriter` by accessing the :attr:`DataFrame.write` property.
    2. (Optional) Specify the save mode by calling :meth:`mode`, which returns the same
       :class:`DataFrameWriter` that is configured to save data using the specified mode.
       The default mode is "errorifexists".
    3. Call :meth:`save_as_table` or :meth:`copy_into_location` to save the data to the
       specified destination.
    """

    def __init__(self, dataframe: "pystarburst.dataframe.DataFrame") -> None:
        self._dataframe = dataframe
        self._save_mode = SaveMode.ERRORIFEXISTS

    def mode(self, save_mode: str) -> "DataFrameWriter":
        """Set the save mode of this :class:`DataFrameWriter`.

        Args:
            save_mode: One of the following strings.

                "append": Append data of this DataFrame to existing data.

                "overwrite": Overwrite existing data.

                "errorifexists": Throw an exception if data already exists.

                "ignore": Ignore this operation if data already exists.

                Default value is "errorifexists".

        Returns:
            The :class:`DataFrameWriter` itself.
        """
        self._save_mode = str_to_enum(save_mode, SaveMode, "`save_mode`")
        return self

    def save_as_table(
        self,
        table_name: Union[str, Iterable[str]],
        *,
        mode: Optional[str] = None,
        column_order: str = "index",
        table_properties: Dict[str, Union[str, bool, int, float]] = None,
        statement_properties: Optional[Dict[str, str]] = None,
    ) -> None:
        """Writes the data to the specified table in a Trino cluster.

        Args:
            table_name: A string or list of strings that specify the table name or fully-qualified object identifier
                (database name, schema name, and table name).
            mode: One of the following values. When it's ``None`` or not provided,
                the save mode set by :meth:`mode` is used.

                "append": Append data of this DataFrame to existing data.

                "overwrite": Overwrite existing data.

                "errorifexists": Throw an exception if data already exists.

                "ignore": Ignore this operation if data already exists.

            column_order: When ``mode`` is "append", data will be inserted into the target table by matching column sequence or column name. Default is "index". When ``mode`` is not "append", the ``column_order`` makes no difference.

                "index": Data will be inserted into the target table by column sequence.
                "name": Data will be inserted into the target table by matching column names. If the target table has more columns than the source DataFrame, use this one.

            table_properties: Any custom table properties used to create the table.

        Examples::

            >>> df = session.create_dataframe([[1,2],[3,4]], schema=["a", "b"])
            >>> df.write.mode("overwrite").save_as_table("my_table")
            >>> session.table("my_table").collect()
            [Row(A=1, B=2), Row(A=3, B=4)]
            >>> df.write.save_as_table("my_table", mode="append")
            >>> session.table("my_table").collect()
            [Row(A=1, B=2), Row(A=3, B=4), Row(A=1, B=2), Row(A=3, B=4)]
            >>> df.write.mode("overwrite").save_as_table("my_table", table_properties={"format": "parquet"})
            >>> session.table("my_table").collect()
            [Row(A=1, B=2), Row(A=3, B=4)]
        """
        save_mode = str_to_enum(mode, SaveMode, "'mode'") if mode else self._save_mode
        full_table_name = table_name if isinstance(table_name, str) else ".".join(table_name)
        validate_object_name(full_table_name)
        if column_order is None or column_order.lower() not in ("name", "index"):
            raise ValueError("'column_order' must be either 'name' or 'index'")
        column_names = self._dataframe.columns if column_order.lower() == "name" else None

        create_table_logic_plan = CreateTable(
            table_name=full_table_name,
            column_names=column_names,
            mode=save_mode,
            query=self._dataframe._plan,
            table_properties={k: Literal(value=v) for k, v in table_properties.items()}
            if table_properties is not None
            else None,
        )
        session = self._dataframe._session
        trino_plan = self._dataframe._session._analyzer.resolve(create_table_logic_plan)
        session._conn.execute(trino_plan, statement_properties=statement_properties)

    saveAsTable = save_as_table
