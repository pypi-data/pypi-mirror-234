#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from typing import List, Literal, Optional

from pydantic import Field
from typing_extensions import Annotated

from pystarburst._internal.analyzer.expression import Expression, ExpressionUnion


class MergeExpression(Expression):
    condition: Optional[Annotated[ExpressionUnion, Field(discriminator="type")]]


class Assignment(Expression):
    type: Literal["Assignment"] = Field("Assignment", alias="@type")
    column: Annotated[ExpressionUnion, Field(discriminator="type")]
    value: Annotated[ExpressionUnion, Field(discriminator="type")]


class UpdateMergeExpression(MergeExpression):
    type: Literal["UpdateMerge"] = Field("UpdateMerge", alias="@type")
    assignments: List[Assignment]


class DeleteMergeExpression(MergeExpression):
    type: Literal["DeleteMerge"] = Field("DeleteMerge", alias="@type")


class InsertMergeExpression(MergeExpression):
    type: Literal["InsertMerge"] = Field("InsertMerge", alias="@type")
    keys: List[Annotated[ExpressionUnion, Field(discriminator="type")]]
    values: List[Annotated[ExpressionUnion, Field(discriminator="type")]]
