#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from typing import Literal

from pydantic import Field
from typing_extensions import Annotated

from pystarburst._internal.analyzer.expression.general import (
    Expression,
    ExpressionUnion,
    NamedExpression,
)
from pystarburst.types import DataTypeUnion


class UnaryExpression(Expression):
    child: Annotated[ExpressionUnion, Field(discriminator="type")]


class Alias(UnaryExpression, NamedExpression):
    type: Literal["Alias"] = Field("Alias", alias="@type")
    name: str


class Cast(UnaryExpression):
    type: Literal["Cast"] = Field("Cast", alias="@type")
    to: DataTypeUnion = Field(discriminator="type")


class TryCast(UnaryExpression):
    type: Literal["TryCast"] = Field("TryCast", alias="@type")
    to: DataTypeUnion = Field(discriminator="type")


class Minus(UnaryExpression):
    type: Literal["Minus"] = Field("Minus", alias="@type")


class IsNull(UnaryExpression):
    type: Literal["IsNull"] = Field("IsNull", alias="@type")


class IsNotNull(UnaryExpression):
    type: Literal["IsNotNull"] = Field("IsNotNull", alias="@type")


class Not(UnaryExpression):
    type: Literal["Not"] = Field("Not", alias="@type")


class UnresolvedAlias(UnaryExpression, NamedExpression):
    type: Literal["UnresolvedAlias"] = Field("UnresolvedAlias", alias="@type")


class SubfieldInt(UnaryExpression):
    type: Literal["SubfieldInt"] = Field("SubfieldInt", alias="@type")
    field: int


class SubfieldString(UnaryExpression):
    type: Literal["SubfieldString"] = Field("SubfieldString", alias="@type")
    field: str
