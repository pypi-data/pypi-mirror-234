#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

import math
from typing import Any, List
from typing import Literal as TypingLiteral
from typing import Optional

from pydantic import Field, root_validator
from typing_extensions import Annotated

from pystarburst._internal.analyzer.analyzer_utils import quote_name
from pystarburst._internal.analyzer.base_model import BaseModel
from pystarburst._internal.analyzer.expression import (
    Expression,
    ExpressionUnion,
    NamedExpression,
)
from pystarburst._internal.analyzer.plan.trino_plan import TrinoPlan
from pystarburst._internal.error_message import PyStarburstClientExceptionMessages
from pystarburst._internal.type_utils import (
    VALID_PYTHON_TYPES_FOR_LITERAL_VALUE,
    infer_type,
)
from pystarburst._internal.utils import random_string
from pystarburst.types import DataTypeUnion


class ArrayExpression(Expression):
    type: TypingLiteral["ArrayExpression"] = Field("ArrayExpression", alias="@type")
    elements: List[Annotated[ExpressionUnion, Field(discriminator="type")]]


class Attribute(Expression, NamedExpression):
    type: TypingLiteral["Attribute"] = Field("Attribute", alias="@type")
    id: str = Field(default_factory=random_string)
    name: str
    datatype: "DataTypeUnion" = Field(discriminator="type", alias="dataType")
    nullable: bool = Field(True)

    def with_name(self, new_name: str) -> "Attribute":
        if self.name == new_name:
            return self
        else:
            return Attribute(
                name=quote_name(new_name),
                dataType=self.datatype,
                nullable=self.nullable,
            )


class CaseWhen(Expression):
    class Branch(BaseModel):
        condition: Annotated[ExpressionUnion, Field(discriminator="type")]
        result: Annotated[ExpressionUnion, Field(discriminator="type")]

    type: TypingLiteral["CaseWhen"] = Field("CaseWhen", alias="@type")
    else_value: Optional[Annotated[ExpressionUnion, Field(discriminator="type")]] = Field(alias="elseValue")
    branches: List[Branch]


class FunctionExpression(Expression):
    type: TypingLiteral["FunctionExpression"] = Field("FunctionExpression", alias="@type")
    name: str
    is_distinct: bool = Field(False, alias="isDistinct")
    arguments: List[Annotated[ExpressionUnion, Field(discriminator="type")]]


class InExpression(Expression):
    type: TypingLiteral["InExpression"] = Field("InExpression", alias="@type")
    column: Annotated[ExpressionUnion, Field(discriminator="type")]
    values: List[Annotated[ExpressionUnion, Field(discriminator="type")]]


class Like(Expression):
    type: TypingLiteral["Like"] = Field("Like", alias="@type")
    expr: Annotated[ExpressionUnion, Field(discriminator="type", alias="expression")]
    pattern: Annotated[ExpressionUnion, Field(discriminator="type")]


class ListAgg(Expression):
    type: TypingLiteral["ListAgg"] = Field("ListAgg", alias="@type")
    col: Annotated[ExpressionUnion, Field(discriminator="type", alias="column")]
    delimiter: str
    is_distinct: bool = Field(alias="isDistinct")
    within_group: List[Annotated[ExpressionUnion, Field(discriminator="type")]] = Field(alias="withinGroup")


class Literal(Expression):
    type: TypingLiteral["Literal"] = Field("Literal", alias="@type")
    value: Any
    datatype: Optional[DataTypeUnion] = Field(None, discriminator="type", alias="dataType")

    @root_validator()
    def check_literal(cls, values):
        if "value" in values:
            value = values["value"]
            if not isinstance(value, VALID_PYTHON_TYPES_FOR_LITERAL_VALUE):
                raise PyStarburstClientExceptionMessages.PLAN_CANNOT_CREATE_LITERAL(type(value))
            if values.get("datatype") is None:
                values["datatype"] = infer_type(value)
            # work around json encoder limitations
            if isinstance(value, float):
                if value == float("+inf"):
                    values["value"] = "infinity()"
                if value == float("-inf"):
                    values["value"] = "-infinity()"
                if math.isnan(value):
                    values["value"] = "nan()"
        return values


class MultipleExpression(Expression):
    type: TypingLiteral["MultipleExpression"] = Field("MultipleExpression", alias="@type")
    expressions: List[Annotated[ExpressionUnion, Field(discriminator="type")]]


class RegExpLike(Expression):
    type: TypingLiteral["RegExpLike"] = Field("RegExpLike", alias="@type")
    expr: Annotated[ExpressionUnion, Field(discriminator="type", alias="expression")]
    pattern: Annotated[ExpressionUnion, Field(discriminator="type")]


class ScalarSubquery(Expression):
    type: TypingLiteral["ScalarSubquery"] = Field("ScalarSubquery", alias="@type")
    trino_plan: TrinoPlan = Field(alias="trinoPlan")


class Star(Expression):
    type: TypingLiteral["Star"] = Field("Star", alias="@type")
    expressions: List[Annotated[ExpressionUnion, Field(discriminator="type")]]


class UnresolvedAttribute(Expression, NamedExpression):
    type: TypingLiteral["UnresolvedAttribute"] = Field("UnresolvedAttribute", alias="@type")
    name: str
