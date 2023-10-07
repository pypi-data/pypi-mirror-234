#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

import pystarburst
from pystarburst._internal.analyzer.dataframe_api_client import DataframeApiClient
from pystarburst._internal.analyzer.plan.logical_plan import LogicalPlan
from pystarburst._internal.analyzer.plan.trino_plan import TrinoPlan


class Analyzer:
    def __init__(self, session: "pystarburst.session.Session") -> None:
        self.dataframe_api_client = DataframeApiClient(session)

    def resolve(self, logical_plan: LogicalPlan) -> TrinoPlan:
        return self.dataframe_api_client.analyze(logical_plan)
