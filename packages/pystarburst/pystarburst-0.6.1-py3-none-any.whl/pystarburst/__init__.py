#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

"""
Contains core classes of pystarburst.
"""

__all__ = [
    "Column",
    "CaseExpr",
    "Row",
    "Session",
    "DataFrame",
    "DataFrameStatFunctions",
    "DataFrameNaFunctions",
    "DataFrameWriter",
    "GroupingSets",
    "RelationalGroupedDataFrame",
    "Window",
    "WindowSpec",
    "Table",
    "UpdateResult",
    "DeleteResult",
    "MergeResult",
    "WhenMatchedClause",
    "WhenNotMatchedClause",
    "QueryRecord",
    "QueryHistory",
]

from pystarburst import functions
from pystarburst._internal.analyzer.expression.binary import (
    Add,
    And,
    Divide,
    EqualTo,
    GreaterThan,
    GreaterThanOrEqual,
    LessThan,
    LessThanOrEqual,
    Multiply,
    NotEqualTo,
    NullSafeEqualTo,
    Or,
    Remainder,
    Subtract,
)
from pystarburst._internal.analyzer.expression.general import (
    ArrayExpression,
    Attribute,
    CaseWhen,
    FunctionExpression,
    InExpression,
    Like,
    ListAgg,
    Literal,
    MultipleExpression,
    RegExpLike,
    ScalarSubquery,
    Star,
    UnresolvedAttribute,
)
from pystarburst._internal.analyzer.expression.grouping_set import (
    Cube,
    GroupingSetsExpression,
    Rollup,
)
from pystarburst._internal.analyzer.expression.sort import SortOrder
from pystarburst._internal.analyzer.expression.table import (
    Assignment,
    DeleteMergeExpression,
    InsertMergeExpression,
    UpdateMergeExpression,
)
from pystarburst._internal.analyzer.expression.table_function import (
    NamedArgumentsTableFunction,
    PosArgumentsTableFunction,
    TableFunctionPartitionSpecDefinition,
)
from pystarburst._internal.analyzer.expression.unary import (
    Alias,
    Cast,
    IsNotNull,
    IsNull,
    Minus,
    Not,
    SubfieldInt,
    SubfieldString,
    TryCast,
    UnresolvedAlias,
)
from pystarburst._internal.analyzer.expression.window import (
    CurrentRow,
    FirstValue,
    Lag,
    LastValue,
    Lead,
    NthValue,
    RangeFrame,
    RowFrame,
    SpecifiedWindowFrame,
    UnboundedFollowing,
    UnboundedPreceding,
    UnspecifiedFrame,
    WindowExpression,
    WindowSpecDefinition,
)
from pystarburst._internal.analyzer.plan.logical_plan.binary import (
    Except,
    Intersect,
    IntersectAll,
    Join,
    Union,
    UnionAll,
    UsingJoin,
)
from pystarburst._internal.analyzer.plan.logical_plan.leaf import (
    Query,
    Range,
    TrinoValues,
    UnresolvedRelation,
)
from pystarburst._internal.analyzer.plan.logical_plan.table import (
    CreateTable,
    TableDelete,
    TableMerge,
    TableUpdate,
)
from pystarburst._internal.analyzer.plan.logical_plan.table_function import (
    TableFunctionJoin,
    TableFunctionRelation,
)
from pystarburst._internal.analyzer.plan.logical_plan.unary import (
    Aggregate,
    CreateView,
    Filter,
    Limit,
    Pivot,
    Project,
    Sample,
    Sort,
    Unpivot,
)
from pystarburst._internal.analyzer.plan.trino_plan import TrinoPlan
from pystarburst._internal.utils import get_version
from pystarburst.column import CaseExpr, Column
from pystarburst.dataframe import DataFrame
from pystarburst.dataframe_na_functions import DataFrameNaFunctions
from pystarburst.dataframe_stat_functions import DataFrameStatFunctions
from pystarburst.dataframe_writer import DataFrameWriter
from pystarburst.query_history import QueryHistory, QueryRecord
from pystarburst.relational_grouped_dataframe import (
    GroupingSets,
    RelationalGroupedDataFrame,
)
from pystarburst.row import Row
from pystarburst.session import Session
from pystarburst.table import (
    DeleteResult,
    MergeResult,
    Table,
    UpdateResult,
    WhenMatchedClause,
    WhenNotMatchedClause,
)
from pystarburst.types import (
    ArrayType,
    BinaryType,
    BooleanType,
    ByteType,
    CharType,
    DateType,
    DayTimeIntervalType,
    DecimalType,
    DoubleType,
    FloatType,
    IntegerType,
    JsonType,
    LongType,
    MapType,
    NullType,
    ShortType,
    StringType,
    StructField,
    StructType,
    TimeNTZType,
    TimestampNTZType,
    TimestampType,
    TimeType,
    UuidType,
    YearMonthIntervalType,
)
from pystarburst.window import Window, WindowSpec

__version__ = get_version()

