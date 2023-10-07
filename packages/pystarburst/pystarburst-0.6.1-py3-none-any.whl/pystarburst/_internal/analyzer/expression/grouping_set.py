#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from typing import Annotated, List, Literal

from pydantic import Field

from pystarburst._internal.analyzer.expression import Expression, ExpressionUnion


class GroupingSet(Expression):
    group_by_exprs: List[Annotated[ExpressionUnion, Field(discriminator="type")]] = Field(alias="groupByExpressions")


class Cube(GroupingSet):
    type: Literal["Cube"] = Field("Cube", alias="@type")


class Rollup(GroupingSet):
    type: Literal["Rollup"] = Field("Rollup", alias="@type")


class GroupingSetsExpression(Expression):
    type: Literal["GroupingSets"] = Field("GroupingSets", alias="@type")
    args: List[List[Annotated[ExpressionUnion, Field(discriminator="type")]]] = Field(alias="groupByExpressionsLists")
