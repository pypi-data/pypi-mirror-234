#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from typing import Literal

from pydantic import Field
from typing_extensions import Annotated

from pystarburst._internal.analyzer.expression import Expression, ExpressionUnion


class BinaryExpression(Expression):
    left: Annotated[ExpressionUnion, Field(discriminator="type")]
    right: Annotated[ExpressionUnion, Field(discriminator="type")]


class EqualTo(BinaryExpression):
    type: Literal["EqualTo"] = Field("EqualTo", alias="@type")


class NullSafeEqualTo(BinaryExpression):
    type: Literal["NullSafeEqualTo"] = Field("NullSafeEqualTo", alias="@type")


class NotEqualTo(BinaryExpression):
    type: Literal["NotEqualTo"] = Field("NotEqualTo", alias="@type")


class GreaterThan(BinaryExpression):
    type: Literal["GreaterThan"] = Field("GreaterThan", alias="@type")


class LessThan(BinaryExpression):
    type: Literal["LessThan"] = Field("LessThan", alias="@type")


class GreaterThanOrEqual(BinaryExpression):
    type: Literal["GreaterThanOrEqual"] = Field("GreaterThanOrEqual", alias="@type")


class LessThanOrEqual(BinaryExpression):
    type: Literal["LessThanOrEqual"] = Field("LessThanOrEqual", alias="@type")


class And(BinaryExpression):
    type: Literal["And"] = Field("And", alias="@type")


class Or(BinaryExpression):
    type: Literal["Or"] = Field("Or", alias="@type")


class Add(BinaryExpression):
    type: Literal["Add"] = Field("Add", alias="@type")


class Subtract(BinaryExpression):
    type: Literal["Subtract"] = Field("Subtract", alias="@type")


class Multiply(BinaryExpression):
    type: Literal["Multiply"] = Field("Multiply", alias="@type")


class Divide(BinaryExpression):
    type: Literal["Divide"] = Field("Divide", alias="@type")


class Remainder(BinaryExpression):
    type: Literal["Remainder"] = Field("Remainder", alias="@type")
