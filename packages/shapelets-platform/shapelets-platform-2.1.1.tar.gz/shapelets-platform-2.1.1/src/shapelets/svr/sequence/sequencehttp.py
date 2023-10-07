import asyncio
import json

from blacksheep import Request, FromJSON, Response
from blacksheep.server.controllers import ApiController, get, post
from requests import Session, ReadTimeout
from typing import Any, Optional

from .isequenceservice import ISequenceService
from ..model.sequence import SequenceProfile, VisualizationInfo


class SequenceHttpServer(ApiController):
    def __init__(self, svr: ISequenceService) -> None:
        self._svr = svr
        super().__init__()

    @classmethod
    def route(cls) -> Optional[str]:
        return '/api/sequences'

    @post("/create")
    async def create_sequence(self, seq: FromJSON[SequenceProfile]) -> Response:
        try:
            self._svr.create_sequence(seq.value)
            return self.ok()
        except Exception as e:
            return self.status_code(500, str(e))

    @get("/{seqId}")
    async def get_sequence(self, request: Request) -> SequenceProfile:
        seq_id = request.route_values['seqId']
        seq = self._svr.get_sequence(seq_id)
        return seq

    @get("{id}/levelsblocks")
    async def get_levels_blocks(self, request: Request) -> VisualizationInfo:
        seq_id = request.route_values['id']
        levels = self._svr.get_levels_blocks(seq_id)
        return levels

    @get("{id}/visualization")
    async def get_visualization(self, request: Request) -> str:
        seq_id = request.route_values['id']
        level_blocks = json.loads(request.query['levelBlocks'][0])
        visualization = self._svr.get_visualization(seq_id, level_blocks)
        if visualization is not None:
            return visualization
        return []

    @post("/generateLevels")
    async def generate_levels(self, sequence_id: str):
        try:
            asyncio.create_task(self._svr.generate_levels(sequence_id))
            return self.ok()
        except Exception as e:
            print(e)
            return self.status_code(500, str(e))


class SequenceHttpProxy(ISequenceService):
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_sequence(self, sequence: SequenceProfile):
        response = self.session.post('/api/sequences/create', json=json.loads(sequence.json()))
        if response.status_code != 200:
            raise RuntimeError(response.content)
        return response

    def get_sequence(self, table_id: str, from_row: int, n: int):
        params = [("table_id", table_id), ("from_row", from_row), ("n", n)]
        return self.session.get('/api/executions/tableData/', params=params)

    def get_levels_blocks(self, request: Request) -> Any:
        pass

    def get_visualization(self, request: Request):
        pass

    def generate_levels(self, sequence_id: str):
        """
        Send request with low timeout as we don't expect a response, and we want to continue our work after sending this request.
        """
        return self.session.post('/api/sequences/generateLevels', params=[("sequence_id", sequence_id)])