_TYPES_MAP = {
    "ArrayType": ArrayType,
    "BinaryType": BinaryType,
    "BooleanType": BooleanType,
    "ByteType": ByteType,
    "CharType": CharType,
    "DateType": DateType,
    "DayTimeIntervalType": DayTimeIntervalType,
    "DecimalType": DecimalType,
    "DoubleType": DoubleType,
    "FloatType": FloatType,
    "IntegerType": IntegerType,
    "JsonType": JsonType,
    "LongType": LongType,
    "MapType": MapType,
    "NullType": NullType,
    "ShortType": ShortType,
    "StringType": StringType,
    "StructType": StructType,
    "StructField": StructField,
    "TimestampNTZType": TimestampNTZType,
    "TimestampType": TimestampType,
    "TimeNTZType": TimeNTZType,
    "TimeType": TimeType,
    "UuidType": UuidType,
    "YearMonthIntervalType": YearMonthIntervalType,
}

_EXPRESSION_MAP = {
    "Add": Add,
    "And": And,
    "Divide": Divide,
    "EqualTo": EqualTo,
    "GreaterThan": GreaterThan,
    "GreaterThanOrEqual": GreaterThanOrEqual,
    "LessThan": LessThan,
    "LessThanOrEqual": LessThanOrEqual,
    "Multiply": Multiply,
    "NotEqualTo": NotEqualTo,
    "NullSafeEqualTo": NullSafeEqualTo,
    "Or": Or,
    "Remainder": Remainder,
    "Subtract": Subtract,
    # groupingset
    "Cube": Cube,
    "GroupingSetsExpression": GroupingSetsExpression,
    "Rollup": Rollup,
    # sort
    "SortOrder": SortOrder,
    # table
    "Assignment": Assignment,
    "DeleteMergeExpression": DeleteMergeExpression,
    "InsertMergeExpression": InsertMergeExpression,
    "UpdateMergeExpression": UpdateMergeExpression,
    # tablefunction
    "NamedArgumentsTableFunction": NamedArgumentsTableFunction,
    "PosArgumentsTableFunction": PosArgumentsTableFunction,
    "TableFunctionPartitionSpecDefinition": TableFunctionPartitionSpecDefinition,
    # unary
    "Alias": Alias,
    "Cast": Cast,
    "IsNotNull": IsNotNull,
    "IsNull": IsNull,
    "Minus": Minus,
    "Not": Not,
    "TryCast": TryCast,
    "UnresolvedAlias": UnresolvedAlias,
    # window
    "CurrentRow": CurrentRow,
    "FirstValue": FirstValue,
    "Lag": Lag,
    "LastValue": LastValue,
    "Lead": Lead,
    "NthValue": NthValue,
    "RangeFrame": RangeFrame,
    "RowFrame": RowFrame,
    "UnboundedFollowing": UnboundedFollowing,
    "UnboundedPreceding": UnboundedPreceding,
    "UnspecifiedFrame": UnspecifiedFrame,
    "WindowExpression": WindowExpression,
    "WindowSpecDefinition": WindowSpecDefinition,
    # general
    "ArrayExpression": ArrayExpression,
    "Attribute": Attribute,
    "CaseWhen": CaseWhen,
    "FunctionExpression": FunctionExpression,
    "InExpression": InExpression,
    "Like": Like,
    "ListAgg": ListAgg,
    "Literal": Literal,
    "MultipleExpression": MultipleExpression,
    "RegExpLike": RegExpLike,
    "ScalarSubquery": ScalarSubquery,
    "Star": Star,
    "SubfieldInt": SubfieldInt,
    "SubfieldString": SubfieldString,
    "UnresolvedAttribute": UnresolvedAttribute,
}

_LOGICAL_PLAN_MAP = {
    # binary
    "Except": Except,
    "Intersect": Intersect,
    "IntersectAll": IntersectAll,
    "Union": Union,
    "UnionAll": UnionAll,
    "Join": Join,
    "UsingJoin": UsingJoin,
    # leaf
    "Query": Query,
    "Range": Range,
    "TrinoValues": TrinoValues,
    "UnresolvedRelation": UnresolvedRelation,
    # table
    "CreateTable": CreateTable,
    "TableDelete": TableDelete,
    "TableMerge": TableMerge,
    "TableUpdate": TableUpdate,
    # table_function
    "TableFunctionRelation": TableFunctionRelation,
    "TableFunctionJoin": TableFunctionJoin,
    # unary
    "Aggregate": Aggregate,
    "CreateView": CreateView,
    "Filter": Filter,
    "Limit": Limit,
    "Pivot": Pivot,
    "Project": Project,
    "Unpivot": Unpivot,
    "Sample": Sample,
    "Sort": Sort,
}

# Types
ArrayType.update_forward_refs()
MapType.update_forward_refs()
StructField.update_forward_refs()

