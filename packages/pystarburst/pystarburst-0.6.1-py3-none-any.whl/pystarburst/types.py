#
# Copyright (c) 2012-2022 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

"""This package contains all pystarburst logical types."""
import re
from typing import List, Literal, Optional, Union

from pydantic import Field

import pystarburst._internal.analyzer.expression as expression
from pystarburst._internal.analyzer.base_model import BaseModel

DataTypeUnion = Union[
    "ArrayType",
    "BinaryType",
    "BooleanType",
    "ByteType",
    "CharType",
    "DateType",
    "DayTimeIntervalType",
    "DecimalType",
    "DoubleType",
    "FloatType",
    "JsonType",
    "IntegerType",
    "LongType",
    "MapType",
    "NullType",
    "ShortType",
    "StringType",
    "StructType",
    "TimestampNTZType",
    "TimestampType",
    "TimeNTZType",
    "TimeType",
    "UuidType",
    "YearMonthIntervalType",
]


class DataType(BaseModel):
    """The base class of PyStarburst data types."""

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"{self.__class__.__name__}()"


# Data types
class NullType(DataType):
    """Represents a null type."""

    type: Literal["NullType"] = Field("NullType", alias="@type")


class _AtomicType(DataType):
    pass


class _SizableType(_AtomicType):
    size: Optional[int] = Field(None)

    def __init__(self, size: int = None, **kwargs):
        if size is not None:
            kwargs["size"] = size
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        if self.size:
            return f"{self.__class__.__name__}({self.size})"
        return super().__repr__()


# Atomic types
class BinaryType(_AtomicType):
    """Binary data type. This maps to the VARBINARY data type in Trino."""

    type: Literal["BinaryType"] = Field("BinaryType", alias="@type")


class BooleanType(_AtomicType):
    """Boolean data type. This maps to the BOOLEAN data type in Trino."""

    type: Literal["BooleanType"] = Field("BooleanType", alias="@type")


class CharType(_SizableType):
    """Char data types. This maps to the CHAR data type in Trino"""

    type: Literal["CharType"] = Field("CharType", alias="@type")


class DateType(_AtomicType):
    """Date data type. This maps to the DATE data type in Trino."""

    type: Literal["DateType"] = Field("DateType", alias="@type")


class StringType(_SizableType):
    """String data type. This maps to the VARCHAR data type in Trino."""

    type: Literal["StringType"] = Field("StringType", alias="@type")


class UuidType(_AtomicType):
    """UUID data type. This maps to the UUID data type in Trino."""

    type: Literal["UuidType"] = Field("UuidType", alias="@type")


class _NumericType(_AtomicType):
    pass


class TimestampNTZType(_SizableType):
    """Timestamp data type. This maps to the TIMESTAMP data type in Trino."""

    type: Literal["TimestampNTZType"] = Field("TimestampNTZType", alias="@type")


class TimestampType(_SizableType):
    """Timestamp with timezone data type. This maps to the TIMESTAMP WITH TIME ZONE data type in Trino."""

    type: Literal["TimestampType"] = Field("TimestampType", alias="@type")


class TimeNTZType(_SizableType):
    """Time data type. This maps to the TIME data type in Trino."""

    type: Literal["TimeNTZType"] = Field("TimeNTZType", alias="@type")


class TimeType(_SizableType):
    """Time with timezone data type. This maps to the TIME WITH TIME ZONE data type in Trino."""

    type: Literal["TimeType"] = Field("TimeType", alias="@type")


# Interval types
class YearMonthIntervalType(_AtomicType):
    """YearMonthIntervalType data type. This maps to the INTERVAL YEAR TO MONTH data type in Trino."""

    type: Literal["YearMonthIntervalType"] = Field("YearMonthIntervalType", alias="@type")


class DayTimeIntervalType(_AtomicType):
    """DayTimeIntervalType data type. This maps to the INTERVAL DAY TO SECOND data type in Trino."""

    type: Literal["DayTimeIntervalType"] = Field("DayTimeIntervalType", alias="@type")


# Numeric types
class _IntegralType(_NumericType):
    pass


class _FractionalType(_NumericType):
    pass


class ByteType(_IntegralType):
    """Byte data type. This maps to the TINYINT data type in Trino."""

    type: Literal["ByteType"] = Field("ByteType", alias="@type")


class ShortType(_IntegralType):
    """Short integer data type. This maps to the SMALLINT data type in Trino."""

    type: Literal["ShortType"] = Field("ShortType", alias="@type")


class IntegerType(_IntegralType):
    """Integer data type. This maps to the INTEGER data type in Trino."""

    type: Literal["IntegerType"] = Field("IntegerType", alias="@type")


class LongType(_IntegralType):
    """Long integer data type. This maps to the BIGINT data type in Trino."""

    type: Literal["LongType"] = Field("LongType", alias="@type")


class FloatType(_FractionalType):
    """Float data type. This maps to the REAL data type in Trino."""

    type: Literal["FloatType"] = Field("FloatType", alias="@type")


class DoubleType(_FractionalType):
    """Double data type. This maps to the DOUBLE data type in Trino."""

    type: Literal["DoubleType"] = Field("DoubleType", alias="@type")


class DecimalType(_FractionalType):
    """Decimal data type. This maps to the DECIMAL data type in Trino."""

    precision: int = Field(38)
    scale: int = Field(0)
    type: Literal["DecimalType"] = Field("DecimalType", alias="@type")

    def __init__(self, precision: int = None, scale: int = None, **kwargs):
        if precision is not None:
            kwargs["precision"] = precision
        if scale is not None:
            kwargs["scale"] = scale
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.precision}, {self.scale})"


