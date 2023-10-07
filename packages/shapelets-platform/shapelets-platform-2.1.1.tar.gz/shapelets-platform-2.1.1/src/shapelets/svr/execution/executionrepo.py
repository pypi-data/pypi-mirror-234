# Copyright (c) 2022 Shapelets.io
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import List

from .iexecutionrepo import IExecutionRepo
from ..db import Connection, transaction


def _execute_function(fn):
    pass


def _add_files(current_fn_id: str, new_ids: List[str], conn: Connection):
    """
    When a function is executed it could create new files. For example, an arrow file with a table information.
    This function makes sure that we associate the new saved files with the dataApp so in the future, when the dataApp
    is deleted, we can also remove its associated files.
    param current_fn_id: current id of the functon being executed. This id is used to get the dataApp ID associated
                        with that function.
    param new_ids: new ids to link.
    """
    conn.execute("SELECT dataappId FROM dataapp_data WHERE dataInfo = ?;", [current_fn_id])
    dataapp_id = conn.fetch_one()[0]
    if dataapp_id is not None:
        for id in new_ids:
            conn.execute("""
                            INSERT INTO dataapp_data 
                            (dataappId, dataInfo)
                            VALUES (?, ?);
                        """, [dataapp_id, id])


class ExecutionRepo(IExecutionRepo):

    def execute_function(self, fn: str):
        _execute_function(fn)

    def add_files(self, current_fn_id: str, new_ids: List[str]):
        with transaction() as conn:
            _add_files(current_fn_id, new_ids, conn)
