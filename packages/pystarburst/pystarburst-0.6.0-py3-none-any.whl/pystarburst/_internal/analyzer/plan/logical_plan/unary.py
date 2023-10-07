#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from typing import Annotated, List, Literal

from pydantic import Field

from pystarburst._internal.analyzer.expression.general import ExpressionUnion
from pystarburst._internal.analyzer.expression.sort import SortOrder
from pystarburst._internal.analyzer.plan.logical_plan import LogicalPlan
from pystarburst._internal.analyzer.plan.trino_plan import TrinoPlan


class UnaryNode(LogicalPlan):
    child: TrinoPlan


class Aggregate(UnaryNode):
    type: Literal["Aggregate"] = Field("Aggregate", alias="@type")
    grouping_expressions: List[Annotated[ExpressionUnion, Field(discriminator="type")]] = Field(alias="groupingExpressions")
    aggregate_expressions: List[Annotated[ExpressionUnion, Field(discriminator="type")]] = Field(alias="aggregateExpressions")


class CreateView(UnaryNode):
    type: Literal["CreateView"] = Field("CreateView", alias="@type")
    name: str


class Filter(UnaryNode):
    type: Literal["Filter"] = Field("Filter", alias="@type")
    condition: ExpressionUnion = Field(discriminator="type")


class Limit(UnaryNode):
    type: Literal["Limit"] = Field("Limit", alias="@type")
    limit_expr: ExpressionUnion = Field(alias="limitExpression", discriminator="type")
    offset_expr: ExpressionUnion = Field(alias="offsetExpression", discriminator="type")


class Project(UnaryNode):
    type: Literal["Project"] = Field("Project", alias="@type")
    project_list: List[Annotated[ExpressionUnion, Field(discriminator="type")]] = Field(alias="projectList")


class Sample(UnaryNode):
    type: Literal["Sample"] = Field("Sample", alias="@type")
    probability_fraction: float = Field(0, alias="probabilityFraction")


class Sort(UnaryNode):
    type: Literal["Sort"] = Field("Sort", alias="@type")
    order: List[SortOrder]
    is_global: bool = Field(False, alias="global")


class Pivot(UnaryNode):
    type: Literal["Pivot"] = Field("Pivot", alias="@type")
    pivot_column: ExpressionUnion = Field(alias="pivotColumn", discriminator="type")
    pivot_values: List[Annotated[ExpressionUnion, Field(discriminator="type")]] = Field(alias="pivotValues")
    aggregates: List[Annotated[ExpressionUnion, Field(discriminator="type")]]


class Unpivot(UnaryNode):
    type: Literal["Unpivot"] = Field("Unpivot", alias="@type")
    ids_column_list: List[Annotated[ExpressionUnion, Field(discriminator="type")]] = Field(alias="idsColumnList")
    unpivot_column_list: List[Annotated[ExpressionUnion, Field(discriminator="type")]] = Field(alias="unpivotColumnList")
    name_column: str = Field(alias="nameColumn")
    value_column: str = Field(alias="valueColumn")
