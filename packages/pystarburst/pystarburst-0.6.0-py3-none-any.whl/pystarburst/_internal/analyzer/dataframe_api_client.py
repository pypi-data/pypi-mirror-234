#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

import copy
import json
from typing import Union

from pydantic import Field
from trino.client import PROXIES, TrinoRequest, logger

from pystarburst._internal.analyzer.base_model import BaseModel
from pystarburst._internal.analyzer.plan.logical_plan import LogicalPlan
from pystarburst._internal.analyzer.plan.trino_plan import TrinoPlan
from pystarburst._internal.utils import PythonObjJSONEncoder
from pystarburst.exceptions import (
    PyStarburstColumnException,
    PyStarburstGeneralException,
    PyStarburstSQLException,
)


class ErrorResponse(BaseModel):
    message: str
    error_code: str = Field(alias="errorCode")


class Response(BaseModel):
    __root__: Union[TrinoPlan, ErrorResponse] = Field()


class DataFrameApiRequest(TrinoRequest):
    @property
    def statement_url(self) -> str:
        return self.get_url("/v1/dataframe/plan")

    def execute(self, payload):
        # Deep copy of the http_headers dict since they may be modified for this
        # request by the provided additional_http_headers
        http_headers = copy.deepcopy(self.http_headers)
        http_headers.update({"Content-Type": "application/json"})

        http_response = self._post(
            self.statement_url,
            data=json.dumps(payload, cls=PythonObjJSONEncoder),
            headers=http_headers,
            timeout=self._request_timeout,
            allow_redirects=self._redirect_handler is None,
            proxies=PROXIES,
        )
        if self._redirect_handler is not None:
            while http_response is not None and http_response.is_redirect:
                location = http_response.headers["Location"]
                url = self._redirect_handler.handle(location)
                logger.info("redirect %s from %s to %s", http_response.status_code, location, url)
                http_response = self._post(
                    url,
                    data=json.dumps(payload, cls=PythonObjJSONEncoder),
                    headers=http_headers,
                    timeout=self._request_timeout,
                    allow_redirects=False,
                    proxies=PROXIES,
                )
        return http_response


class DataFrameTableFunction:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, payload):
        payload_json = json.dumps(payload, cls=PythonObjJSONEncoder)
        try:
            self.cursor.execute(f"SELECT trino_plan FROM TABLE(analyze_logical_plan(?))", [payload_json])
        except Exception as e:
            raise PyStarburstSQLException(f"Failed to analyze logical plan: {str(e.message)}") from e
        rows = self.cursor.fetchall()
        return rows[0][0]


class DataframeApiClient:
    def __init__(self, session):
        self.session = session

    def analyze(self, logical_plan: LogicalPlan) -> TrinoPlan:
        conn = self.session._conn._conn
        cursor = self.session._conn._cursor
        if self.session.use_endpoint:
            trino_request = DataFrameApiRequest(
                conn.host,
                conn.port,
                conn._client_session,
                conn._http_session,
                conn.http_scheme,
                conn.auth,
                conn.redirect_handler,
                conn.max_attempts,
                conn.request_timeout,
            )
        else:
            trino_request = DataFrameTableFunction(cursor)
        payload = self.serialize(logical_plan)
        if self.session.use_endpoint:
            response = trino_request.execute(payload).json()
        else:
            response = json.loads(trino_request.execute(payload))
        return self.deserialize(response)

    def serialize(self, logical_plan):
        return logical_plan.dict(by_alias=True, exclude_none=True)

    def deserialize(self, json) -> TrinoPlan:
        response = Response.parse_obj(json).__root__

        if isinstance(response, ErrorResponse):
            message = response.message
            error_code = response.error_code
            if error_code == "SQL_ERROR":
                raise PyStarburstSQLException(message)
            if error_code == "COLUMN_ERROR":
                raise PyStarburstColumnException(message)
            raise PyStarburstGeneralException(message)

        assert isinstance(response, TrinoPlan)
        return response
