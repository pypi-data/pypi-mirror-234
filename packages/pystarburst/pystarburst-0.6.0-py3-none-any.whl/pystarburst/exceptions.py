#
# Copyright (c) 2012-2022 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

"""This package contains all pystarburst client-side exceptions."""
import logging
from typing import Optional

_logger = logging.getLogger(__name__)


class PyStarburstClientException(Exception):
    """Base pystarburst exception class"""

    def __init__(
        self,
        message: str,
    ) -> None:
        self.message: str = message

    def __repr__(self):
        return f"{self.__class__.__name__}({self.message!r})"

    def __str__(self):
        return self.message


class PyStarburstDataframeException(PyStarburstClientException):
    """Exception for dataframe related errors."""

    pass


class PyStarburstPlanException(PyStarburstClientException):
    """Exception for plan analysis errors."""

    pass


class PyStarburstSQLException(PyStarburstClientException):
    """Exception for errors related to the executed SQL statement that was generated
    from the Trino plan.
    """

    def __init__(
        self,
        message: str,
        query_id: Optional[str] = None,
    ) -> None:
        self.message: str = message
        self.query_id: str = query_id

    def __repr__(self):
        return f"{self.__class__.__name__}({self.message!r}, {self.query_id!r})"


class PyStarburstServerException(PyStarburstClientException):
    """Exception for miscellaneous related errors."""

    pass


class PyStarburstGeneralException(PyStarburstClientException):
    """Exception for general exceptions."""

    pass


class PyStarburstColumnException(PyStarburstDataframeException):
    """Exception for column related errors during dataframe operations."""

    pass


class PyStarburstJoinException(PyStarburstDataframeException):
    """Exception for join related errors during dataframe operations."""

    pass


class PyStarburstTableException(PyStarburstDataframeException):
    """Exception for table related errors."""

    pass


class PyStarburstSessionException(PyStarburstServerException):
    """Exception for any session related errors."""

    pass


class PyStarburstMissingDbOrSchemaException(PyStarburstServerException):
    """Exception for when a schema or database is missing in the session connection.
    These are needed to run queries.
    """

    pass


class PyStarburstFetchDataException(PyStarburstServerException):
    """Exception for when we are trying to fetch data from Trino."""

    pass


class PyStarburstInvalidObjectNameException(PyStarburstGeneralException):
    """Exception for inputting an invalid object name. Checked locally."""

    pass
