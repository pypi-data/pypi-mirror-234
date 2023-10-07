# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
from blacksheep import Request, FromJSON
from blacksheep.server.controllers import ApiController, get, post, delete, ws
from requests import Session
from typing import Any, List, Optional

from .iexecutionservice import IExecutionService
from ..docs import docs
from ..model.function import FunctionProfile


# from ...apps.widgets import Widget


class ExecutionHttpServer(ApiController):
    def __init__(self, svr: IExecutionService) -> None:
        self._svr = svr
        super().__init__()

    @classmethod
    def route(cls) -> Optional[str]:
        return '/api/executions'

    @post("/runFn")
    async def run_execution(self, fn: FromJSON[FunctionProfile]) -> Any:
        function = FunctionProfile(body=fn.value.body,
                                   parameters=fn.value.parameters,
                                   result=fn.value.result)
        result = self._svr.execute_function(function)
        return result.to_dict_widget()

    @get("/tableData")
    async def table_data(self, table: str, fromRow: int, n: int) -> Any:
        return self._svr.table_data(table, fromRow, n)


class ExecutionHttpProxy(IExecutionService):
    def __init__(self, session: Session) -> None:
        self.session = session

    def execute_function(self, fn: FunctionProfile):
        return self.session.post('/api/executions/runFn/', params=[("fn", fn)])

    def table_data(self, table_id: str, from_row: int, n: int):
        params = [("table_id", table_id), ("from_row", from_row), ("n", n)]
        return self.session.get('/api/executions/tableData/', params=params)
