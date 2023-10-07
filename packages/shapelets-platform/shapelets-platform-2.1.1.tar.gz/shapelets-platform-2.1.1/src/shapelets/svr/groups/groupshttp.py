# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from blacksheep.server.controllers import ApiController, get, post
from requests import Session
from typing import List, Optional

from . import http_docs
from .igroupsservice import IGroupsService, InvalidGroupName

from ..docs import docs
from ..model import GroupProfile, GroupAttributes
from ..telemetry import ITelemetryService


class GroupsHttpServer(ApiController):
    def __init__(self, svr: IGroupsService, telemetry: ITelemetryService) -> None:
        self._svr = svr
        self._telemetry = telemetry
        super().__init__()

    @classmethod
    def route(cls) -> Optional[str]:
        return '/api/groups'

    @get("/")
    async def get_groups(self) -> List[GroupProfile]:
        try:
            return self.json(self._svr.get_all())
        except Exception as e:
            return self.status_code(500, str(e))

    @post("/")
    async def create(self, groupName: str, groupDescription: str) -> Optional[GroupProfile]:
        try:
            response = self.json(self._svr.create(GroupAttributes(name=groupName, description=groupDescription)))
            self._telemetry.send_telemetry(event="GroupCreated", info={"group_name": groupName})
            return response
        except Exception as e:
            return self.status_code(500, str(e))

    @get("/unp/all")
    async def get_all(self) -> List[GroupProfile]:
        try:
            return self.json(self._svr.get_all())
        except Exception as e:
            return self.status_code(500, str(e))

    @get("/unp/details")
    async def get_details(self, groupName: str) -> Optional[GroupProfile]:
        try:
            return self.json(self._svr.get_details(groupName))
        except Exception as e:
            return self.status_code(500, str(e))

    @get('/unp/check')  # description="Checks if the proposed group name already exists"
    @docs(http_docs.group_name_doc)
    async def group_name_exists(self, groupName: str) -> bool:
        try:
            return self.json(self._svr.group_name_exists(groupName))
        except Exception as e:
            return self.status_code(500, str(e))

    @get('/unp/remove')
    async def delete_group(self, groupName: str) -> str:
        try:
            response = self.json(self._svr.delete_group(groupName))
            self._telemetry.send_telemetry(event="GroupDelete", info={"group_name": groupName})
            return response
        except InvalidGroupName as e:
            return self.bad_request(str(e))
        except Exception as e:
            return self.status_code(500, str(e))

    @get('/unp/removeAll')
    async def delete_all(self):
        try:
            response = self.json(self._svr.delete_all())
            self._telemetry.send_telemetry(event="GroupDeleteAll")
            return response
        except Exception as e:
            return self.status_code(500, str(e))


class GroupsHttpProxy(IGroupsService):
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, group_name: str, group_description: str) -> Optional[GroupProfile]:
        response = self.session.post(
            '/api/groups/', params=[("groupName", group_name), ("groupDescription", group_description)])
        if response.status_code == 400 or response.status_code == 500:
            raise Exception(response.content)
        return response.json()

    def get_all(self) -> List[GroupProfile]:
        response = self.session.get('/api/groups/unp/all')
        return response.json()

    def get_details(self, group_name: str) -> Optional[GroupProfile]:
        response = self.session.get('/api/groups/unp/details', params=[("groupName", group_name)])
        if response.status_code == 400:
            raise InvalidGroupName(group_name)
        return response.ok and response.json()

    def group_name_exists(self, group_name: str) -> bool:
        response = self.session.get('/api/groups/unp/check', params=[("groupName", group_name)])
        if response.status_code == 400:
            raise InvalidGroupName(group_name)
        return response.ok and bool(response.json() == True)

    def delete_group(self, group_name: str) -> str:
        response = self.session.get('/api/groups/unp/remove', params=[("groupName", group_name)])
        if response.status_code == 400:
            raise InvalidGroupName(group_name)
        return response.json()  # response.ok and bool(response.json() == True)

    def delete_all(self) -> bool:
        response = self.session.get('/api/groups/unp/removeAll')
        return response.ok and bool(response.json() == True)

    def all_users_in_group(self, group_name: str):
        raise RuntimeError("TODO")

    def has_privileges(self, group_name: str) -> bool:
        return True
