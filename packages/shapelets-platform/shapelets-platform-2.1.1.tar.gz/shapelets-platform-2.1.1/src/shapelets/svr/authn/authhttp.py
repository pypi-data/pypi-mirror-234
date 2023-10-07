# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import json

from blacksheep import FromJSON, Response
from blacksheep.server.controllers import ApiController, get, post
from pydantic import BaseModel
from requests import Session
from typing import Dict, Optional, Union

from .iauthservice import (
    Addresses,
    Challenge,
    IAuthService,
    InvalidUserName,
    UnknownUser,
    VerificationError
)
from ..utils import FlexBytes
from ..model import UserAttributes, SignedPrincipalId, GCPrincipalId
from ..telemetry import ITelemetryService


class VerifyChallenge(BaseModel):
    userName: str
    nonce: Optional[FlexBytes]
    token: FlexBytes
    rememberMe: bool

    class Config:
        json_encoders = {
            FlexBytes: lambda v: str(v)
        }


class Registration(BaseModel):
    userName: str
    salt: FlexBytes
    pk: FlexBytes

    user_details: Optional[UserAttributes] = None

    class Config:
        json_encoders = {
            FlexBytes: lambda v: str(v)
        }


class GetTokenRequest(BaseModel):
    gc: GCPrincipalId
    user_details: Optional[UserAttributes]

    class Config:
        json_encoders = {
            FlexBytes: lambda v: str(v)
        }


class AuthHttpServer(ApiController):
    def __init__(self, svr: IAuthService, telemetry: ITelemetryService) -> None:
        self._svr = svr
        self._telemetry = telemetry
        super().__init__()

    @classmethod
    def route(cls) -> Optional[str]:
        return '/api/login'

    @get('/unp/check')
    async def check_user_exists(self, username: str) -> bool:
        try:
            return self.json(self._svr.user_name_exists(username))
        except InvalidUserName as e:
            return self.bad_request(str(e))
        except Exception as e:
            return self.status_code(500, str(e))

    @get('/unp/remove')
    async def remove_user(self, userName: str, transfer: str = None) -> bool:
        try:
            user_id = self._svr.remove_user(userName, transfer)
            if user_id:
                self._telemetry.send_telemetry(event="UserRemove", info={"user_id": user_id})
                return True
            return False
        except InvalidUserName as e:
            return self.bad_request(str(e))
        except Exception as e:
            return self.status_code(500, str(e))

    @get('/unp/challenge')
    async def generate_challenge(self, userName: str) -> Challenge:
        try:
            return self.json(json.loads(self._svr.generate_challenge(userName).json()))
        except InvalidUserName as e:
            return self.bad_request(str(e))
        except UnknownUser as e:
            return self.not_found(str(e))
        except Exception as e:
            return self.status_code(500, str(e))

    @post('/unp/authenticate')
    async def verify_challenge(self, details: FromJSON[VerifyChallenge]) -> Response:
        data = details.value
        try:
            principal = self._svr.verify_challenge(data.userName, data.nonce, data.token)
            return self.ok(principal.to_token())
        except InvalidUserName as e:
            return self.bad_request(str(e))
        except VerificationError as e:
            return self.unauthorized(str(e))
        except Exception as e:
            return self.status_code(500, str(e))

    @post('/unp/register')
    async def new_registration(self, details: FromJSON[Registration]) -> Response:
        data: Registration = details.value
        user_details = data.user_details or UserAttributes(nickName=data.userName)
        user_id = self._svr.register(data.userName, data.salt, data.pk, user_details)
        if user_id is not None:
            self._telemetry.send_telemetry(event="UserCreated", info={"user_id": user_id})
            return self.ok(user_id is not None)
        return self.not_found("Unable to create user")

    @get('/available/{protocol}')
    async def available(self, protocol: str):
        return self.ok(self._svr.available(protocol))

    @get('/available')
    async def providers(self):
        return self.ok(self._svr.providers())

    @get('/addresses')
    async def addresses(self, protocol: str, req: Optional[str] = None):
        return self._svr.compute_addresses(protocol, req)

    @get('/verify')
    async def verify(self, token: str):
        return self.ok(self._svr.verify(token))

    @post('/token')
    async def get_token(self, details: FromJSON[GetTokenRequest]):
        principal = self._svr.auth_token(details.value.gc, details.value.user_details)
        return self.ok(principal.to_token())


