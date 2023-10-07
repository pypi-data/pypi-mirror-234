#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from typing import List, Literal, Optional, Union

from pydantic import Field
from typing_extensions import Annotated

from pystarburst._internal.analyzer.base_model import BaseModel
from pystarburst._internal.analyzer.expression import Expression, ExpressionUnion
from pystarburst._internal.analyzer.expression.sort import SortOrder


class SpecialFrameBoundary(Expression):
    pass


class UnboundedPreceding(SpecialFrameBoundary):
    type: Literal["UnboundedPreceding"] = Field("UnboundedPreceding", alias="@type")


class UnboundedFollowing(SpecialFrameBoundary):
    type: Literal["UnboundedFollowing"] = Field("UnboundedFollowing", alias="@type")


class CurrentRow(SpecialFrameBoundary):
    type: Literal["CurrentRow"] = Field("CurrentRow", alias="@type")


class FrameType(BaseModel):
    pass


class RowFrame(FrameType):
    type: Literal["RowFrame"] = Field("RowFrame", alias="@type")


class RangeFrame(FrameType):
    type: Literal["RangeFrame"] = Field("RangeFrame", alias="@type")


FrameTypeUnion = Union[RowFrame, RangeFrame]


class WindowFrame(Expression):
    pass


class UnspecifiedFrame(WindowFrame):
    type: Literal["UnspecifiedFrame"] = Field("UnspecifiedFrame", alias="@type")


class SpecifiedWindowFrame(WindowFrame):
    type: Literal["SpecifiedWindowFrame"] = Field("SpecifiedWindowFrame", alias="@type")
    frame_type: FrameTypeUnion = Field(discriminator="type", alias="frameType")
    lower: Annotated[ExpressionUnion, Field(discriminator="type")]
    upper: Annotated[ExpressionUnion, Field(discriminator="type")]


WindowFrameUnion = Union[UnspecifiedFrame, SpecifiedWindowFrame]


class WindowSpecDefinition(Expression):
    type: Literal["WindowSpecDefinition"] = Field("WindowSpecDefinition", alias="@type")
    partition_spec: Optional[List[Annotated[ExpressionUnion, Field(discriminator="type")]]] = Field(alias="partitionSpec")
    order_spec: Optional[List[SortOrder]] = Field(alias="orderSpec")
    frame_spec: WindowFrameUnion = Field(discriminator="type", alias="frameSpec")


class WindowExpression(Expression):
    type: Literal["Window"] = Field("Window", alias="@type")
    window_function: Annotated[ExpressionUnion, Field(discriminator="type", alias="windowFunction")]
    window_spec: WindowSpecDefinition = Field(alias="windowSpecDefinition")


class RankRelatedFunctionExpression(Expression):
    expr: Annotated[ExpressionUnion, Field(alias="expression", discriminator="type")]
    offset: Optional[int]
    default: Optional[Annotated[ExpressionUnion, Field(discriminator="type")]] = Field(alias="defaultExpression")
    ignore_nulls: bool = Field(alias="ignoreNulls")


class Lag(RankRelatedFunctionExpression):
    type: Literal["Lag"] = Field("Lag", alias="@type")


class Lead(RankRelatedFunctionExpression):
    type: Literal["Lead"] = Field("Lead", alias="@type")


class NthValue(RankRelatedFunctionExpression):
    type: Literal["NthValue"] = Field("NthValue", alias="@type")


class LastValue(RankRelatedFunctionExpression):
    type: Literal["LastValue"] = Field("LastValue", alias="@type")


class FirstValue(RankRelatedFunctionExpression):
    type: Literal["FirstValue"] = Field("FirstValue", alias="@type")
