#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from typing import List
from typing import Literal as TypingLiteral
from typing import Optional

from pydantic import Field

from pystarburst._internal.analyzer.expression.general import Attribute, Literal
from pystarburst._internal.analyzer.plan.logical_plan import LogicalPlan


class LeafNode(LogicalPlan):
    pass


class Query(LeafNode):
    type: TypingLiteral["Query"] = Field("Query", alias="@type")
    sql: str = Field("", alias="query")


class Range(LeafNode):
    type: TypingLiteral["Range"] = Field("Range", alias="@type")
    start: int = Field(0)
    end: int = Field(0)
    step: int = Field(1)
    resolution: str = Field("server")


class TrinoValues(LeafNode):
    type: TypingLiteral["TrinoValues"] = Field("TrinoValues", alias="@type")
    attributes: List[Attribute]
    data: Optional[List[List[Literal]]]


class UnresolvedRelation(LeafNode):
    type: TypingLiteral["UnresolvedRelation"] = Field("UnresolvedRelation", alias="@type")
    name: str
