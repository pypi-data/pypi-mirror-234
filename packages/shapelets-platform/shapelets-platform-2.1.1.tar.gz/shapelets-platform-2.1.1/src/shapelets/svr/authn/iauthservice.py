# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from abc import ABC, abstractmethod
from pydantic import AnyUrl, BaseModel
from typing import Dict, Optional, Union

from ..model import UserAttributes, SignedPrincipalId, GCPrincipalId
from ..utils import FlexBytes


class Addresses(BaseModel):
    ws: AnyUrl
    redirect: AnyUrl


class Challenge(BaseModel):
    userName: str
    nonce: FlexBytes
    salt: FlexBytes

    class Config:
        json_encoders = {
            FlexBytes: lambda v: list(v)
        }


class InvalidUserName(Exception):
    def __init__(self, userName: str, *args: object) -> None:
        self._userName = userName
        super().__init__(*args)

    def __str__(self) -> str:
        return f"Invalid user name {self._userName}"


class UnknownUser(Exception):
    def __init__(self, userName: str, *args: object) -> None:
        self._userName = userName
        super().__init__(*args)

    def __str__(self) -> str:
        return f"Unknown user name {self._userName}"


class VerificationError(Exception):
    def __init__(self, msg: str, *args: object) -> None:
        self._msg = msg
        super().__init__(*args)

    def __str__(self) -> str:
        return f'Verification error: {self._msg}'


class InvalidLength(Exception):
    def __init__(self, field: str, req_length: int, provided: int, *args: object) -> None:
        self._req_length = req_length
        self._provided = provided
        self._field = field
        super().__init__(*args)

    def __str__(self) -> str:
        return f"[{self._field}]: Required length is {self._req_length}; provided {self._provided}"


class UserAlreadyExists(Exception):
    def __init__(self, userName: str, *args: object) -> None:
        self._userName = userName
        super().__init__(*args)

    def __str__(self) -> str:
        return f"User {self._userName} already exists"


class IAuthService(ABC):
    @abstractmethod
    def verify(self, principal: Union[SignedPrincipalId, str]) -> bool:
        """
        Verifies an authentication token signed by this server

        Parameters
        ----------
        principal: either a string token or a SignedPrincipalId instance
            Credentials to verify.

        Returns
        -------
        A boolean flag; when True, the credentials are valid.  False otherwise.        
        """
        pass

    @abstractmethod
    def auth_token(self, principal: GCPrincipalId, user_details: Optional[UserAttributes] = None) -> SignedPrincipalId:
        """
        Returns an authentication token after verifying an identity obtained 
        through an external authn provider

        Parameters
        ----------
        principal: GCPrincipalId, required
            Principal received after completing an external authentication process 

        user_details: UserAttributes, optional, defaults to None 
            User details to be used when the user is new

        Returns
        -------
        SignedPrincipalId, an instance of a principal that can be used to interact 
            with Shapelets.
        """
        pass

    @abstractmethod
    def available(self, protocol: str) -> bool:
        """
        Checks if a particular external authentication protocol is available

        See Also
        --------
        providers, which returns list of valid authentication protocols.
        """
        pass

    @abstractmethod
    def providers(self) -> Dict[str, bool]:
        """
        Returns a list of valid authentication protocols, including unp
        """
        pass

    @abstractmethod
    def compute_addresses(self, protocol: str, req: Optional[str] = None) -> Optional[Addresses]:
        """
        Returns a pair of addresses, one for a web socket where authentication 
        results are sent, and another, for the web browser redirection to 
        initiate the authentication process.

        Parameters
        ----------
        protocol: str, required
            The desired protocol.  'unp' is not a valid parameter.
        req: str, optional
            The unique id for the interaction.  If none, a random uuid will be used 
            to correlate web socket with user browser activity.

        Returns
        -------
        Address: This method returns None if the protocol is unp or the protocol is 
                 not recognised.  Otherwise, it returns the web socket and redirection 
                 address.
        """
        pass

    @abstractmethod
    def user_name_exists(self, userName: str) -> bool:
        """
        Checks for the uniqueness of a user name (for username and password)
        """
        pass

    @abstractmethod
    def remove_user(self, userName: str, transfer: str) -> int:
        """
        Remove the user indicated by user name
        """
        pass

    @abstractmethod
    def register(self, userName: str, salt: bytes, verify_key: bytes, user_details: UserAttributes) -> int:
        """
        Registers credentials for a new user based on user name and password 

        Parameters
        ----------
        userName: str, required
            User name.  If the user name is not unique in the system, it will 
            throw UserAlreadyExists

        salt: bytes, required
            Bytes used during the key derivation process.

        verify_key: bytes, required
            Public key to verify client generated signatures.

        user_details: UserAttributes, required
            Initial user profile.

        Returns
        -------
        bool, True if the registration was successful. False if the transaction couldn't 
            be completed.

        Exceptions
        ----------
        InvalidUserName: 
            The userName parameter is either None or a string of length zero.        
        InvalidLength: 
            Raised if either the salt or the verify key do not conform with 
            the expected length requirements
        UserAlreadyExists:
            Raised if the user has already registered.
        """
        pass

    @abstractmethod
    def generate_challenge(self, userName: str) -> Challenge:
        """
        Generates a log in challenge for a registered user

        Parameters
        ----------
        userName: str
            Registered user name 

        Returns
        -------
        Challenge: 
            Returns a message with the original salt used during the registration 
            process and a nonce, which the user need to sign with his private 
            signature key derived from the salt and his password.

        Exceptions
        ----------
        InvalidUserName: 
            The userName parameter is either None or a string of length zero.        
        UnknownUser:
            If the user is not present in the system
        RuntimeError:
            Raised when an inconsistent entry in the database is found.

        """
        pass

    @abstractmethod
    def verify_challenge(self, userName: str, nonce: Optional[bytes], token: bytes) -> SignedPrincipalId:
        """
        Completes the authentication process by checking the signature over a nonce  
        is verifiable using the stored public signature associated with a user 
        during the registration process.

        Parameters
        ----------
        userName: str 
            Registered user name 
        token: bytes
            Signature over nonce, using the private signature key generated from the 
            salt and user password
        nonce: bytes, optional
            Original nonce generated by the challenge. If provided, it will be matched against 
            the stored nonce.

        Returns
        -------
        SignedPrincipalId, an instance of a principal that can be used to interact 
            with Shapelets.

        Exceptions
        ----------
        ValueError: 
            The userName parameter is either None or a string of length zero.
        VerificationError:
            The signature cannot be verified.  The message should include a description 
            of the problem encountered
        RuntimeError:
            Raised when an inconsistent entry in the database is found.
        """
        pass

    @abstractmethod
    def associate_unp(self, principal: SignedPrincipalId, new_user_name: str, new_salt: bytes, new_verify_key: bytes):
        """
        Associates (or updates) a user-name/password combination to the current logged user.
        """
        pass

    @abstractmethod
    def associate(self, principal: SignedPrincipalId, new_principal: GCPrincipalId):
        """
        Associate an external credential to the current logged user
        """
        pass

    @abstractmethod
    def disassociate(self, principal: SignedPrincipalId, scope: str):
        """
        Disassociates a particular authentication protocol 
        """
        pass