class AuthHttpProxy(IAuthService):
    def __init__(self, session: Session) -> None:
        self.session = session

    def user_name_exists(self, userName: str) -> bool:
        response = self.session.get('/api/login/unp/check', params=[("username", userName)])

        if response.status_code == 400:
            raise InvalidUserName(userName)

        return response.ok and bool(response.json() == True)

    def remove_user(self, userName: str, transfer: str = None) -> int:
        response = self.session.get('/api/login/unp/remove', params=[("userName", userName), ("transfer", transfer)])
        if response.status_code != 200:
            raise Exception(response.content)

        return response.ok and bool(response.json() == True)

    def generate_challenge(self, userName: str) -> Challenge:
        response = self.session.get('/api/login/unp/challenge', params=[("userName", userName)])
        if response.status_code == 400:
            raise InvalidUserName(userName)
        elif response.status_code == 404:
            raise UnknownUser(userName)
        elif response.status_code != 200:
            raise RuntimeError(response.text)

        return Challenge.parse_obj(response.json())

    def verify_challenge(self, userName: str, nonce: Optional[bytes], token: bytes) -> SignedPrincipalId:
        payload = VerifyChallenge(userName=userName,
                                  nonce=nonce,
                                  token=token,
                                  rememberMe=False)

        response = self.session.post('/api/login/unp/authenticate', json=json.loads(payload.json()))
        if response.status_code == 400:
            raise InvalidUserName(userName)
        elif response.status_code == 401:
            raise VerificationError(response.text)
        elif response.status_code != 200:
            raise RuntimeError(response.text)

        token = response.text
        principal = SignedPrincipalId.from_token(token)
        if principal is None:
            raise RuntimeError(f"Unable to decode token [{token}]")

        return principal

    def register(self, userName: str, salt: bytes, verify_key: bytes, user_details: UserAttributes) -> Response:
        payload = Registration(userName=userName, salt=salt, pk=verify_key, user_details=user_details)
        response = self.session.post('/api/login/unp/register', json=json.loads(payload.json()))
        return response

    def available(self, protocol: str) -> bool:
        response = self.session.get(f'/api/login/available/{protocol}')
        return response.ok and bool(response.json() == True)

    def providers(self) -> Dict[str, bool]:
        response = self.session.get('/api/login/available')
        response.raise_for_status()
        return response.json()

    def compute_addresses(self, protocol: str, req: Optional[str] = None) -> Optional[Addresses]:
        params = [('protocol', protocol)]
        if req is not None:
            params.append(('req', req))

        response = self.session.get('/api/login/addresses', params=params)
        response.raise_for_status()
        data = response.json()
        if len(data) == 0:
            return None
        return Addresses.parse_obj(data)

    def verify(self, principal: Union[SignedPrincipalId, str]) -> bool:
        token = principal.to_token() if isinstance(principal, SignedPrincipalId) else str(principal)
        response = self.session.get('/api/login/verify', params=[('token', token)])
        return response.ok and bool(response.json() == True)

    def auth_token(self, principal: GCPrincipalId, user_details: Optional[UserAttributes] = None) -> SignedPrincipalId:
        token_request = GetTokenRequest(gc=principal, user_details=user_details)
        response = self.session.post('/api/login/token', json=json.loads(token_request.json()))
        response.raise_for_status()
        return SignedPrincipalId.from_token(response.text)

    def associate_unp(self, principal: SignedPrincipalId, new_user_name: str, new_salt: bytes, new_verify_key: bytes):
        """
        Associates (or updates) a user-name/password combination to the current logged user.
        """
        raise RuntimeError("TODO")

    def associate(self, principal: SignedPrincipalId, new_principal: GCPrincipalId):
        """
        Associate an external credential to the current logged user
        """
        raise RuntimeError("TODO")

    def disassociate(self, principal: SignedPrincipalId, scope: str):
        """
        Disassociates a particular authentication protocol 
        """
        raise RuntimeError("TODO")
