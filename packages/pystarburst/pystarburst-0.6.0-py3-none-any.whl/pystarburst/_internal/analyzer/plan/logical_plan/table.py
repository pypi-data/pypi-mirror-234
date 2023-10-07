#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from enum import Enum
from typing import Dict, List, Literal, Optional

from pydantic import Field
from typing_extensions import Annotated

from pystarburst._internal.analyzer.expression import Expression, ExpressionUnion
from pystarburst._internal.analyzer.expression.table import Assignment
from pystarburst._internal.analyzer.plan.logical_plan import LogicalPlan
from pystarburst._internal.analyzer.plan.trino_plan import TrinoPlan


class SaveMode(str, Enum):
    APPEND = "APPEND"
    OVERWRITE = "OVERWRITE"
    ERRORIFEXISTS = "ERRORIFEXISTS"
    IGNORE = "IGNORE"


class CreateTable(LogicalPlan):
    type: Literal["CreateTable"] = Field("CreateTable", alias="@type")
    mode: SaveMode = Field(alias="saveMode")
    table_name: str = Field(alias="tableName")
    column_names: Optional[List[str]] = Field(alias="columnNames")
    query: TrinoPlan
    table_properties: Optional[Dict[str, ExpressionUnion]] = Field(alias="tableProperties")


class TableDelete(LogicalPlan):
    type: Literal["TableDelete"] = Field("TableDelete", alias="@type")
    table_name: str = Field(alias="tableName")
    condition: Optional[Expression]


class TableMerge(LogicalPlan):
    type: Literal["TableMerge"] = Field("TableMerge", alias="@type")
    table_name: str = Field(alias="tableName")
    source: TrinoPlan
    join_expr: ExpressionUnion = Field(alias="joinExpression", discriminator="type")
    clauses: List[Annotated[ExpressionUnion, Field(discriminator="type")]]


class TableUpdate(LogicalPlan):
    type: Literal["TableUpdate"] = Field("TableUpdate", alias="@type")
    table_name: str = Field(alias="tableName")
    assignments: List[Assignment]
    condition: Optional[Annotated[ExpressionUnion, Field(discriminator="type")]]
