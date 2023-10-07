#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from typing import Literal

from pydantic import Field

from pystarburst._internal.analyzer.expression.table_function import (
    TableFunctionExpression,
)
from pystarburst._internal.analyzer.plan.logical_plan import LogicalPlan


class TableFunctionRelation(LogicalPlan):
    type: Literal["TableFunctionRelation"] = Field("TableFunctionRelation", alias="@type")
    table_function: TableFunctionExpression


class TableFunctionJoin(LogicalPlan):
    type: Literal["TableFunctionJoin"] = Field("TableFunctionJoin", alias="@type")
    child: LogicalPlan
    table_function: TableFunctionExpression
