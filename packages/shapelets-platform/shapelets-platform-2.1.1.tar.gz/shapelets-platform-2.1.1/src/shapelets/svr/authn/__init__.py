# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from rodi import Container

from .authhttp import AuthHttpProxy, AuthHttpServer
from .authrepo import AuthRepo
from .authservice import AuthService
from .gc_client import gc_flow, AuthenticationError
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


def setup_remote_client(container: Container):
    container.add_singleton(IAuthService, AuthHttpProxy)


def setup_services(container: Container):
    container.add_singleton(IAuthRepo, AuthRepo)
    container.add_singleton(IAuthService, AuthService)


__all__ = [
    'setup_remote_client', 'setup_services',
    'IAuthRepo', 'IAuthService',
    'UserAlreadyExists', 'InvalidLength', 'VerificationError',
    'UnknownUser', 'InvalidUserName', 'Challenge', 'Addresses',
    'AuthHttpServer', 'gc_flow', 'AuthenticationError'
]

# class UnPApi:

#     def __init__(self, unpSvc: IUnPService, cfg: Settings) -> None:
#         self.__unp = unpSvc
#         self.__cfg = cfg

#     def __contains__(self, userName: str) -> bool:
#         return self.user_exists(userName)

#     def user_exists(self, userName: str) -> bool:
#         return self.__unp.user_exists(userName)

#     def register(self, userName: str, password: str, profile: Optional[Any] = None):
#         if self.unp.user_exists(userName):
#             raise ValueError(f"{userName} already registered in the system")

#         salt = crypto.generate_salt()
#         pk = crypto.derive_verify_key(salt, password.encode('utf-8'))

#         self.unp.register(userName, salt, pk)

#     def login(self, userName: Optional[str] = None, password: Optional[str] = None) -> SignedPrincipalId:
#         usr = userName or self.__cfg.client.username
#         pwd = password or self.__cfg.client.password

#         if usr is None:
#             raise ValueError("User name is required")

#         if pwd is None:
#             raise ValueError("Password is required")

#         if isinstance(pwd, SecretStr):
#             pwd = pwd.get_secret_value()

#         challenge = self.__unp.generate_challenge(usr)
#         token = crypto.sign_challenge(challenge.salt, challenge.nonce, pwd.encode('utf-8'))
#         return self.__unp.verify_challenge(usr, challenge.nonce, token)
