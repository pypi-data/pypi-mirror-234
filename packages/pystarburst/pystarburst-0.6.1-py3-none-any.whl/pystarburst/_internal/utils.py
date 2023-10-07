#
# Copyright (c) 2012-2022 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

import array
import binascii
import datetime
import decimal
import importlib
import importlib.metadata
import logging
import platform
import random
import re
import string
import sys
import traceback
import uuid
from enum import Enum
from json import JSONEncoder
from random import choice
from typing import Any, Iterator, List, NamedTuple, Optional, Tuple, Type

from dateutil.relativedelta import relativedelta

try:
    from zoneinfo import ZoneInfo
except ModuleNotFoundError:
    from backports.zoneinfo import ZoneInfo

from trino import __version__ as connector_version
from trino.dbapi import Cursor

import pystarburst
from pystarburst._internal.error_message import PyStarburstClientExceptionMessages
from pystarburst.row import Row

PYTHON_VERSION = ".".join(str(v) for v in sys.version_info[:3])
OPERATING_SYSTEM = platform.system()
PLATFORM = platform.platform()

TRINO_UNQUOTED_ID_PATTERN = r"(?:[a-zA-Z_][\w\$]{0,255})"
TRINO_QUOTED_ID_PATTERN = '(?:"(?:[^"]|""){1,255}")'
TRINO_ID_PATTERN = f"({TRINO_UNQUOTED_ID_PATTERN}|{TRINO_QUOTED_ID_PATTERN})"
TRINO_CASE_INSENSITIVE_QUOTED_ID_PATTERN = r'("([a-z_][a-z0-9_\$]{0,255})")'
TRINO_CASE_INSENSITIVE_UNQUOTED_SUFFIX_PATTERN = r"([a-zA-Z0-9_\$]{0,255})"

# Valid name can be:
#   identifier
#   identifier.identifier
#   identifier.identifier.identifier
TRINO_OBJECT_RE_PATTERN = re.compile(f"^(?:(?:{TRINO_ID_PATTERN}\\.){{0,2}}){TRINO_ID_PATTERN}$")

TRINO_CATALOG_SCHEMA_PATTERN = re.compile(f"^(?:(?:{TRINO_ID_PATTERN}\\.){{0,1}}){TRINO_ID_PATTERN}$")

TRINO_IDENTIFIER_PATTERN = re.compile(TRINO_ID_PATTERN)

TRINO_ALIASED_PATTERN = re.compile(f".+\\s+(?:AS\\s+)?{TRINO_ID_PATTERN}")

TRINO_CASE_INSENSITIVE_QUOTED_ID_RE_PATTERN = re.compile(TRINO_CASE_INSENSITIVE_QUOTED_ID_PATTERN)
TRINO_CASE_INSENSITIVE_UNQUOTED_SUFFIX_RE_PATTERN = re.compile(TRINO_CASE_INSENSITIVE_UNQUOTED_SUFFIX_PATTERN)

# Prefix for allowed temp object names in stored proc
TEMP_OBJECT_NAME_PREFIX = "TRINO_TEMP_"
ALPHANUMERIC = string.digits + string.ascii_lowercase

TRINO_SELECT_SQL_PREFIX_PATTERN = re.compile(r"^(\s|\()*(select|with)", re.IGNORECASE)


class TempObjectType(Enum):
    TABLE = "TABLE"
    VIEW = "VIEW"
    FUNCTION = "FUNCTION"
    COLUMN = "COLUMN"
    PROCEDURE = "PROCEDURE"
    TABLE_FUNCTION = "TABLE_FUNCTION"


def validate_identifier_name(name: str):
    if not TRINO_IDENTIFIER_PATTERN.match(name):
        raise PyStarburstClientExceptionMessages.GENERAL_INVALID_OBJECT_NAME(name)


def validate_object_name(name: str):
    if not TRINO_OBJECT_RE_PATTERN.match(name):
        raise PyStarburstClientExceptionMessages.GENERAL_INVALID_OBJECT_NAME(name)


def validate_catalog_schema_name(name: str):
    if not TRINO_CATALOG_SCHEMA_PATTERN.match(name):
        raise PyStarburstClientExceptionMessages.GENERAL_INVALID_OBJECT_NAME(name)


def get_version() -> str:
    return importlib.metadata.metadata("pystarburst")["version"]


def get_python_version() -> str:
    return platform.python_version()


def get_connector_version() -> str:
    return connector_version


def get_os_name() -> str:
    return platform.system()


def is_pandas_installed() -> bool:
    try:
        importlib.import_module("pandas")
        from pandas import DataFrame  # NOQA

        return True
    except ImportError:
        return False


def get_application_name() -> str:
    return "pystarburst"


def is_single_quoted(name: str) -> bool:
    return name.startswith("'") and name.endswith("'")


def is_trino_quoted_id_case_insensitive(name: str) -> bool:
    return TRINO_CASE_INSENSITIVE_QUOTED_ID_RE_PATTERN.fullmatch(name) is not None


def is_aliased(column_expression: str) -> bool:
    return TRINO_ALIASED_PATTERN.fullmatch(column_expression) is not None


def is_trino_unquoted_suffix_case_insensitive(name: str) -> bool:
    return TRINO_CASE_INSENSITIVE_UNQUOTED_SUFFIX_RE_PATTERN.fullmatch(name) is not None


def unwrap_single_quote(name: str) -> str:
    new_name = name.strip()
    if is_single_quoted(new_name):
        new_name = new_name[1:-1]
    new_name = new_name.replace("\\'", "'")
    return new_name


def is_sql_select_statement(sql: str) -> bool:
    return TRINO_SELECT_SQL_PREFIX_PATTERN.match(sql) is not None


