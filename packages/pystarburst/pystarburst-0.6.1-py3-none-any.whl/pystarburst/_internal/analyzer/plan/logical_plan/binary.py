#
# Copyright (c) 2012-2022 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from enum import Enum
from typing import Annotated, List, Literal, Optional

from pydantic import Field

from pystarburst._internal.analyzer.expression.general import ExpressionUnion
from pystarburst._internal.analyzer.plan.logical_plan import LogicalPlan
from pystarburst._internal.analyzer.plan.trino_plan import TrinoPlan
from pystarburst._internal.error_message import PyStarburstClientExceptionMessages

SUPPORTED_JOIN_TYPE_STR = [
    "inner",
    "outer",
    "full",
    "fullouter",
    "leftouter",
    "left",
    "rightouter",
    "right",
    "leftsemi",
    "semi",
    "leftanti",
    "anti",
    "cross",
]


class BinaryNode(LogicalPlan):
    left: TrinoPlan
    right: TrinoPlan


class SetOperation(BinaryNode):
    pass


class Except(SetOperation):
    type: Literal["Except"] = Field("Except", alias="@type")


class Intersect(SetOperation):
    type: Literal["Intersect"] = Field("Intersect", alias="@type")


class IntersectAll(SetOperation):
    type: Literal["IntersectAll"] = Field("IntersectAll", alias="@type")


class Union(SetOperation):
    type: Literal["Union"] = Field("Union", alias="@type")


class UnionAll(SetOperation):
    type: Literal["UnionAll"] = Field("UnionAll", alias="@type")


class JoinType(str, Enum):
    INNER_JOIN = "INNER_JOIN"
    CROSS_JOIN = "CROSS_JOIN"
    LEFT_OUTER_JOIN = "LEFT_OUTER_JOIN"
    RIGHT_OUTER_JOIN = "RIGHT_OUTER_JOIN"
    FULL_OUTER_JOIN = "FULL_OUTER_JOIN"
    LEFT_SEMI_JOIN = "LEFT_SEMI_JOIN"
    ANTI_JOIN = "ANTI_JOIN"


class Join(BinaryNode):
    type: Literal["Join"] = Field("Join", alias="@type")
    join_type: str = Field(alias="joinType")
    condition: Optional[Annotated[ExpressionUnion, Field(discriminator="type")]]


class UsingJoin(BinaryNode):
    type: Literal["UsingJoin"] = Field("UsingJoin", alias="@type")
    join_type: str = Field(alias="joinType")
    using_columns: List[str] = Field(alias="usingColumns")


def create_join_type(join_type: str) -> "JoinType":
    jt = join_type.strip().lower().replace("_", "")

    if jt == "inner":
        return JoinType.INNER_JOIN

    if jt in ["outer", "full", "fullouter"]:
        return JoinType.FULL_OUTER_JOIN

    if jt in ["leftouter", "left"]:
        return JoinType.LEFT_OUTER_JOIN

    if jt in ["rightouter", "right"]:
        return JoinType.RIGHT_OUTER_JOIN

    if jt in ["leftsemi", "semi"]:
        return JoinType.LEFT_SEMI_JOIN

    if jt in ["leftanti", "anti"]:
        return JoinType.ANTI_JOIN

    if jt == "cross":
        return JoinType.CROSS_JOIN

    raise PyStarburstClientExceptionMessages.DF_JOIN_INVALID_JOIN_TYPE(join_type, ", ".join(SUPPORTED_JOIN_TYPE_STR))
