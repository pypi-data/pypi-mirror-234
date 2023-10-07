# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import requests
import uuid

from pydantic import SecretStr
from typing import Dict, Optional, Union

from ..utils import crypto
from .iauthrepo import IAuthRepo
from .iauthservice import (
    Addresses,
    Challenge,
    IAuthService,
    InvalidLength,
    InvalidUserName,
    UnknownUser,
    UserAlreadyExists,
    VerificationError
)
from ..db import transaction
from ..model import GCPrincipalId, SignedPrincipalId, UserAttributes
from ..settings import Settings


class AuthService(IAuthService):
    __slots__ = ('_gc_url', '_gc_pk', '_auth_repo', '__pk', '__sk')

    def __init__(self, settings: Settings, auth_repo: IAuthRepo) -> None:
        self._gc_url = settings.grand_central
        self._gc_pk = settings.grand_central_pk
        self._auth_repo = auth_repo

        secret = settings.server.secret
        salt = settings.server.salt

        if secret is None:
            secret = crypto.generate_random_password()
        elif isinstance(secret, SecretStr):
            secret = secret.get_secret_value().encode('ascii')
        elif isinstance(secret, str):
            secret = secret.encode('ascii')
        else:
            raise ValueError(f'Sign secret is not valid.  {type(secret)}')

        if salt is None:
            salt = crypto.generate_salt()

        self.__pk, self.__sk = crypto.derive_signature_keys(salt, secret)

    def verify(self, principal: Union[SignedPrincipalId, str]) -> bool:
        checked = principal if isinstance(principal, SignedPrincipalId) else None

        if isinstance(principal, str):
            checked = SignedPrincipalId.from_token(principal)

        if checked is None:
            raise ValueError("Principal parameter should be a string token or a signed principal object")

        message = f'{checked.scope}:{checked.id}:{checked.userId}'.encode('ascii')
        if not crypto.verify(message, checked.signature, self.__pk):
            return False

        uid = self._auth_repo.find_userId(checked.scope, checked.id)
        if uid is None:
            return False

        return uid == checked.userId

    ###########################
    # External Authentication #
    ###########################

    def auth_token(self, principal: GCPrincipalId, user_details: Optional[UserAttributes] = None) -> SignedPrincipalId:
        msg = f'{principal.scope}:{principal.id}'.encode('ascii')
        if not crypto.verify(msg, principal.signature, self._gc_pk):
            raise VerificationError("Invalid principal")

        uid = self._auth_repo.find_userId(principal.scope, principal.id)
        if uid is None:
            if user_details is None:
                raise ValueError("Missing user details for new registration.")
            uid = self._auth_repo.create_new_user(principal.scope, principal.id, user_details)

        text = f'{principal.scope}:{principal.id}:{uid}'
        signature = crypto.sign(text.encode('ascii'), self.__sk)

        return SignedPrincipalId(
            scope=principal.scope,
            id=principal.id,
            userId=uid,
            signature=signature
        )

    def available(self, protocol: str) -> bool:
        if protocol == 'unp':
            return True
        else:
            query_address = f'https://{self._gc_url}/auth'
            response = requests.get(query_address, verify=False)
            if response.ok:
                response_json = response.json()
                return response_json[protocol] if protocol in response_json else False

        return False

    def providers(self) -> Dict[str, bool]:
        result = dict()
        result['unp'] = True

        query_address = f'https://{self._gc_url}/auth'
        response = requests.get(query_address, verify=False)
        if response.ok:
            result.update(response.json())

        return result

    def compute_addresses(self, protocol: str, req: Optional[str] = None) -> Optional[Addresses]:
        if protocol == 'unp' or not self.available(protocol):
            return None

        actual_req = req if req is not None else uuid.uuid4().hex
        return Addresses(
            ws=f'wss://{self._gc_url}/auth/ws/{actual_req}',
            redirect=f'https://{self._gc_url}/auth/{protocol}/{actual_req}'
        )

    ##########################
    # User Name and Password #
    ##########################

    def user_name_exists(self, userName: str) -> bool:
        return self._auth_repo.user_name_exists(userName)

    def remove_user(self, userName: str, transfer: str) -> int:
        return self._auth_repo.remove_user(userName, transfer)

    def register(self, userName: str, salt: bytes, verify_key: bytes, user_details: UserAttributes) -> int:

        if userName is None or len(userName) == 0:
            raise InvalidUserName(userName)

        if len(salt) != crypto.salt_bytes():
            raise InvalidLength('salt', crypto.salt_bytes(), len(salt))

        if len(verify_key) != crypto.verify_key_bytes():
            raise InvalidLength('verify_key', crypto.verify_key_bytes(), len(verify_key))

        with transaction():
            if self._auth_repo.user_name_exists(userName):
                raise UserAlreadyExists(userName)

            uid = self._auth_repo.create_new_user_unp(userName, salt, verify_key, user_details)
            return uid

    def generate_challenge(self, userName: str) -> Challenge:
        if userName is None or len(userName) == 0:
            raise InvalidUserName(userName)

        with transaction():
            if not self._auth_repo.user_name_exists(userName):
                raise UnknownUser(userName)

            salt = self._auth_repo.get_salt(userName)
            if salt is None:
                raise RuntimeError(f"Unable to retrieve salt associated with user {userName}")

            previous, _ = self._auth_repo.last_nonce(userName)
            nonce = crypto.generate_nonce(previous)
            self._auth_repo.store_nonce(userName, nonce)

            return Challenge(userName=userName, nonce=nonce, salt=salt)

    def verify_challenge(self, userName: str, nonce: Optional[bytes], token: bytes) -> SignedPrincipalId:

        if userName is None or len(userName) == 0:
            raise InvalidUserName(userName)

        with transaction():
            # get the nonce
            issued_nonce, already_verified = self._auth_repo.last_nonce(userName)
            # get the verify key from the repo
            verify_key = self._auth_repo.get_verify_key(userName)
            # and expire whatever is there, regardless
            self._auth_repo.expire_nonce(userName)

        # check it hasn't been used and the nonce is there
        if already_verified or issued_nonce is None:
            raise VerificationError(f"No challenge pending for user {userName}")

        # compare if given
        if nonce is not None:
            if not crypto.compare_buffers(nonce, issued_nonce):
                raise VerificationError("Nonces are different")

        if verify_key is None:
            raise RuntimeError(f"Unable to find verify key for user {userName}")

        if not crypto.verify_challenge(token, issued_nonce, verify_key):
            raise VerificationError(f"Unable to verify signature")

        uid = self._auth_repo.find_userId("unp", userName)
        if uid is None:
            raise VerificationError(f"No valid user found for credentials")

        message = f'unp:{userName}:{uid}'.encode('ascii')
        return SignedPrincipalId(
            scope='unp',
            id=userName,
            userId=uid,
            signature=crypto.sign(message, self.__sk)
        )

    def associate_unp(self, principal: SignedPrincipalId, new_user_name: str, new_salt: bytes, new_verify_key: bytes):
        if not self.verify(principal):
            raise VerificationError("Invalid principal")

        if len(new_salt) != crypto.salt_bytes():
            raise InvalidLength('salt', crypto.salt_bytes(), len(new_salt))

        if len(new_verify_key) != crypto.verify_key_bytes():
            raise InvalidLength('verify_key', crypto.verify_key_bytes(), len(new_verify_key))

        with transaction():
            existing_user_name = None
            if principal.scope != 'unp':
                if self._auth_repo.user_name_exists(new_user_name):
                    raise UserAlreadyExists(new_user_name)
                existing_user_name = self._auth_repo.find_user_name_with_principal(principal.scope, principal.id)
            else:
                existing_user_name = principal.id

            if existing_user_name is None:
                self._auth_repo.associate_unp(principal.userId, new_user_name, new_salt, new_verify_key)
            else:
                self._auth_repo.update_salt_and_key(existing_user_name, new_user_name, new_salt, new_verify_key)

    def associate(self, principal: SignedPrincipalId, new_principal: GCPrincipalId):
        if not self.verify(principal):
            raise VerificationError("Invalid principal")

        msg = f'{new_principal.scope}:{new_principal.id}'.encode('ascii')
        if not crypto.verify(msg, new_principal.signature, self._gc_pk):
            raise VerificationError("Invalid principal")

        self._auth_repo.associate(principal.userId, new_principal.scope, new_principal.id)

    def disassociate(self, principal: SignedPrincipalId, scope: str):
        if not self.verify(principal):
            raise VerificationError("Invalid principal")

        self._auth_repo.disassociate(principal.userId, scope)
