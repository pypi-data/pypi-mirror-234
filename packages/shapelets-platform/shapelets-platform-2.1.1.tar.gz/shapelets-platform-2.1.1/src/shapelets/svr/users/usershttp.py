# Copyright (c) 2022 Shapelets.io
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from blacksheep.server.controllers import ApiController, delete, get, post, put
from guardpost.asynchronous.authentication import Identity
from requests import Session
from typing import List, Optional, Union

from . import http_docs, IUsersService
from ..groups import InvalidGroupName
from ..docs import docs
from ..model import PrincipalId, ResolvedPrincipalId, UserAttributes, UserId, UserProfile


class UsersHttpServer(ApiController):
    def __init__(self, svr: IUsersService) -> None:
        self._svr = svr
        super().__init__()

    @classmethod
    def route(cls) -> Optional[str]:
        return '/api/users'

    @get("/")
    async def user_list(self) -> List[UserProfile]:
        return self.json(self._svr.get_all())

    @delete("/")
    async def delete_all_users(self) -> bool:
        return self._svr.delete_all()

    @post("/checkNickName")  # description="Checks if the proposed username already exists"
    @docs(http_docs.nickname_doc)
    async def check_nickname(self, nickName: str) -> bool:
        return self._svr.nickname_exists(nickName)

    @get("/me")
    @docs(http_docs.me_doc)
    async def my_details(self, identity: Optional[Identity]) -> UserProfile:
        if identity:
            return self._svr.get_user_details(identity.claims.get("userId"))
        return False

    @get("/{id}")
    async def get_user_details(self, id: int) -> Optional[UserProfile]:
        return self._svr.get_user_details(id)

    @put("/{id}")
    async def save_user_details(self, id: int, details: UserProfile) -> Optional[UserProfile]:
        self._svr.save_user_details(id, details)

    @delete("/{id}")
    async def delete_user(self, id: int):
        self._svr.delete(id)

    @get("/{id}/groups")
    async def get_user_groups(self, id: int):
        pass

    @put("/{userName}/groups")
    async def add_to_group(self, userName: str, groups: list, write: bool):
        try:
            if self.json(self._svr.add_to_group(userName, groups, write)):
                return self.ok(f"User {userName} added successfully to group/s {groups}")
            return self.bad_request()
        except InvalidGroupName as e:
            return self.bad_request(str(e))
        except Exception as e:
            return self.status_code(500, str(e))

    @delete("/{userName}/groups")
    async def remove_from_group(self, userName: str, groups: list):
        try:
            if self._svr.remove_from_group(userName, groups):
                return self.ok(f"User {userName} removed successfully from group/s {groups}")
            return self.bad_request()
        except InvalidGroupName as e:
            return self.bad_request(str(e))
        except Exception as e:
            return self.status_code(500, str(e))

    @get("/{id}/principals")
    async def get_user_principals(self, id: int) -> List[PrincipalId]:
        return self._svr.get_principals(id)


class UsersHttpProxy(IUsersService):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> List[UserProfile]:
        response = self.session.get('/api/users/')
        return response.json()

    def create(self, attributes: UserAttributes, principal: Optional[PrincipalId]) -> UserProfile:
        pass

    def delete_user(self, id: int):
        self.session.delete('/api/users/{id}', params=[("id", id)])

    def delete_all(self) -> bool:
        self.session.delete('/api/users/')
        return True

    def get_user_details(self, id: int) -> Optional[UserProfile]:
        return self.session.get('/api/users/{id}', params=[("id", id)])

    def save_user_details(self, id: int, details: UserProfile) -> Optional[UserProfile]:
        self.session.put('/api/users/{id}', params=[("id", id), ("details", details)])
        pass

    @docs(http_docs.nickname_doc)
    def nickname_exists(self, nickName: str) -> bool:
        return self.session.get('/api/users/checkNickName', params=[("nickName", nickName)])

    def get_principals(self, id: int) -> List[PrincipalId]:
        return self.session.get('/api/users/{id}/principals', params=[("id", id)])

    def dissociate_principal(self, principal: PrincipalId):
        pass

    def verify_principal(self, resolved_principal: ResolvedPrincipalId) -> bool:
        pass

    def resolve_principal(self, scope: str, pid: str) -> Optional[ResolvedPrincipalId]:
        pass

    def add_to_group(self, user_name: str, groups: Union[List[str], str], write: bool = False):
        response = self.session.put(f'/api/users/{user_name}/groups',
                                    params=[("userName", user_name), ("groups", groups), ("write", write)])
        if response.status_code != 200:
            raise Exception(response.content)
        print(response.content)

    def remove_from_group(self, user_name: str, groups: Union[List[str], str]):
        response = self.session.delete(f'/api/users/{user_name}/groups',
                                       params=[("userName", user_name), ("groups", groups)])
        if response.status_code != 200:
            raise Exception(response.content)
        print(response.content)

    def get_user_groups(self, id: int):
        response = self.session.get('/api/users/{id}/groups', params=[("id", id)])
        pass

    @docs(http_docs.me_doc)
    def my_details(self) -> UserProfile:
        response = self.session.get('/api/users/me')
        return UserProfile(uid=-1, nickName="pepe")
