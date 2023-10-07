#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from enum import Enum
from typing import Literal, Optional

from pydantic import Field

from pystarburst._internal.analyzer.expression.unary import UnaryExpression


class NullOrdering(str, Enum):
    NULLS_FIRST = "NULLS_FIRST"
    NULLS_LAST = "NULLS_LAST"


class SortDirection(str, Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class SortOrder(UnaryExpression):
    type: Literal["SortOrder"] = Field("SortOrder", alias="@type")
    direction: SortDirection = Field(SortDirection.ASCENDING, alias="direction")
    null_ordering: Optional[NullOrdering] = Field(None, alias="nullOrdering")
