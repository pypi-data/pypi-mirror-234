#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from typing import Union

from pystarburst._internal.analyzer.base_model import BaseModel

ExpressionUnion = Union[
    # binary
    "Add",
    "And",
    "Divide",
    "EqualTo",
    "GreaterThan",
    "GreaterThanOrEqual",
    "LessThan",
    "LessThanOrEqual",
    "Multiply",
    "NotEqualTo",
    "NullSafeEqualTo",
    "Or",
    "Remainder",
    "Subtract",
    # groupingset
    "Cube",
    "GroupingSetsExpression",
    "Rollup",
    # sort
    "SortOrder",
    # table
    "Assignment",
    "DeleteMergeExpression",
    "InsertMergeExpression",
    "UpdateMergeExpression",
    # tablefunction
    "NamedArgumentsTableFunction",
    "PosArgumentsTableFunction",
    "TableFunctionPartitionSpecDefinition",
    # unary
    "Alias",
    "Cast",
    "IsNotNull",
    "IsNull",
    "Minus",
    "Not",
    "TryCast",
    "UnresolvedAlias",
    # window
    "CurrentRow",
    "FirstValue",
    "Lag",
    "LastValue",
    "Lead",
    "NthValue",
    "RangeFrame",
    "RowFrame",
    "UnboundedFollowing",
    "UnboundedPreceding",
    "UnspecifiedFrame",
    "WindowExpression",
    "WindowSpecDefinition",
    # general
    "ArrayExpression",
    "Attribute",
    "CaseWhen",
    "FunctionExpression",
    "InExpression",
    "Like",
    "ListAgg",
    "Literal",
    "MultipleExpression",
    "RegExpLike",
    "ScalarSubquery",
    "Star",
    "SubfieldInt",
    "SubfieldString",
    "UnresolvedAttribute",
]


class Expression(BaseModel):
    pass


class NamedExpression:
    pass