class JsonType(DataType):
    """Json data type. This maps to the JSON data type in Trino."""

    type: Literal["JsonType"] = Field("JsonType", alias="@type")


class ArrayType(DataType):
    """Array data type. This maps to the ARRAY data type in Trino."""

    type: Literal["ArrayType"] = Field("ArrayType", alias="@type")
    element_type: Optional[DataTypeUnion] = Field(StringType(), alias="elementType", discriminator="type")

    def __init__(self, element_type: DataType = None, **kwargs):
        if element_type is None:
            element_type = StringType()
        super().__init__(element_type=element_type, **kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.element_type)})"


class MapType(DataType):
    """Map data type. This maps to the MAP data type in Trino."""

    type: Literal["MapType"] = Field("MapType", alias="@type")
    key_type: Optional[DataTypeUnion] = Field(StringType(), alias="keyType", discriminator="type")
    value_type: Optional[DataTypeUnion] = Field(StringType(), alias="valueType", discriminator="type")

    def __init__(self, key_type: DataType = None, value_type: DataType = None, **kwargs):
        if key_type is None:
            key_type = StringType()
        if value_type is None:
            value_type = StringType()
        super().__init__(key_type=key_type, value_type=value_type, **kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.key_type)}, {repr(self.value_type)})"


class ColumnIdentifier(BaseModel):
    """Represents a column identifier."""

    normalized_name: str = Field(alias="normalizedName")

    def __init__(self, normalized_name: str = None, **kwargs) -> None:
        super().__init__(normalized_name=normalized_name, **kwargs)

    @property
    def name(self) -> str:
        return ColumnIdentifier._strip_unnecessary_quotes(self.normalized_name)

    @property
    def quoted_name(self) -> str:
        return self.normalized_name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.normalized_name == other
        elif isinstance(other, ColumnIdentifier):
            return self.normalized_name == other.normalized_name
        else:
            return False

    @staticmethod
    def _strip_unnecessary_quotes(string: str) -> str:
        """Removes the unnecessary quotes from name.

        Remove quotes if name starts with _a-zA-Z and only contains _0-9a-zA-Z$.
        """
        remove_quote = re.compile('^"([_a-z]+[_a-z0-9$]*)"$', re.IGNORECASE)
        result = remove_quote.search(string)
        return string[1:-1] if result else string


class StructField(BaseModel):
    """Represents the content of :class:`StructField`."""

    column_identifier: Union[ColumnIdentifier, str] = Field(None, alias="columnIdentifier")
    datatype: DataTypeUnion = Field(alias="dataType", discriminator="type")
    nullable: bool = Field(False)

    def __init__(
        self, column_identifier: Union[ColumnIdentifier, str] = None, datatype: DataType = None, nullable: bool = True, **kwargs
    ):
        super().__init__(
            column_identifier=ColumnIdentifier(column_identifier) if isinstance(column_identifier, str) else column_identifier,
            datatype=datatype,
            nullable=nullable,
            **kwargs,
        )

    @property
    def name(self) -> str:
        """Returns the column name."""
        return self.column_identifier.name

    @name.setter
    def name(self, n: str) -> None:
        self.column_identifier = ColumnIdentifier(n)

    def __repr__(self) -> str:
        return f"StructField({self.name!r}, {repr(self.datatype)}, nullable={self.nullable})"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __str__(self) -> str:
        return f"{self.name}: {repr(self.datatype)} (nullable = {self.nullable})"


class StructType(DataType):
    """Represents a table schema. Contains :class:`StructField` for each column."""

    type: Literal["StructType"] = Field("StructType", alias="@type")
    fields: List["StructField"] = Field([])

    def __init__(self, fields=None, **kwargs):
        if fields is None:
            fields = []
        super().__init__(fields=fields, **kwargs)

    @classmethod
    def _from_attributes(cls, attributes: list) -> "StructType":
        if attributes is None:
            return cls()
        return cls(fields=[StructField(a.name, a.datatype, a.nullable) for a in attributes])

    def __str__(self) -> str:
        return f"StructType([{', '.join(repr(f) for f in self.fields)}])"

    # def __getitem__(self, item: Union[str, int, slice]) -> StructField:
    #     """Access fields by name, index or slice."""
    #     if isinstance(item, str):
    #         for field in self.fields:
    #             if field.name == item:
    #                 return field
    #         raise KeyError(f"No StructField named {item}")
    #     elif isinstance(item, int):
    #         return self.fields[item]  # may throw ValueError
    #     elif isinstance(item, slice):
    #         return StructType(self.fields[item])
    #     else:
    #         raise TypeError(
    #             f"StructType items should be strings, integers or slices, but got {type(item).__name__}"
    #         )

    def __setitem__(self, key, value):
        raise TypeError("StructType object does not support item assignment")

    @property
    def names(self) -> List[str]:
        """Returns the list of names of the :class:`StructField`"""
        return [f.name for f in self.fields]

    def print_schema(self) -> str:
        return self._format_tree_string()

    def _format_tree_string(self) -> str:
        tree_string = "\nroot\n"
        prefix = " |-- "

        return f"{tree_string}" + "\n".join(prefix + str(field) for field in self.fields)

    printSchema = print_schema