# Expressions
Assignment.update_forward_refs(**_EXPRESSION_MAP)
Add.update_forward_refs(**_EXPRESSION_MAP)
And.update_forward_refs(**_EXPRESSION_MAP)
Divide.update_forward_refs(**_EXPRESSION_MAP)
EqualTo.update_forward_refs(**_EXPRESSION_MAP)
GreaterThan.update_forward_refs(**_EXPRESSION_MAP)
GreaterThanOrEqual.update_forward_refs(**_EXPRESSION_MAP)
LessThan.update_forward_refs(**_EXPRESSION_MAP)
LessThanOrEqual.update_forward_refs(**_EXPRESSION_MAP)
Multiply.update_forward_refs(**_EXPRESSION_MAP)
NotEqualTo.update_forward_refs(**_EXPRESSION_MAP)
NullSafeEqualTo.update_forward_refs(**_EXPRESSION_MAP)
Or.update_forward_refs(**_EXPRESSION_MAP)
Remainder.update_forward_refs(**_EXPRESSION_MAP)
Subtract.update_forward_refs(**_EXPRESSION_MAP)
ArrayExpression.update_forward_refs(**_EXPRESSION_MAP)
Attribute.update_forward_refs(**_EXPRESSION_MAP, **_TYPES_MAP)
Literal.update_forward_refs(**_EXPRESSION_MAP, **_TYPES_MAP)
CaseWhen.update_forward_refs(**_EXPRESSION_MAP)
CaseWhen.Branch.update_forward_refs(**_EXPRESSION_MAP)
FunctionExpression.update_forward_refs(**_EXPRESSION_MAP)
InExpression.update_forward_refs(**_EXPRESSION_MAP)
Like.update_forward_refs(**_EXPRESSION_MAP)
ListAgg.update_forward_refs(**_EXPRESSION_MAP)
MultipleExpression.update_forward_refs(**_EXPRESSION_MAP)
RegExpLike.update_forward_refs(**_EXPRESSION_MAP)
ScalarSubquery.update_forward_refs(**_EXPRESSION_MAP)
Star.update_forward_refs(**_EXPRESSION_MAP)
SubfieldInt.update_forward_refs(**_EXPRESSION_MAP)
SubfieldString.update_forward_refs(**_EXPRESSION_MAP)
UnresolvedAttribute.update_forward_refs(**_EXPRESSION_MAP)
Cube.update_forward_refs(**_EXPRESSION_MAP)
Rollup.update_forward_refs(**_EXPRESSION_MAP)
GroupingSetsExpression.update_forward_refs(**_EXPRESSION_MAP)
SortOrder.update_forward_refs(**_EXPRESSION_MAP)
DeleteMergeExpression.update_forward_refs(**_EXPRESSION_MAP)
InsertMergeExpression.update_forward_refs(**_EXPRESSION_MAP)
UpdateMergeExpression.update_forward_refs(**_EXPRESSION_MAP)
NamedArgumentsTableFunction.update_forward_refs(**_EXPRESSION_MAP)
PosArgumentsTableFunction.update_forward_refs(**_EXPRESSION_MAP)
TableFunctionPartitionSpecDefinition.update_forward_refs(**_EXPRESSION_MAP)
Alias.update_forward_refs(**_EXPRESSION_MAP)
Cast.update_forward_refs(**_EXPRESSION_MAP, **_TYPES_MAP)
IsNotNull.update_forward_refs(**_EXPRESSION_MAP)
IsNull.update_forward_refs(**_EXPRESSION_MAP)
Minus.update_forward_refs(**_EXPRESSION_MAP)
Not.update_forward_refs(**_EXPRESSION_MAP)
TryCast.update_forward_refs(**_EXPRESSION_MAP, **_TYPES_MAP)
UnresolvedAlias.update_forward_refs(**_EXPRESSION_MAP)
SpecifiedWindowFrame.update_forward_refs(**_EXPRESSION_MAP)
WindowSpecDefinition.update_forward_refs(**_EXPRESSION_MAP)
WindowExpression.update_forward_refs(**_EXPRESSION_MAP)
Lag.update_forward_refs(**_EXPRESSION_MAP)
Lead.update_forward_refs(**_EXPRESSION_MAP)
NthValue.update_forward_refs(**_EXPRESSION_MAP)
LastValue.update_forward_refs(**_EXPRESSION_MAP)
FirstValue.update_forward_refs(**_EXPRESSION_MAP)

# Trino plan
TrinoPlan.update_forward_refs(**_EXPRESSION_MAP, **_LOGICAL_PLAN_MAP)

# Logical plans
Aggregate.update_forward_refs(**_EXPRESSION_MAP)
Filter.update_forward_refs(**_EXPRESSION_MAP)
Limit.update_forward_refs(**_EXPRESSION_MAP)
Project.update_forward_refs(**_EXPRESSION_MAP)
Join.update_forward_refs(**_EXPRESSION_MAP)
UsingJoin.update_forward_refs(**_EXPRESSION_MAP)
UpdateMergeExpression.update_forward_refs(**_EXPRESSION_MAP)
CreateTable.update_forward_refs(**_EXPRESSION_MAP)
TableMerge.update_forward_refs(**_EXPRESSION_MAP)
TableUpdate.update_forward_refs(**_EXPRESSION_MAP)
Pivot.update_forward_refs(**_EXPRESSION_MAP)
Unpivot.update_forward_refs(**_EXPRESSION_MAP)
# TODO: add all plans here
