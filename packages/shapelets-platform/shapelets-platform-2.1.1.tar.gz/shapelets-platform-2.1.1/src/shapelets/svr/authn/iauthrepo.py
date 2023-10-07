# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from abc import ABC, abstractmethod
from typing import Optional, Tuple

from ..model import UserAttributes


class IAuthRepo(ABC):

    @abstractmethod
    def find_userId(self, scope: str, id: str) -> Optional[int]:
        """
        Checks if a user is associated with a particular authentication 
        protocol and its correspondent unique id.
        """
        pass

    @abstractmethod
    def create_new_user_unp(self, userName: str, salt: bytes, verify_key: bytes, user_details: UserAttributes) -> int:
        pass

    @abstractmethod
    def create_new_user(self, scope: str, id: str, user_details: UserAttributes) -> int:
        """
        Creates a new user, associated with the given authentication protocol 
        and its correspondent unique id.
        """
        pass

    @abstractmethod
    def last_nonce(self, userName: str) -> Optional[Tuple[bytes, bool]]:
        pass

    @abstractmethod
    def user_name_exists(self, userName: str) -> bool:
        pass

    @abstractmethod
    def remove_user(self, userName: str, transfer: str) -> int:
        pass

    @abstractmethod
    def get_salt(self, userName: str) -> Optional[bytes]:
        pass

    @abstractmethod
    def store_nonce(self, userName: str, nonce: bytes):
        pass

    @abstractmethod
    def get_verify_key(self, userName: str) -> Optional[bytes]:
        pass

    @abstractmethod
    def expire_nonce(self, userName: str):
        pass

    @abstractmethod
    def update_salt_and_key(self, existing_user_name: str, new_user_name: str, new_salt: bytes, new_verify_key: bytes):
        pass

    @abstractmethod
    def find_user_name_with_principal(self, scope: str, id: str) -> Optional[str]:
        pass

    @abstractmethod
    def associate(self, userId: int, scope: str, id: str):
        pass

    @abstractmethod
    def associate_unp(self, userId: int, new_user_name: str, new_salt: bytes, new_verify_key: bytes):
        pass

    @abstractmethod
    def disassociate(self, userId: int, scope: str):
        pass
