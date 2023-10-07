#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from typing import Union

from pystarburst._internal.analyzer.base_model import BaseModel


class LogicalPlan(BaseModel):
    pass


LogicalPlanUnion = Union[
    # binary
    "Except",
    "Intersect",
    "IntersectAll",
    "Union",
    "UnionAll",
    "Join",
    "UsingJoin",
    # leaf
    "Query",
    "Range",
    "TrinoValues",
    "UnresolvedRelation",
    # table
    "CreateTable",
    "TableDelete",
    "TableMerge",
    "TableUpdate",
    # table_function
    "TableFunctionRelation",
    "TableFunctionJoin",
    # unary
    "Aggregate",
    "CreateView",
    "Filter",
    "Limit",
    "Pivot",
    "Project",
    "Unpivot",
    "Sample",
    "Sort",
]