def random_number() -> int:
    """Get a random unsigned integer."""
    return random.randint(0, 2**31)


def random_string() -> str:
    return uuid.uuid4().hex


def parse_positional_args_to_list(*inputs: Any) -> List:
    """Convert the positional arguments to a list."""
    if len(inputs) == 1:
        return [*inputs[0]] if isinstance(inputs[0], (list, tuple, set)) else [inputs[0]]
    else:
        return [*inputs]


def str_to_enum(value: str, enum_class: Type[Enum], except_str: str) -> Enum:
    try:
        return enum_class(value.upper())
    except ValueError:
        raise ValueError(f"{except_str} must be one of {', '.join([e.value.lower() for e in enum_class])}")


def create_statement_query_tag(skip_levels: int = 0) -> str:
    stack = traceback.format_stack(limit=skip_levels)
    return "".join(stack[:-skip_levels] if skip_levels else stack)


def random_name_for_temp_object(object_type: TempObjectType) -> str:
    return f"{TEMP_OBJECT_NAME_PREFIX}{object_type.value}_{generate_random_alphanumeric()}".lower()


def generate_random_alphanumeric(length: int = 10) -> str:
    return "".join(choice(ALPHANUMERIC) for _ in range(length))


def column_to_bool(col_):
    """A replacement to bool(col_) to check if ``col_`` is None or Empty.

    ``Column.__bool__` raises an exception to remind users to use &, |, ~ instead of and, or, not for logical operations.
    The side-effect is the implicit call like ``if col_`` also raises an exception.
    Our internal code sometimes needs to check an input column is None, "", or []. So this method will help it by writeint ``if column_to_bool(col_): ...``
    """
    if isinstance(col_, pystarburst.Column):
        return True
    return bool(col_)


def result_set_to_rows(result_set: List[Any], result_meta: Optional[List[Any]] = None) -> List[Row]:
    col_names = [col.name for col in result_meta] if result_meta else None
    rows = []
    for data in result_set:
        if data is None:
            raise ValueError("Result returned from Trino Python Client is None")
        row = Row(*data)
        # row might have duplicated column names
        if col_names:
            row._fields = col_names
        rows.append(row)
    return rows


def result_set_to_iter(result_set: Cursor, result_meta: Optional[List[Any]] = None) -> Iterator[Row]:
    col_names = [col.name for col in result_meta] if result_meta else None
    for data in result_set.gi_frame.f_locals["self"].rows:
        if data is None:
            raise ValueError("Result returned from Python connector is None")
        row = Row(*data)
        if col_names:
            row._fields = col_names
        yield row


class PythonObjJSONEncoder(JSONEncoder):
    """Converts common Python objects to json serializable objects."""

    def default(self, value):
        if isinstance(value, relativedelta):
            if value.years == 0 and value.months == 0:
                raise TypeError("Unsupported conversion, specify years or months in relativedelta")
            # TODO: we should throw an exception here in case we receive values that contain any other units (seconds, ...)
            return f"{value.years}-{value.months}"
        if isinstance(value, datetime.timedelta):
            return f"{value.days} 00:00:{(value.seconds+value.microseconds/1000000):.3f}"
        if isinstance(value, (bytes, bytearray)):
            return binascii.hexlify(value).decode("utf-8")
        if isinstance(value, uuid.UUID):
            return str(value)
        elif isinstance(value, decimal.Decimal):
            return format(value, "f")
        elif isinstance(value, datetime.datetime) and value.tzinfo is None:
            # TODO: figure out why we can't use value.strftime("%Y-%m-%d %H:%M:%S.%f")
            return f"{value.year:04}-{value.month:02}-{value.day:02} {value.hour:02}:{value.minute:02}:{value.second:02}.{value.microsecond:06}"
        if isinstance(value, datetime.datetime) and value.tzinfo is not None:
            # TODO: figure out why we can't use value.strftime("%Y-%m-%d %H:%M:%S.%f")
            datetime_str = f"{value.year:04}-{value.month:02}-{value.day:02} {value.hour:02}:{value.minute:02}:{value.second:02}.{value.microsecond:06}"
            # named timezones
            if isinstance(value.tzinfo, ZoneInfo):
                return f"{datetime_str} {value.tzinfo.key}"
            if hasattr(value.tzinfo, "zone"):
                return f"{datetime_str} {value.tzinfo.zone}"
            # offset-based timezones
            return f"{datetime_str} {value.tzinfo.tzname(value)}"
        if isinstance(value, datetime.time) and value.tzinfo is None:
            return value.strftime("%H:%M:%S.%f")
        if isinstance(value, datetime.time) and value.tzinfo is not None:
            time_str = value.strftime("%H:%M:%S.%f")
            # named timezones
            if isinstance(value.tzinfo, ZoneInfo):
                utc_offset = datetime.datetime.now(tz=value.tzinfo).strftime("%z")
                return f"{time_str}{utc_offset[:3]}:{utc_offset[3:]}"
            # offset-based timezones
            timezone = value.strftime("%z")
            return f"{time_str}{timezone[:3]}:{timezone[3:]}"
        if isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, array.array):
            return value.tolist()
        else:
            return super().default(value)


logger = logging.getLogger("pystarburst")


class ResultMetadata(NamedTuple):
    name: str
    type_code: int
    display_size: int
    internal_size: int
    precision: int
    scale: int
    is_nullable: bool


def convert_result_meta_to_named_tuple(description: List[Tuple[Any]]) -> List[ResultMetadata]:
    if description is None:
        return []
    return [ResultMetadata(*row) for row in description]
